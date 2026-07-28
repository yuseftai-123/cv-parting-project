"""
NER Extractor Service (Layer 2) - Non-PII Entity Extraction
Uses spaCy fr_core_news_lg for ORG/DATE entities and regex patterns for job titles & diplomas.
French and English only (per MVP scope).
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
            _nlp_en = False  # sentinel: tried and failed
    return _nlp_en if _nlp_en is not False else None


# ---------------------------------------------------------------------------
# Section-splitting keywords
# ---------------------------------------------------------------------------
EXPERIENCE_HEADERS = re.compile(
    r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience"
    r"|employment\s+history|parcours\s+professionnel)",
    re.MULTILINE,
)

EDUCATION_HEADERS = re.compile(
    r"(?i)^(?:formations?|[eé]ducation|education|academic\s+background"
    r"|dipl[oô]mes?|qualifications?|parcours\s+acad[eé]mique)",
    re.MULTILINE,
)

# Any section header (used to find the boundary of a section)
ANY_SECTION_HEADER = re.compile(
    r"(?i)^(?:exp[eé]riences?\s*professionnelles?|work\s+experience|professional\s+experience"
    r"|employment\s+history|parcours\s+professionnel"
    r"|formations?|[eé]ducation|education|academic\s+background"
    r"|dipl[oô]mes?|qualifications?|parcours\s+acad[eé]mique"
    r"|comp[eé]tences?|skills|langues|languages|centres?\s+d.int[eé]r[eê]t"
    r"|hobbies|loisirs|projets?|projects?|certifications?"
    r"|r[eé]f[eé]rences?|references|profil|profile|summary|objectif)",
    re.MULTILINE,
)

# ---------------------------------------------------------------------------
# Job title patterns (regex-based, no fine-tuning)
# ---------------------------------------------------------------------------
# Note: Using double-quoted raw strings to avoid issues with single quotes
APOS = "['\u2019]"  # matches ASCII apostrophe or Unicode right single quote

JOB_TITLE_PATTERNS = re.compile(
    r"(?i)\b("
    # French titles
    r"ing[eé]nieur(?:\s+(?:d" + APOS + r"?[eé]tat|en|informatique|logiciel|r[eé]seaux|civil|industriel))?"
    r"|d[eé]veloppeur(?:\s+(?:web|full\s*stack|front[\s-]*end|back[\s-]*end|mobile|java|python|\.net))?"
    r"|chef\s+de\s+(?:projet|produit|d[eé]partement)"
    r"|responsable\s+(?:technique|informatique|qualit[eé]|commercial|rh|marketing)"
    r"|directeur(?:\s+(?:technique|g[eé]n[eé]ral|commercial|financier|artistique))?"
    r"|technicien(?:\s+(?:sup[eé]rieur|informatique|r[eé]seaux|maintenance))?"
    r"|consultant(?:\s+(?:fonctionnel|technique|s[eé]nior|junior|it|sap|bi))?"
    r"|analyste(?:\s+(?:programmeur|fonctionnel|de\s+donn[eé]es|financier|business))?"
    r"|administrateur(?:\s+(?:syst[èe]me|base\s+de\s+donn[eé]es|r[eé]seaux?))?"
    r"|comptable|auditeur|juriste|avoca?t"
    r"|gestionnaire(?:\s+de\s+(?:stock|paie|projet))?"
    r"|assistant(?:e)?(?:\s+(?:de\s+direction|administratif|commercial|rh))?"
    r"|stagiaire(?:\s+(?:en|p[eé]dagogique))?"
    r"|architecte(?:\s+(?:logiciel|solution|cloud|si))?"
    # English titles
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
    # French diplomas
    r"baccalaur[eé]at|bac(?:\s*\+\s*\d)?"
    r"|licence(?:\s+professionnelle)?|master(?:\s+(?:sp[eé]cialis[eé]|recherche|professionnel))?"
    r"|doctorat|th[èe]se"
    r"|dipl[oô]me\s+(?:d" + APOS + r"?ing[eé]nieur|d" + APOS + r"?[eé]tat|universitaire)"
    r"|dut|deug|deust|bts|cpge"
    r"|ing[eé]nieur\s+d" + APOS + r"?[eé]tat"
    # English diplomas
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
# Date extraction helper
# ---------------------------------------------------------------------------
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

    # Take the first match as the primary date range
    first = matches[0].strip()
    # Check if it contains a range separator
    range_sep = re.search(r"[-\u2013\u2014/\u00e0]", first)
    if range_sep:
        parts = re.split(r"\s*[-\u2013\u2014/\u00e0]\s*", first, maxsplit=1)
        if len(parts) == 2:
            result["date_debut"] = parts[0].strip()
            result["date_fin"] = parts[1].strip()
            return result

    # If just a single year, treat it as date_debut
    result["date_debut"] = first
    if len(matches) > 1:
        result["date_fin"] = matches[1].strip()
    return result


# ---------------------------------------------------------------------------
# Section splitter
# ---------------------------------------------------------------------------
def _split_sections(text: str) -> Dict[str, str]:
    """
    Split CV text into sections based on heading keywords.
    Returns dict with keys: 'experience', 'education', 'other'.
    """
    sections = {"experience": "", "education": "", "other": ""}

    # Find all section header positions
    all_headers = list(ANY_SECTION_HEADER.finditer(text))

    if not all_headers:
        # No headers found - treat entire text as 'other'
        sections["other"] = text
        return sections

    # Add text before the first header as 'other' (usually contact info)
    if all_headers[0].start() > 0:
        sections["other"] = text[: all_headers[0].start()]

    for i, match in enumerate(all_headers):
        # Determine the end of this section (start of next header or end of text)
        start = match.end()
        end = all_headers[i + 1].start() if i + 1 < len(all_headers) else len(text)
        section_text = text[start:end].strip()
        header_text = match.group(0).strip()

        if EXPERIENCE_HEADERS.match(header_text):
            sections["experience"] += "\n" + section_text
        elif EDUCATION_HEADERS.match(header_text):
            sections["education"] += "\n" + section_text
        else:
            sections["other"] += "\n" + section_text

    return sections


# ---------------------------------------------------------------------------
# Entity extraction from a section block
# ---------------------------------------------------------------------------
def _extract_experience_entries(text: str, nlp) -> List[Dict[str, Any]]:
    """
    Extract experience entries from a text block.
    Uses spaCy for ORG detection, regex for job titles and dates.
    """
    if not text.strip():
        return []

    entries = []
    doc = nlp(text[:100000])  # Limit text length for performance

    # Collect all ORG entities from spaCy
    org_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]

    # Collect all job titles from regex
    job_titles = [m.group(0).strip() for m in JOB_TITLE_PATTERNS.finditer(text)]

    # Split text into paragraph blocks to try to group entries
    blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in blocks if b.strip()]

    if not blocks:
        # Single-block fallback
        dates = _extract_date_range(text)
        entries.append({
            "poste": job_titles[0] if job_titles else None,
            "entreprise": org_entities[0] if org_entities else None,
            "date_debut": dates["date_debut"],
            "date_fin": dates["date_fin"],
            "description": text[:200].strip() if text else None,
        })
        return entries

    for block in blocks:
        if len(block) < 10:
            continue

        # Run NER on this block
        block_doc = nlp(block[:10000])
        block_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
        block_titles = [m.group(0).strip() for m in JOB_TITLE_PATTERNS.finditer(block)]
        block_dates = _extract_date_range(block)

        # Only create an entry if we found at least a job title or an org
        if block_titles or block_orgs:
            entries.append({
                "poste": block_titles[0] if block_titles else None,
                "entreprise": block_orgs[0] if block_orgs else None,
                "date_debut": block_dates["date_debut"],
                "date_fin": block_dates["date_fin"],
                "description": block[:200].strip(),
            })

    # If we found no structured entries, create one from overall findings
    if not entries and (job_titles or org_entities):
        dates = _extract_date_range(text)
        entries.append({
            "poste": job_titles[0] if job_titles else None,
            "entreprise": org_entities[0] if org_entities else None,
            "date_debut": dates["date_debut"],
            "date_fin": dates["date_fin"],
            "description": text[:200].strip(),
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
    doc = nlp(text[:100000])

    # Collect ORG entities (schools, universities)
    org_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]

    # Collect diploma patterns
    diplomas = [m.group(0).strip() for m in DIPLOMA_PATTERNS.finditer(text)]

    # Split into blocks
    blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in blocks if b.strip()]

    if not blocks:
        dates = _extract_date_range(text)
        entries.append({
            "diplome": diplomas[0] if diplomas else None,
            "etablissement": org_entities[0] if org_entities else None,
            "date_debut": dates["date_debut"],
            "date_fin": dates["date_fin"],
            "description": text[:200].strip() if text else None,
        })
        return entries

    for block in blocks:
        if len(block) < 10:
            continue

        block_doc = nlp(block[:10000])
        block_orgs = [ent.text.strip() for ent in block_doc.ents if ent.label_ == "ORG"]
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

    # Fallback
    if not entries and (diplomas or org_entities):
        dates = _extract_date_range(text)
        entries.append({
            "diplome": diplomas[0] if diplomas else None,
            "etablissement": org_entities[0] if org_entities else None,
            "date_debut": dates["date_debut"],
            "date_fin": dates["date_fin"],
            "description": text[:200].strip(),
        })

    return entries


# ---------------------------------------------------------------------------
# Main public API
# ---------------------------------------------------------------------------
def extract_ner(text: str) -> Dict[str, Any]:
    """
    Main entry point for NER extraction (Layer 2).
    
    Takes raw CV text (already PII-masked), extracts non-PII entities:
    - experiences: job titles, companies, date ranges
    - formations: diplomas, schools, date ranges
    
    Returns dict matching the spec's experiences/formations structure.
    """
    nlp = _get_fr_model()
    if nlp is None:
        logger.error("No spaCy model available. Cannot run NER extraction.")
        return {"experiences": [], "formations": []}

    # 1. Split text into sections
    sections = _split_sections(text)

    # 2. Extract experiences
    experiences = _extract_experience_entries(sections["experience"], nlp)

    # 3. Extract formations
    formations = _extract_education_entries(sections["education"], nlp)

    # 4. If no experiences found in experience section, also try the 'other' section
    #    (handles CVs where experiences appear before any section header)
    if not experiences and sections["other"].strip():
        logger.info("No experience section found; trying 'other' section")
        experiences = _extract_experience_entries(sections["other"], nlp)

    # 5. If still nothing, try extracting from the full text
    if not experiences and not formations:
        logger.info("No section headers found; attempting full-text extraction")
        experiences = _extract_experience_entries(text, nlp)
        formations = _extract_education_entries(text, nlp)

    return {
        "experiences": experiences,
        "formations": formations,
    }
