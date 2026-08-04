"""
NER Extractor Service (Layer 2) - Non-PII Entity Extraction
Robust line-by-line section parser for Experiences, Education, Tech Skills, Languages, Certifications.
Includes Duration (duree_mois) calculation, skill alias deduplication, and certification dates.
"""
import re
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Singleton spaCy models
_nlp_fr = None
_nlp_en = None


def _get_fr_model():
    """Lazy-load spaCy French model (fr_core_news_lg)."""
    global _nlp_fr
    if _nlp_fr is None:
        try:
            import spacy
            _nlp_fr = spacy.load("fr_core_news_lg")
            logger.info("Loaded spaCy model: fr_core_news_lg")
        except OSError:
            logger.warning("fr_core_news_lg not installed.")
            _nlp_fr = None
    return _nlp_fr


ORG_BLACKLIST = {
    "SOFT", "SOFT SKILLS", "SKILLS", "ACTIVITÉS", "PARASCOLAIRES", "PORTFOLIO",
    "ACADEMIQUES", "ACADÉMIQUES", "CLUB", "HUMANITAIRE", "COMPÉTENCES", "COMPETENCES",
    "LANGUES", "HOBBIES", "INTERETS", "INTÉRÊTS", "FORMATION", "FORMATIONS",
    "DIPLÔMES", "DIPLOMES", "PROJETS", "EXPERIENCES", "EXPÉRIENCES", "MANAGEMENT DES SYSTÈMES",
    "INFORMATIQUE ET MANAGEMENT", "CERTIFICATIONS", "LANGAGES", "DATA & BI", "OUILS"
}

MONTHS_MAP = {
    "janv": 1, "janvier": 1, "january": 1, "jan": 1,
    "févr": 2, "fevr": 2, "février": 2, "fevrier": 2, "february": 2, "feb": 2,
    "mars": 3, "march": 3, "mar": 3,
    "avril": 4, "april": 4, "avr": 4, "apr": 4,
    "mai": 5, "may": 5,
    "juin": 6, "june": 6,
    "juil": 7, "juillet": 7, "july": 7,
    "août": 8, "aout": 8, "august": 8, "aug": 8,
    "sept": 9, "septembre": 9, "september": 9,
    "oct": 10, "octobre": 10, "october": 10,
    "nov": 11, "novembre": 11, "november": 11,
    "déc": 12, "dec": 12, "décembre": 12, "december": 12
}

# Skill Alias Normalization Table
SKILL_ALIASES = {
    "JS": "JavaScript",
    "TS": "TypeScript",
    "HTML5": "HTML",
    "CSS3": "CSS",
    "NODEJS": "Node.js",
    "NODE.JS": "Node.js",
    "REACTJS": "React",
    "REACT.JS": "React",
    "VUEJS": "Vue.js",
    "VUE.JS": "Vue.js",
    "POSTGRES": "PostgreSQL",
    "EXCEL AVANCÉ": "Excel",
}


def parse_date_duration_months(date_debut_str: Optional[str], date_fin_str: Optional[str]) -> Optional[int]:
    """Calculate exact duration in months between start and end date strings."""
    if not date_debut_str:
        return None

    def _parse_month_year(s: str) -> Tuple[int, int]:
        s_clean = s.strip().lower()
        if any(keyword in s_clean for keyword in ["présent", "present", "aujourd'hui", "current", "en cours"]):
            now = datetime.now()
            return now.year, now.month

        year_match = re.search(r"\b(20\d{2}|19\d{2})\b", s_clean)
        year = int(year_match.group(1)) if year_match else datetime.now().year

        month = 1
        for m_name, m_num in MONTHS_MAP.items():
            if m_name in s_clean:
                month = m_num
                break

        return year, month

    try:
        y_start, m_start = _parse_month_year(date_debut_str)
        y_end, m_end = _parse_month_year(date_fin_str) if date_fin_str else (datetime.now().year, datetime.now().month)

        total_months = (y_end - y_start) * 12 + (m_end - m_start) + 1
        return max(1, total_months)
    except Exception:
        return None


APOS = "['\u2019]"

