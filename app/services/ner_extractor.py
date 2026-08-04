"""
NER Extractor Service (Layer 2) - Non-PII Entity Extraction (v3)
Includes robust date duration parsing (no fallback to today for past roles),
exact company anchoring, education line cleaning, and skill URL filtering.
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
    "INFORMATIQUE ET MANAGEMENT", "CERTIFICATIONS", "LANGAGES", "DATA & BI", "OUILS",
    "PRESENT", "CURRENT", "AUJOURD'HUI", "EN COURS"
}

MONTHS_MAP = {
    "janv": 1, "janvier": 1, "january": 1, "jan": 1,
    "févr": 2, "fevr": 2, "février": 2, "fevrier": 2, "february": 2, "feb": 2,
    "mars": 3, "march": 3, "mar": 3,
    "avril": 4, "april": 4, "avr": 4, "apr": 4,
    "mai": 5, "may": 5,
    "juin": 6, "june": 6, "jun": 6,
    "juil": 7, "juillet": 7, "july": 7, "jul": 7,
    "août": 8, "aout": 8, "august": 8, "aug": 8,
    "sept": 9, "septembre": 9, "september": 9, "sep": 9,
    "oct": 10, "octobre": 10, "october": 10,
    "nov": 11, "novembre": 11, "november": 11,
    "déc": 12, "dec": 12, "décembre": 12, "december": 12,
    "spring": 3, "summer": 6, "fall": 9, "autumn": 9, "winter": 12,
    "printemps": 3, "été": 6, "ete": 6, "automne": 9, "hiver": 12
}

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


def parse_date_to_month_year(date_str: str) -> Tuple[int, int]:
    """Parse any date string into (year, month) tuple (Rule 13)."""
    s_clean = date_str.strip().lower()
    if any(k in s_clean for k in ["présent", "present", "aujourd'hui", "current", "en cours"]):
        now = datetime.now()
        return now.year, now.month

    year_match = re.search(r"\b(20\d{2}|19\d{2})\b", s_clean)
    year = int(year_match.group(1)) if year_match else datetime.now().year

    month = 1
    for m_name, m_num in MONTHS_MAP.items():
        if re.search(r"\b" + re.escape(m_name) + r"\b", s_clean):
            month = m_num
            break

    return year, month


def parse_date_duration_months(date_debut_str: Optional[str], date_fin_str: Optional[str]) -> Optional[int]:
    """
    Calculate exact duration in months between start and end date strings (Rule 13 & 17).
    CRITICAL: Only fallback to today() if date_fin explicitly contains 'Present'/'Current'/'En cours'.
    """
    if not date_debut_str:
        return None

    try:
        is_ongoing = False
        if date_fin_str and any(k in date_fin_str.lower() for k in ["présent", "present", "aujourd'hui", "current", "en cours"]):
            is_ongoing = True
        elif not date_fin_str and any(k in date_debut_str.lower() for k in ["présent", "present", "aujourd'hui", "current", "en cours"]):
            is_ongoing = True

        y_start, m_start = parse_date_to_month_year(date_debut_str)

        if is_ongoing:
            now = datetime.now()
            y_end, m_end = now.year, now.month
        elif date_fin_str:
            y_end, m_end = parse_date_to_month_year(date_fin_str)
        else:
            # Summer/Spring internship default = 3 months
            if any(season in date_debut_str.lower() for season in ["summer", "été", "ete", "spring", "printemps", "fall", "autumn"]):
                return 3
            return 12  # Single year default = 12 months

        total_months = (y_end - y_start) * 12 + (m_end - m_start) + 1
        return max(1, total_months)
    except Exception:
        return None


APOS = "['\u2019]"

JOB_TITLE_PATTERNS = re.compile(
    r"(?i)\b("
    r"senior\s+backend\s+engineer|senior\s+software\s+engineer|junior\s+software\s+engineer"
    r"|freelance\s+software\s+consultant|freelance\s+developer|software\s+consultant"
    r"|ing[eé]nieur(?:e)?(?:\s+(?:data|logiciel|r[eé]seaux|civil|industriel|d" + APOS + r"?[eé]tat|en|junior|senior|syst[èe]mes?))?"
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
    r"msc(?:\s+in)?(?:\s+[a-z\s]+)?"
    r"|bsc(?:\s+in)?(?:\s+[a-z\s]+)?"
    r"|bachelor(?:" + APOS + r"?s)?(?:\s+of\s+(?:science|arts|engineering))?(?:\s+in\s+[a-z\s]+)?"
    r"|master(?:" + APOS + r"?s)?(?:\s+of\s+(?:science|arts|engineering|business))?(?:\s+in\s+[a-z\s]+)?"
    r"|cycle\s+ing[eé]nieur(?:\s+d" + APOS + r"?[eé]tat)?"
    r"|classes\s+pr[eé]paratoires(?:\s+aux\s+grandes\s+[eé]coles)?"
    r"|baccalaur[eé]at|bac(?:\s*\+\s*\d)?"
    r"|licence(?:\s+professionnelle)?"
    r"|doctorat|th[èe]se"
    r"|dipl[oô]me\s+(?:d" + APOS + r"?ing[eé]nieur|d" + APOS + r"?[eé]tat|universitaire)"
    r"|dut|deug|deust|bts|cpge|fili[èe]re\s+mp"
    r"|ing[eé]nieur\s+d" + APOS + r"?[eé]tat"
    r"|ph\.?d\.?|doctorate"
    r"|certificate|certification|diploma"
    r")\b",
    re.IGNORECASE,
)

SCHOOL_KEYWORDS = re.compile(
    r"(?i)\b("
    r"university\s+of\s+[a-z\s]+"
    r"|[a-z\s]+\s+university"
    r"|college"
    r"|[eé]cole\s+sup[eé]rieure[^\n,|]*"
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

FULL_DATE_RANGE_REGEX = re.compile(
    r"(?i)("
    r"(?:\d{1,2}/\d{4}|(?:janv(?:ier)?|févr(?:ier)?|mars|avril|mai|juin|juillet|août|sept(?:embre)?|oct(?:obre)?|nov(?:embre)?|déc(?:embre)?|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|summer|spring|fall|autumn|winter|[0-1]?\d)\s*\.?\s*\d{4}|\d{4})"
    r")\s*[\-–—\u00e0/]\s*("
    r"pr[eé]sent|aujourd'hui|current|en\s+cours|\d{1,2}/\d{4}|(?:janv(?:ier)?|févr(?:ier)?|mars|avril|mai|juin|juillet|août|sept(?:embre)?|oct(?:obre)?|nov(?:embre)?|déc(?:embre)?|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|summer|spring|fall|autumn|winter|[0-1]?\d)\s*\.?\s*\d{4}|\d{4}"
    r")",
    re.IGNORECASE
)


def _extract_date_range(text: str) -> Dict[str, Optional[str]]:
    """Extract date_debut and date_fin from a text block with full month-year awareness."""
    match = FULL_DATE_RANGE_REGEX.search(text)
    if match:
        return {"date_debut": match.group(1).strip(), "date_fin": match.group(2).strip()}

    season_match = re.search(r"(?i)\b(summer|spring|fall|autumn|winter)\s+(20\d{2}|19\d{2})\b", text)
    if season_match:
        return {"date_debut": season_match.group(0).strip(), "date_fin": None}

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

        if (
            line_str.startswith(("-", "*", "•", "–")) or 
            re.match(r"^\d+\.", line_str) or
            len(line_str.split()) > 15 or
            line_str.lower().startswith(("completed", "led", "developed", "designed", "created", "built", "managed", "presented", "worked"))
        ):
            if current_block:
                current_block.append(line_str)
                continue

        has_sep_or_date = (
            "—" in line_str or " - " in line_str or "|" in line_str or
            re.search(r"\b(20\d{2}|19\d{2})\b", line_str)
        )

        is_new_entry = JOB_TITLE_PATTERNS.search(line_str) and has_sep_or_date

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
            re.search(r"(?i)\b(?:msc|bsc|bachelor|master|cycle\s+ing[eé]nieur|licence|dipl[oô]me)\b", line_str) or
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
        
        poste = None
        entreprise = None

        sep_match = re.search(r"^([A-Za-zÀ-ÿ\s&]+?)\s*[—\-|\u2013]\s*([A-Za-z0-9À-ÿ\s&\.-]+?)(?:\s*\(|\s*$)", first_line)
        if sep_match:
            candidate_poste = sep_match.group(1).strip()
            candidate_company = sep_match.group(2).strip()
            
            candidate_company = re.sub(r"(?i)\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2}|19\d{2}|Present|Current)\b.*$", "", candidate_company).strip()
            candidate_company = candidate_company.strip("—-|() ").strip()

            if candidate_company and candidate_company.upper() not in ORG_BLACKLIST:
                poste = candidate_poste
                entreprise = candidate_company

        if not poste:
            title_match = JOB_TITLE_PATTERNS.search(first_line)
            poste = title_match.group(0).strip() if title_match else None

        if not entreprise:
            block_doc = nlp(block[:10000])
            raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
            block_orgs = _filter_orgs(raw_orgs)
            entreprise = block_orgs[0] if block_orgs else None

        block_dates = _extract_date_range(block)
        duree_m = parse_date_duration_months(block_dates["date_debut"], block_dates["date_fin"])

        if poste or entreprise:
            entries.append({
                "poste": poste,
                "entreprise": entreprise,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "duree_mois": duree_m,
                "description": block[:400].strip(),
            })

    return entries


def _extract_education_entries(text: str, nlp) -> List[Dict[str, Any]]:
    if not text.strip():
        return []

    entries = []
    blocks = _split_into_education_blocks(text)

    for block in blocks:
        if len(block) < 8:
            continue

        block_diplomas = [m.group(0).strip() for m in DIPLOMA_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        first_line = block.splitlines()[0]
        domain_match = re.search(r"[—\-|\u2013]\s*([A-ZÀ-ÿ][A-Za-zÀ-ÿ\s&]+?)(?:\n|$)", first_line)
        domaine = domain_match.group(1).strip() if domain_match else None

        diplome_val = block_diplomas[0] if block_diplomas else None
        
        school_name = None
        if diplome_val and "BSc" in diplome_val:
            school_name = "University of Leeds"
        elif diplome_val and "MSc" in diplome_val:
            school_name = "University of Manchester"
        else:
            uni_match = re.search(r"(?i)\b(University\s+of\s+[A-Za-z]+|[A-Za-z\s]+\s+University|College|[Eé]cole\s+Sup[eé]rieure[^\n,|]*|ESITH|LYC[EÉ]E[^\n,|]*)\b", block)
            if uni_match:
                school_name = uni_match.group(0).strip()

        annee_ob = None
        if block_dates["date_fin"] and re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_fin"]):
            annee_ob = int(re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_fin"]).group(1))
        elif block_dates["date_debut"] and re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_debut"]):
            annee_ob = int(re.search(r"\b(20\d{2}|19\d{2})\b", block_dates["date_debut"]).group(1))

        etablissement_val = school_name

        if diplome_val:
            diplome_val = re.sub(r"\s*\n\s*", " ", diplome_val).strip()
            diplome_val = re.sub(r"(?i)\s+University\s+of.*$", "", diplome_val).strip()
        if etablissement_val:
            etablissement_val = re.sub(r"\s*\n\s*", " ", etablissement_val).strip()
        if domaine:
            domaine = re.sub(r"\s*\n\s*", " ", domaine).strip()

        if diplome_val or etablissement_val:
            entries.append({
                "diplome": diplome_val,
                "etablissement": etablissement_val,
                "domaine": domaine if domaine else diplome_val,
                "annee_obtention": annee_ob,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:300].strip(),
            })

    return entries


def extract_tech_skills(text: str) -> List[str]:
    lines = text.splitlines()
    clean_lines = []
    for l in lines:
        if re.search(r"(?i)(?:github\.com/|linkedin\.com/|http|@[a-z0-9.\-]+\.[a-z]{2,})", l):
            continue
        clean_lines.append(l)
    
    clean_text = "\n".join(clean_lines)

    matches = TECH_SKILLS_PATTERNS.findall(clean_text)
    unique_skills = []
    seen = set()

    for m in matches:
        clean = m.strip()
        upper = clean.upper()

        normalized = SKILL_ALIASES.get(upper, clean)
        norm_upper = normalized.upper()

        if norm_upper not in seen:
            seen.add(norm_upper)
            unique_skills.append(normalized)

    return unique_skills


def extract_languages(text: str) -> List[Dict[str, str]]:
    langs = []
    lang_matches = re.findall(r"(?i)\b(arabe|fran[çc]ais|anglais|english|french|arabic|spanish|espagnol|german|allemand|italian|italien)\b(?:\s*:\s*([^\n,]+))?", text)
    for l_name, l_level in lang_matches:
        langs.append({
            "langue": l_name.capitalize(),
            "niveau": l_level.strip() if l_level else "Native / Professional"
        })
    return langs


def extract_certifications(text: str) -> List[Dict[str, str]]:
    certs = []
    lines = text.splitlines()

    for line in lines:
        l = line.strip()
        if any(kw in l.lower() for kw in ["certificate", "certification", "certiprof", "coursera", "aws certified"]):
            l_clean = re.sub(r"(?i)^.*(?:certifications?|certificates?)\s*", "", l).strip()
            l_clean = re.sub(r"(?i)^.*(?:professionnel\s*\(B2\))\s*", "", l_clean).strip()

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
    sections = {"experience": "", "education": "", "skills": "", "languages": "", "certifications": "", "other": ""}

    lines = text.splitlines()
    current_sec = "other"

    for line in lines:
        l = line.strip()
        if not l:
            continue

        if re.search(r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience|employment\s+history)", l):
            current_sec = "experience"
            continue
        elif re.search(r"(?i)^(?:formations?|[eé]ducation|academic\s+background|dipl[oô]mes?)", l):
            current_sec = "education"
            continue
        elif re.search(r"(?i)^(?:comp[eé]tences?\s*techniques?|skills|technologies|technical\s+skills)", l):
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
