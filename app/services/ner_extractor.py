"""
NER Extractor Service (Layer 2) - Non-PII Entity Extraction
Uses spaCy fr_core_news_lg for ORG/DATE entities and regex patterns for job titles & diplomas.
Enhanced Section Splitting & Blacklist Filtering.
"""
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# spaCy model loading (singleton)
# ---------------------------------------------------------------------------
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
            logger.warning(
                "fr_core_news_lg not installed. Run: python -m spacy download fr_core_news_lg"
            )
            _nlp_fr = None
    return _nlp_fr


def _get_en_model():
    """Lazy-load spaCy English model (en_core_web_sm) as optional fallback."""
    global _nlp_en
    if _nlp_en is None:
        try:
            import spacy
            _nlp_en = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model: en_core_web_sm")
        except OSError:
            logger.info("en_core_web_sm not available; using fr model for English text")
            _nlp_en = False  # sentinel
    return _nlp_en if _nlp_en is not False else None


# ---------------------------------------------------------------------------
# Blacklist for falsely recognized company names (ORG)
# ---------------------------------------------------------------------------
ORG_BLACKLIST = {
    "SOFT", "SOFT SKILLS", "SKILLS", "ACTIVITÉS", "PARASCOLAIRES", "PORTFOLIO",
    "ACADEMIQUES", "ACADÉMIQUES", "CLUB", "HUMANITAIRE", "COMPÉTENCES", "COMPETENCES",
    "LANGUES", "HOBBIES", "INTERETS", "INTÉRÊTS", "FORMATION", "FORMATIONS",
    "DIPLÔMES", "DIPLOMES", "PROJETS", "EXPERIENCES", "EXPÉRIENCES"
}


# ---------------------------------------------------------------------------
# Section-splitting keywords
# ---------------------------------------------------------------------------
EXPERIENCE_HEADERS = re.compile(
    r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience"
    r"|employment\s+history|parcours\s+professionnel|exp[eé]riences?)",
    re.MULTILINE,
)

EDUCATION_HEADERS = re.compile(
    r"(?i)^(?:formations?|[eé]ducation|education|academic\s+background"
    r"|dipl[oô]mes?|qualifications?|parcours\s+acad[eé]mique|activit[eé]s?\s+parascolaires?|[eé]tudes)",
    re.MULTILINE,
)

SKILLS_HEADERS = re.compile(
    r"(?i)^(?:comp[eé]tences?|skills|soft\s+skills|hard\s+skills|savoir-faire|langues|languages)",
    re.MULTILINE,
)

ANY_SECTION_HEADER = re.compile(
    r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience"
    r"|employment\s+history|parcours\s+professionnel|exp[eé]riences?"
    r"|formations?|[eé]ducation|education|academic\s+background"
    r"|dipl[oô]mes?|qualifications?|parcours\s+acad[eé]mique|activit[eé]s?\s+parascolaires?|[eé]tudes"
    r"|comp[eé]tences?|skills|soft\s+skills|hard\s+skills|savoir-faire|langues|languages|centres?\s+d.int[eé]r[eê]t"
    r"|hobbies|loisirs|projets?|projects?|portfolio|portfolio\s+acad[eé]miques?|certifications?"
    r"|r[eé]f[eé]rences?|references|profil|profile|summary|objectif)",
    re.MULTILINE,
)

# ---------------------------------------------------------------------------
# Job title patterns
# ---------------------------------------------------------------------------
APOS = "['\u2019]"