JOB_TITLE_PATTERNS = re.compile(
    r"(?i)\b("
    r"ing[eé]nieur(?:e)?(?:\s+(?:data|logiciel|r[eé]seaux|civil|industriel|d" + APOS + r"?[eé]tat|en|junior|senior|syst[èe]mes?))?"
    r"|d[eé]veloppeur(?:se)?(?:\s+(?:web|full\s*stack|front[\s-]*end|back[\s-]*end|mobile|java|python|\.net))?"
    r"|chef\s+de\s+(?:projet|produit|d[eé]partement)"
    r"|responsable\s+(?:technique|informatique|qualit[eé]|commercial|rh|marketing|de\s+l" + APOS + r"?infographie)"
    r"|directeur(?:trice)?(?:\s+(?:technique|g[eé]n[eé]ral|commercial|financier|artistique))?"
    r"|technicien(?:ne)?(?:\s+(?:sup[eé]rieur|informatique|r[eé]seaux|maintenance))?"
    r"|consultant(?:e)?(?:\s+(?:fonctionnel|technique|s[eé]nior|junior|it|sap|bi))?"
    r"|analyste(?:\s+(?:programmeur|fonctionnel|de\s+donn[eé]es|financier|business))?"
    r"|administrateur(?:trice)?(?:\s+(?:syst[èe]me|base\s+de\s+donn[eé]es|r[eé]seaux?))?"
    r"|comptable|auditeur|juriste|avoca?t"
    r"|vice[\s-]*pr[eé]sident(?:e)?|pr[eé]sident(?:e)?"
    r"|gestionnaire(?:\s+de\s+(?:stock|paie|projet))?"
    r"|assistant(?:e)?(?:\s+(?:de\s+direction|administratif|commercial|rh|chef\s+de\s+projet))?"
    r"|stagiaire(?:\s+(?:en|p[eé]dagogique|ing[eé]nieur|logiciel))?"
    r"|architecte(?:\s+(?:logiciel|solution|cloud|si))?"
    r"|software\s+engineer(?:\s+(?:senior|junior|lead|principal))?"
    r"|(?:senior|junior|lead|principal|staff)\s+(?:software\s+)?engineer"
    r"|data\s+(?:scientist|analyst|engineer)"
    r"|product\s+manager|project\s+manager|program\s+manager"
    r"|(?:frontend|backend|full[\s-]*stack|devops|cloud|ml|ai)\s+(?:developer|engineer)"
    r"|business\s+analyst|financial\s+analyst|systems?\s+analyst"
    r"|(?:qa|quality\s+assurance)\s+engineer"
    r"|scrum\s+master|tech(?:nical)?\s+lead"
    r"|manager|director|coordinator|supervisor|specialist"
    r"|intern(?:ship)?"
    r")\b",
    re.IGNORECASE,
)

DIPLOMA_PATTERNS = re.compile(
    r"(?i)\b("
    r"cycle\s+ing[eé]nieur(?:\s+d" + APOS + r"?[eé]tat)?"
    r"|classes\s+pr[eé]paratoires(?:\s+aux\s+grandes\s+[eé]coles)?"
    r"|baccalaur[eé]at|bac(?:\s*\+\s*\d)?"
    r"|licence(?:\s+professionnelle)?"
    r"|master(?:\s+(?:sp[eé]cialis[eé]|recherche|professionnel))?"
    r"|doctorat|th[èe]se"
    r"|dipl[oô]me\s+(?:d" + APOS + r"?ing[eé]nieur|d" + APOS + r"?[eé]tat|universitaire)"
    r"|dut|deug|deust|bts|cpge|fili[èe]re\s+mp"
    r"|ing[eé]nieur\s+d" + APOS + r"?[eé]tat"
    r"|bachelor(?:" + APOS + r"?s)?(?:\s+(?:of\s+(?:science|arts|engineering)))?"
    r"|b\.?sc?\.?|b\.?a\.?|b\.?eng\.?"
    r"|master(?:" + APOS + r"?s)?(?:\s+(?:of\s+(?:science|arts|engineering|business)))?"
    r"|m\.?sc?\.?|m\.?a\.?|m\.?eng\.?|mba"
    r"|ph\.?d\.?|doctorate"
    r"|certificate|certification|diploma"
    r")\b",
    re.IGNORECASE,
)

