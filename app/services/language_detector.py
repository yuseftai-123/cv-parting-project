"""
Language Detector Service
Detects whether text is French (fr), English (en), or Arabic (ar).
"""
import re

# Arabic character range regex
ARABIC_REGEX = re.compile(r'[\u0600-\u06FF]')

# Distinctive French and English words/patterns
FRENCH_KEYWORDS = {
    "et", "du", "de", "des", "le", "la", "les", "en", "dans", "pour",
    "par", "sur", "avec", "expérience", "professionnelle", "formation",
    "compétences", "ingénieur", "développeur", "projet", "gestion"
}

ENGLISH_KEYWORDS = {
    "and", "the", "of", "in", "to", "for", "with", "on", "at", "by",
    "experience", "professional", "education", "skills", "engineer",
    "developer", "project", "management", "summary", "work"
}

def detect_language(text: str) -> str:
    """
    Detects the primary language of the raw text.
    Returns: 'ar', 'fr', or 'en' (defaults to 'fr').
    """
    if not text or not text.strip():
        return "fr"

    # Check for Arabic script characters
    arabic_chars = len(ARABIC_REGEX.findall(text))
    total_chars = len(text)
    if arabic_chars / max(total_chars, 1) > 0.1:
        return "ar"

    # Tokenize words for French / English scoring
    words = re.findall(r'\b[a-zA-Zà-ÿÀ-Ÿ]+\b', text.lower())
    if not words:
        return "fr"

    fr_score = sum(1 for w in words if w in FRENCH_KEYWORDS)
    en_score = sum(1 for w in words if w in ENGLISH_KEYWORDS)

    if en_score > fr_score:
        return "en"

    return "fr"