JOB_TITLE_PATTERNS = re.compile(
    r"(?i)\b("
    r"ing[eé]nieur(?:\s+(?:d" + APOS + r"?[eé]tat|en|informatique|logiciel|r[eé]seaux|civil|industriel))?"
    r"|d[eé]veloppeur(?:\s+(?:web|full\s*stack|front[\s-]*end|back[\s-]*end|mobile|java|python|\.net))?"
    r"|chef\s+de\s+(?:projet|produit|d[eé]partement)"
    r"|responsable\s+(?:technique|informatique|qualit[eé]|commercial|rh|marketing|de\s+l" + APOS + r"?infographie)"
    r"|directeur(?:\s+(?:technique|g[eé]n[eé]ral|commercial|financier|artistique))?"
    r"|technicien(?:\s+(?:sup[eé]rieur|informatique|r[eé]seaux|maintenance))?"
    r"|consultant(?:\s+(?:fonctionnel|technique|s[eé]nior|junior|it|sap|bi))?"
    r"|analyste(?:\s+(?:programmeur|fonctionnel|de\s+donn[eé]es|financier|business))?"
    r"|administrateur(?:\s+(?:syst[èe]me|base\s+de\s+donn[eé]es|r[eé]seaux?))?"
    r"|comptable|auditeur|juriste|avoca?t"
    r"|vice[\s-]*pr[eé]sident|pr[eé]sident"
    r"|gestionnaire(?:\s+de\s+(?:stock|paie|projet))?"
    r"|assistant(?:e)?(?:\s+(?:de\s+direction|administratif|commercial|rh))?"
    r"|stagiaire(?:\s+(?:en|p[eé]dagogique))?"
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

# ---------------------------------------------------------------------------
# Diploma / degree patterns
# ---------------------------------------------------------------------------
DIPLOMA_PATTERNS = re.compile(
    r"(?i)\b("
    r"baccalaur[eé]at|bac(?:\s*\+\s*\d)?"
    r"|licence(?:\s+professionnelle)?|master(?:\s+(?:sp[eé]cialis[eé]|recherche|professionnel))?"
    r"|doctorat|th[èe]se"
    r"|cycle\s+ing[eé]nieur(?:\s+d" + APOS + r"?[eé]tat)?"
    r"|dipl[oô]me\s+(?:d" + APOS + r"?ing[eé]nieur|d" + APOS + r"?[eé]tat|universitaire)"
    r"|dut|deug|deust|bts|cpge"
    r"|ing[eé]nieur\s+d" + APOS + r"?[eé]tat"
    r"|bachelor(?:" + APOS + r"?s)?(?:\s+(?:of\s+(?:science|arts|engineering)))?"
    r"|b\.?sc?\.?|b\.?a\.?|b\.?eng\.?"
    r"|master(?:" + APOS + r"?s)?(?:\s+(?:of\s+(?:science|arts|engineering|business)))?"
    r"|m\.?sc?\.?|m\.?a\.?|m\.?eng\.?|mba"
    r"|ph\.?d\.?|doctorate"
    r"|associate(?:" + APOS + r"?s)?\s+degree"
    r"|certificate|certification|diploma"
    r")\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Known Tech Stack Regex Extractor
# ---------------------------------------------------------------------------
TECH_SKILLS_PATTERNS = re.compile(
    r"(?i)\b("
    r"html5?|css3?|javascript|js|typescript|ts|python|java|c\+\+|c#|php|ruby|go|golang|rust|swift|kotlin"
    r"|react(?:\.js)?|vue(?:\.js)?|angular|node(?:\.js)?|express|fastapi|flask|django|spring\s+boot"
    r"|postgresql|postgres|mysql|sqlite|mongodb|redis|oracle|sql"
    r"|docker|kubernetes|aws|azure|gcp|git|github|gitlab|ci/cd"
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


def _split_sections(text: str) -> Dict[str, str]:
    """
    Split CV text into sections based on heading keywords.
    Returns dict with keys: 'experience', 'education', 'skills', 'other'.
    """
    sections = {"experience": "", "education": "", "skills": "", "other": ""}

    all_headers = list(ANY_SECTION_HEADER.finditer(text))

    if not all_headers:
        sections["other"] = text
        return sections

    if all_headers[0].start() > 0:
        sections["other"] = text[: all_headers[0].start()]

    for i, match in enumerate(all_headers):
        start = match.end()
        end = all_headers[i + 1].start() if i + 1 < len(all_headers) else len(text)
        section_text = text[start:end].strip()
        header_text = match.group(0).strip()

        if EXPERIENCE_HEADERS.match(header_text):
            sections["experience"] += "\n" + section_text
        elif EDUCATION_HEADERS.match(header_text):
            sections["education"] += "\n" + section_text
        elif SKILLS_HEADERS.match(header_text):
            sections["skills"] += "\n" + section_text
        else:
            sections["other"] += "\n" + section_text

    return sections


def _filter_orgs(org_list: List[str]) -> List[str]:
    """Filter out falsely recognized company names matching the blacklist."""
    valid_orgs = []
    for org in org_list:
        clean_org = org.strip().strip(":").strip()
        if clean_org and clean_org.upper() not in ORG_BLACKLIST and len(clean_org) > 2:
            valid_orgs.append(clean_org)
    return valid_orgs


def _extract_experience_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """
    Extract experience entries from a text block.
    Uses spaCy for ORG detection (filtered), regex for job titles and dates.
    """
    if not text.strip():
        return []

    entries = []
    blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in blocks if b.strip()]

    for block in blocks:
        if len(block) < 10:
            continue

        # Skip block if it is purely education/formation
        if re.search(r"(?i)\b(?:cycle\s+ing[eé]nieur|dipl[oô]me|baccalaur[eé]at|licence|master|dut|bts)\b", block):
            continue

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)
        block_titles = [m.group(0).strip() for m in JOB_TITLE_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        if block_titles or block_orgs:
            entries.append({
                "poste": block_titles[0] if block_titles else None,
                "entreprise": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:200].strip(),
            })

    return entries


def _extract_education_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """
    Extract education/formation entries from a text block.
    Uses spaCy for ORG (school names), regex for diploma keywords and dates.
    """
    if not text.strip():
        return []

    entries = []
    blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in blocks if b.strip()]

    for block in blocks:
        if len(block) < 10:
            continue

        block_doc = nlp(block[:10000])
        raw_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_orgs = _filter_orgs(raw_orgs)
        block_diplomas = [m.group(0).strip() for m in DIPLOMA_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        if block_diplomas or block_orgs:
            entries.append({
                "diplome": block_diplomas[0] if block_diplomas else None,
                "etablissement": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:200].strip(),
            })

    return entries