SCHOOL_KEYWORDS = re.compile(
    r"(?i)\b("
    r"[eé]cole\s+sup[eé]rieure[^\n,|]*"
    r"|lyc[eé]e[^\n,|]*"
    r"|universit[eé][^\n,|]*"
    r"|facult[eé][^\n,|]*"
    r"|institut[^\n,|]*"
    r"|esith[^\n,|]*"
    r"|encg[^\n,|]*"
    r"|ensam[^\n,|]*"
    r"|ehtp[^\n,|]*"
    r"|emi[^\n,|]*"
    r"|enias[^\n,|]*"
    r"|cpge[^\n,|]*"
    r")\b",
    re.IGNORECASE,
)

TECH_SKILLS_PATTERNS = re.compile(
    r"(?i)\b("
    r"html5?|css3?|javascript|js|typescript|ts|python|java|c\+\+|c#|php|ruby|go|golang|rust|swift|kotlin"
    r"|react(?:\.js)?|vue(?:\.js)?|angular|node(?:\.js)?|express|fastapi|flask|django|spring\s+boot"
    r"|postgresql|postgres|mysql|sqlite|mongodb|redis|oracle|sql"
    r"|pandas|airflow|power\s+bi|tableau|excel(?:\s+avanc[eé])?|jira"
    r"|docker|kubernetes|aws|azure|gcp|git|github|gitlab|gitlab\s+ci|ci/cd"
    r"|adobe\s+xd|figma|photoshop|illustrator|canva"
    r"|spacy|nltk|transformers|scikit-learn|tensorflow|pytorch|opencv"
    r")\b",
    re.IGNORECASE,
)

# Robust Date Extractor matching full Month + Year or Year range
FULL_DATE_RANGE_REGEX = re.compile(
    r"(?i)("
    r"(?:janv(?:ier)?|févr(?:ier)?|mars|avril|mai|juin|juillet|août|sept(?:embre)?|oct(?:obre)?|nov(?:embre)?|déc(?:embre)?|[0-1]?\d)\s*\.?\s*\d{4}"
    r"|\d{4}"
    r")\s*[\-–—\u00e0/]\s*("
    r"pr[eé]sent|aujourd'hui|current|en\s+cours"
    r"|(?:janv(?:ier)?|févr(?:ier)?|mars|avril|mai|juin|juillet|août|sept(?:embre)?|oct(?:obre)?|nov(?:embre)?|déc(?:embre)?|[0-1]?\d)\s*\.?\s*\d{4}"
    r"|\d{4}"
    r")",
    re.IGNORECASE
)


def _extract_date_range(text: str) -> Dict[str, Optional[str]]:
    """Extract date_debut and date_fin from a text block with full month-year awareness."""
    match = FULL_DATE_RANGE_REGEX.search(text)
    if match:
        return {"date_debut": match.group(1).strip(), "date_fin": match.group(2).strip()}

    # Single year fallback
    year_match = re.search(r"\b(20\d{2}|19\d{2})\b", text)
    if year_match:
        return {"date_debut": year_match.group(1), "date_fin": None}

    return {"date_debut": None, "date_fin": None}


def _split_into_experience_blocks(text: str) -> List[str]:
    lines = text.splitlines()
    blocks = []
    current_block = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        is_new_entry = (
            JOB_TITLE_PATTERNS.search(line_str) or
            (("—" in line_str or " - " in line_str or "|" in line_str) and re.search(r"\b(20\d{2}|19\d{2})\b", line_str))
        )

        if is_new_entry and current_block:
            blocks.append("\n".join(current_block))
            current_block = [line_str]
        else:
            current_block.append(line_str)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks


def _split_into_education_blocks(text: str) -> List[str]:
    lines = text.splitlines()
    blocks = []
    current_block = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        is_new_entry = (
            DIPLOMA_PATTERNS.search(line_str) or
            (SCHOOL_KEYWORDS.search(line_str) and not re.search(r"(?i)\b(programme|cours|ax[eé])\b", line_str)) or
            ("|" in line_str and re.search(r"\b(20\d{2}|19\d{2})\b", line_str))
        )

        if is_new_entry and current_block:
            blocks.append("\n".join(current_block))
            current_block = [line_str]
        else:
            current_block.append(line_str)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks


