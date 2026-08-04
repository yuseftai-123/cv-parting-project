"""
NER Extractor Service (Layer 2) - Non-PII Entity Extraction
Robust line-by-line section parser for Experiences, Education, Tech Skills, Languages, Certifications.
"""
import re
import logging
from typing import List, Dict, Any, Optional

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
    "INFORMATIQUE ET MANAGEMENT"
}

APOS = "['\u2019]"

JOB_TITLE_PATTERNS = re.compile(
    r"(?i)\b("
    r"ing[eé]nieur(?:e)?(?:\s+(?:d" + APOS + r"?[eé]tat|en|informatique|logiciel|r[eé]seaux|civil|industriel|data|junior|senior))?"
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
    r"baccalaur[eé]at|bac(?:\s*\+\s*\d)?"
    r"|licence(?:\s+professionnelle)?|master(?:\s+(?:sp[eé]cialis[eé]|recherche|professionnel))?"
    r"|doctorat|th[èe]se"
    r"|cycle\s+ing[eé]nieur(?:\s+d" + APOS + r"?[eé]tat)?"
    r"|classes\s+pr[eé]paratoires(?:\s+aux\s+grandes\s+[eé]coles)?"
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

DATE_RANGE_PATTERN = re.compile(
    r"(?i)("
    r"\d{4}\s*[-\u2013\u2014/\u00e0]\s*(?:\d{4}|pr[eé]sent|aujourd" + APOS + r"?hui|present|current|en\s+cours)"
    r"|\b(?:jan(?:v(?:ier)?)?|f[eé]v(?:rier)?|feb(?:ruary)?|mars?|march?|avr(?:il)?|apr(?:il)?"
    r"|mai|may|juin|june?|juil(?:let)?|july?|ao[ûu]t|aug(?:ust)?"
    r"|sept(?:embre|ember)?|oct(?:obre|ober)?|nov(?:embre|ember)?|d[eé]c(?:embre|ember)?)"
    r"\s*\.?\s*\d{4}\s*[-\u2013\u2014/\u00e0]\s*"
    r"(?:jan(?:v(?:ier)?)?|f[eé]v(?:rier)?|feb(?:ruary)?|mars?|march?|avr(?:il)?|apr(?:il)?"
    r"|mai|may|juin|june?|juil(?:let)?|july?|ao[ûu]t|aug(?:ust)?"
    r"|sept(?:embre|ember)?|oct(?:obre|ober)?|nov(?:embre|ember)?|d[eé]c(?:embre|ember)?)"
    r"\s*\.?\s*\d{4}"
    r"|\b\d{4}\b"
    r")",
)


def _extract_date_range(text: str) -> Dict[str, Optional[str]]:
    """Extract date_debut and date_fin from a text block."""
    matches = DATE_RANGE_PATTERN.findall(text)
    result = {"date_debut": None, "date_fin": None}
    if not matches:
        return result

    first = matches[0].strip()
    range_sep = re.search(r"[-\u2013\u2014/\u00e0]", first)
    if range_sep:
        parts = re.split(r"\s*[-\u2013\u2014/\u00e0]\s*", first, maxsplit=1)
        if len(parts) == 2:
            result["date_debut"] = parts[0].strip()
            result["date_fin"] = parts[1].strip()
            return result

    result["date_debut"] = first
    if len(matches) > 1:
        result["date_fin"] = matches[1].strip()
    return result


def _split_into_experience_blocks(text: str) -> List[str]:
    """Split experience text into individual job blocks by job title or date headers."""
    lines = text.splitlines()
    blocks = []
    current_block = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        # Check if line indicates a new job entry (job title or company separator)
        is_new_entry = (
            JOB_TITLE_PATTERNS.search(line_str) or
            ("—" in line_str or " - " in line_str or "|" in line_str) and DATE_RANGE_PATTERN.search(line_str)
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
    """Split education text into individual formation blocks."""
    lines = text.splitlines()
    blocks = []
    current_block = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        is_new_entry = (
            DIPLOMA_PATTERNS.search(line_str) or
            DATE_RANGE_PATTERN.search(line_str) or
            SCHOOL_KEYWORDS.search(line_str)
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
    """Filter out falsely recognized company names matching the blacklist."""
    valid_orgs = []
    for org in org_list:
        clean_org = org.strip().strip(":").strip()
        if clean_org and clean_org.upper() not in ORG_BLACKLIST and len(clean_org) > 2:
            valid_orgs.append(clean_org)
    return valid_orgs


def _extract_experience_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """Extract structured job experience entries."""
    if not text.strip():
        return []

    entries = []
    blocks = _split_into_experience_blocks(text)

    for block in blocks:
        if len(block) < 8:
            continue

        # Skip block if it is purely education/formation or soft skills
        if re.search(r"(?i)\b(?:cycle\s+ing[eé]nieur|dipl[oô]me|baccalaur[eé]at|licence|master|dut|bts|soft\s+skills)\b", block):
            continue

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)

        # Fallback regex for company name after dash (e.g. Ingénieure Data — Atlas Digital Solutions)
        if not block_orgs:
            company_dash = re.search(r"[—\-]\s*([A-Z][A-Za-z0-9\s&]+)", block)
            if company_dash:
                c_name = company_dash.group(1).strip()
                # Remove trailing parenthetical dates like (Mars 2025)
                c_name = re.sub(r"\(.*?\)", "", c_name).strip()
                if c_name and c_name.upper() not in ORG_BLACKLIST:
                    block_orgs.append(c_name)

        block_titles = [m.group(0).strip() for m in JOB_TITLE_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        if block_titles or block_orgs:
            entries.append({
                "poste": block_titles[0] if block_titles else None,
                "entreprise": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:300].strip(),
            })

    return entries


def _extract_education_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """Extract structured education entries."""
    if not text.strip():
        return []

    entries = []
    blocks = _split_into_education_blocks(text)

    for block in blocks:
        if len(block) < 8:
            continue

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)

        # School Regex Matcher Fallback
        school_match = SCHOOL_KEYWORDS.search(block)
        if school_match:
            school_name = school_match.group(0).strip()
            if not block_orgs or len(school_name) > len(block_orgs[0]):
                block_orgs = [school_name]

        block_diplomas = [m.group(0).strip() for m in DIPLOMA_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        if block_diplomas or block_orgs:
            entries.append({
                "diplome": block_diplomas[0] if block_diplomas else None,
                "etablissement": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:300].strip(),
            })

    return entries


def extract_tech_skills(text: str) -> List[str]:
    """Extract technical skills found anywhere in the CV text."""
    matches = TECH_SKILLS_PATTERNS.findall(text)
    unique_skills = []
    seen = set()
    for m in matches:
        clean = m.strip()
        upper = clean.upper()
        if upper not in seen:
            seen.add(upper)
            unique_skills.append(clean)
    return unique_skills


def extract_languages(text: str) -> List[Dict[str, str]]:
    """Extract spoken languages from text."""
    langs = []
    lang_matches = re.findall(r"(?i)\b(arabe|fran[çc]ais|anglais|espagnol|allemand|italien)\b(?:\s*:\s*([^\n,]+))?", text)
    for l_name, l_level in lang_matches:
        langs.append({
            "langue": l_name.capitalize(),
            "niveau": l_level.strip() if l_level else "Professionnel"
        })
    return langs


def extract_certifications(text: str) -> List[Dict[str, str]]:
    """Extract certifications from text."""
    certs = []
    cert_matches = re.findall(r"(?i)\b([A-Za-z0-9\s\-\(\)]+Certificate[^\n]*|[A-Za-z0-9\s\-\(\)]+Certification[^\n]*)", text)
    for c in cert_matches:
        certs.append({
            "label": c.strip(),
            "date": None
        })
    return certs


def _split_sections(text: str) -> Dict[str, str]:
    """Split CV text into sections based on heading keywords."""
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
        elif re.search(r"(?i)^(?:soft\s+skills|portfolio|activit[eé]s?\s+parascolaires?| centres?\s+d.int[eé]r[eê]t)", l):
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

    # 1. Split text into sections
    sections = _split_sections(text)

    # 2. Extract experiences & formations
    experiences = _extract_experience_entries(sections["experience"], nlp)
    formations = _extract_education_entries(sections["education"], nlp)

    # Fallbacks if sections were not cleanly demarcated
    if not experiences:
        experiences = _extract_experience_entries(text, nlp)
    if not formations:
        formations = _extract_education_entries(text, nlp)

    # 3. Extract tech skills, languages, and certifications
    tech_skills = extract_tech_skills(text)
    languages = extract_languages(text)
    certifications = extract_certifications(text)

    return {
        "experiences": experiences,
        "formations": formations,
        "competences": {
            "techniques": tech_skills,
            "langues": languages,
            "certifications": certifications
        }
    }