def extract_tech_skills(text: str) -> List[str]:
    """Extract technical skills found anywhere in the CV text."""
    matches = TECH_SKILLS_PATTERNS.findall(text)
    # Deduplicate while preserving order and proper capitalization
    unique_skills = []
    seen = set()
    for m in matches:
        clean = m.strip()
        upper = clean.upper()
        if upper not in seen:
            seen.add(upper)
            unique_skills.append(clean)
    return unique_skills


def extract_ner(text: str) -> Dict[str, Any]:
    """
    Main entry point for NER extraction (Layer 2).
    Extracts non-PII entities: experiences, formations, and technical skills.
    """
    nlp = _get_fr_model()
    if nlp is None:
        logger.error("No spaCy model available. Cannot run NER extraction.")
        return {"experiences": [], "formations": [], "competences": {"techniques": []}}

    # 1. Split text into sections
    sections = _split_sections(text)

    # 2. Extract experiences & formations
    experiences = _extract_experience_entries(sections["experience"], nlp)
    formations = _extract_education_entries(sections["education"], nlp)

    # 3. If section splitting missed entries, scan 'other' section
    if not formations and sections["other"].strip():
        formations = _extract_education_entries(sections["other"], nlp)

    if not experiences and sections["other"].strip():
        experiences = _extract_experience_entries(sections["other"], nlp)

    # 4. Extract tech skills from entire CV text
    tech_skills = extract_tech_skills(text)

    return {
        "experiences": experiences,
        "formations": formations,
        "competences": {
            "techniques": tech_skills,
            "langues": [],
            "certifications": []
        }
    }