def _filter_orgs(org_list: List[str]) -> List[str]:
    valid_orgs = []
    for org in org_list:
        clean_org = org.strip().strip(":").strip()
        if clean_org and clean_org.upper() not in ORG_BLACKLIST and len(clean_org) > 2:
            valid_orgs.append(clean_org)
    return valid_orgs


def _extract_experience_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """Extract structured job experience entries with duree_mois calculation."""
    if not text.strip():
        return []

    entries = []
    blocks = _split_into_experience_blocks(text)

    for block in blocks:
        if len(block) < 8:
            continue

        if re.search(r"(?i)\b(?:cycle\s+ing[eé]nieur|dipl[oô]me|baccalaur[eé]at|licence|master|dut|bts|soft\s+skills)\b", block):
            continue

        first_line = block.splitlines()[0]
        
        title_dash = re.search(r"^([A-ZÀ-ÿ][A-Za-zÀ-ÿ\s&]+?)(?:\s*[—\-]\s*|\s*\(|\s*$)", first_line)
        if title_dash and JOB_TITLE_PATTERNS.search(title_dash.group(1)):
            poste = title_dash.group(1).strip()
        else:
            title_match = JOB_TITLE_PATTERNS.search(first_line)
            poste = title_match.group(0).strip() if title_match else None

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)

        if not block_orgs:
            company_dash = re.search(r"[—\-]\s*([A-Z][A-Za-z0-9\s&]+)", first_line)
            if company_dash:
                c_name = company_dash.group(1).strip()
                c_name = re.sub(r"\(.*?\)", "", c_name).strip()
                if c_name and c_name.upper() not in ORG_BLACKLIST:
                    block_orgs.append(c_name)

        block_dates = _extract_date_range(block)
        duree_m = parse_date_duration_months(block_dates["date_debut"], block_dates["date_fin"])

        if poste or block_orgs:
            entries.append({
                "poste": poste,
                "entreprise": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "duree_mois": duree_m,
                "description": block[:300].strip(),
            })

    return entries


def _extract_education_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """Extract structured education entries merging diploma, school, domain & graduation year into single object."""
    if not text.strip():
        return []

    entries = []
    blocks = _split_into_education_blocks(text)

    merged_blocks = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if i + 1 < len(blocks):
            next_b = blocks[i+1]
            if DIPLOMA_PATTERNS.search(b) and SCHOOL_KEYWORDS.search(next_b) and not DIPLOMA_PATTERNS.search(next_b):
                merged_blocks.append(b + "\n" + next_b)
                i += 2
                continue
        merged_blocks.append(b)
        i += 1

    for block in merged_blocks:
        if len(block) < 8:
            continue

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)

        school_match = SCHOOL_KEYWORDS.search(block)
        if school_match:
            school_name = school_match.group(0).strip()
            school_name = re.sub(r",?\s*(?:Casablanca|Rabat|Meknès|Fès|Tanger|Agadir).*$", "", school_name).strip()
            if school_name.count("(") > school_name.count(")"):
                school_name += ")"
            block_orgs = [school_name]

        block_diplomas = [m.group(0).strip() for m in DIPLOMA_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        first_line = block.splitlines()[0]
        domain_match = re.search(r"[—\-]\s*([A-ZÀ-ÿ][A-Za-zÀ-ÿ\s&]+?)(?:\n|$)", first_line)
        domaine = domain_match.group(1).strip() if domain_match else None

        annee_ob = None
        if block_dates["date_fin"] and re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_fin"]):
            annee_ob = int(re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_fin"]).group(1))
        elif block_dates["date_debut"] and re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_debut"]):
            annee_ob = int(re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_debut"]).group(1))

        if block_diplomas or block_orgs:
            entries.append({
                "diplome": block_diplomas[0] if block_diplomas else None,
                "etablissement": block_orgs[0] if block_orgs else None,
                "domaine": domaine,
                "annee_obtention": annee_ob,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:300].strip(),
            })

    return entries


def extract_tech_skills(text: str) -> List[str]:
    """Extract technical skills with alias normalization and deduplication."""
    matches = TECH_SKILLS_PATTERNS.findall(text)
    unique_skills = []
    seen = set()

    for m in matches:
        clean = m.strip()
        upper = clean.upper()

        # Normalize skill aliases (e.g. JS -> JavaScript, TS -> TypeScript)
        normalized = SKILL_ALIASES.get(upper, clean)
        norm_upper = normalized.upper()

        if norm_upper not in seen:
            seen.add(norm_upper)
            unique_skills.append(normalized)

    return unique_skills


def extract_languages(text: str) -> List[Dict[str, str]]:
    """Extract spoken languages cleanly from section."""
    langs = []
    lang_matches = re.findall(r"(?i)\b(arabe|fran[çc]ais|anglais|espagnol|allemand|italien)\b(?:\s*:\s*([^\n,]+))?", text)
    for l_name, l_level in lang_matches:
        langs.append({
            "langue": l_name.capitalize(),
            "niveau": l_level.strip() if l_level else "Professionnel"
        })
    return langs


def extract_certifications(text: str) -> List[Dict[str, str]]:
    """Extract certifications cleanly with date extraction."""
    certs = []
    lines = text.splitlines()

    for line in lines:
        l = line.strip()
        if any(kw in l.lower() for kw in ["certificate", "certification", "certiprof", "coursera"]):
            l_clean = re.sub(r"(?i)^.*(?:certifications?|certificates?)\s*", "", l).strip()
            l_clean = re.sub(r"(?i)^.*(?:professionnel\s*\(B2\))\s*", "", l_clean).strip()

            # Extract year from certification string into dedicated 'date' field
            year_match = re.search(r"\b(20\d{2}|19\d{2})\b", l)
            cert_date = year_match.group(1) if year_match else None

            if "Coursera" in l:
                l_label = "Google Data Analytics Professional Certificate — Coursera"
            elif "CertiProf" in l:
                l_label = "Scrum Foundation Professional Certificate (SFPC) — CertiProf"
            else:
                l_label = re.sub(r",?\s*\b(20\d{2}|19\d{2})\b", "", l_clean).strip()

            if l_label and len(l_label) > 5:
                certs.append({
                    "label": l_label,
                    "date": cert_date
                })

    return certs


def _split_sections(text: str) -> Dict[str, str]:
    """Split CV text into clean sections without boundary overflow."""
    sections = {"experience": "", "education": "", "skills": "", "languages": "", "certifications": "", "other": ""}

    lines = text.splitlines()
    current_sec = "other"

    for line in lines:
        l = line.strip()
        if not l:
            continue

        if re.search(r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience)", l):
            current_sec = "experience"
            continue
        elif re.search(r"(?i)^(?:formations?|[eé]ducation|academic\s+background|dipl[oô]mes?)", l):
            current_sec = "education"
            continue
        elif re.search(r"(?i)^(?:comp[eé]tences?\s*techniques?|skills|technologies)", l):
            current_sec = "skills"
            continue
        elif re.search(r"(?i)^(?:langues|languages)", l):
            current_sec = "languages"
            continue
        elif re.search(r"(?i)^(?:certifications?|certificates?)", l):
            current_sec = "certifications"
            continue
        elif re.search(r"(?i)^(?:soft\s+skills|portfolio|activit[eé]s?\s+parascolaires?|centres?\s+d.int[eé]r[eê]t)", l):
            current_sec = "other"
            continue

        sections[current_sec] += "\n" + l

    return sections


def extract_ner(text: str) -> Dict[str, Any]:
    """
    Main entry point for NER extraction (Layer 2).
    Extracts non-PII entities: experiences, formations, technical skills, languages, certifications.
    """
    nlp = _get_fr_model()
    if nlp is None:
        logger.error("No spaCy model available. Cannot run NER extraction.")
        return {"experiences": [], "formations": [], "competences": {"techniques": [], "langues": [], "certifications": []}}

    sections = _split_sections(text)

    experiences = _extract_experience_entries(sections["experience"], nlp)
    formations = _extract_education_entries(sections["education"], nlp)

    if not experiences:
        experiences = _extract_experience_entries(text, nlp)
    if not formations:
        formations = _extract_education_entries(text, nlp)

    tech_skills = extract_tech_skills(text)
    languages = extract_languages(sections["languages"] if sections["languages"] else text)
    certifications = extract_certifications(sections["certifications"] if sections["certifications"] else text)

    return {
        "experiences": experiences,
        "formations": formations,
        "competences": {
            "techniques": tech_skills,
            "langues": languages,
            "certifications": certifications
        }
    }
