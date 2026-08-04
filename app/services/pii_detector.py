import re

# Moroccan cities dictionary for address detection
MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Marrakech", "Marrakesh", "Fès", "Fes", "Tanger", "Tangier",
    "Agadir", "Meknès", "Meknes", "Oujda", "Kénitra", "Kenitra", "Tétouan", "Tetouan",
    "Safi", "Mohammedia", "Khouribga", "El Jadida", "Nador", "Taza", "Settat",
    "Salé", "Sale", "Temara", "Témara", "Khenifra", "Ksar El Kebir", "Larache",
    "Guelmim", "Berrechid", "Wazzan", "Errachidia", "Essaouira", "Ifrane"
]

# Compiled Regex Patterns
PHONE_REGEX = re.compile(r'(?:\+212|0)[\s.\-]*[567](?:[\s.\-]?\d){8}\b')
EMAIL_REGEX = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
CIN_REGEX = re.compile(r'\b[A-Z]{1,2}\d{5,6}\b')
DOB_REGEX = re.compile(
    r'(?i)(?:n[eé](?:e)?|born|date\s+de\s+naissance|d\.o\.b\.?|naissance)\s*(?:le|on|:)?\s*'
    r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4}|\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})'
)
LINKEDIN_GITHUB_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?(?:linkedin\.com/in|github\.com)/[a-zA-Z0-9_\-]+/?',
    re.IGNORECASE
)
NAME_CONTEXT_REGEX = re.compile(
    r'(?i)(?:nom|full\s+name|nom\s+complet|candidat(?:e)?)\s*[:\-]\s*([A-ZÀ-ÿ][a-zà-ÿA-ZÀ-ÿ\'-]+(?:[ \t]+[A-ZÀ-ÿ][a-zà-ÿA-ZÀ-ÿ\'-]+)+)'
)

def detect_phone(text: str) -> dict:
    match = PHONE_REGEX.search(text)
    if match:
        val = match.group(0).strip()
        confidence = 0.98 if val.startswith("+212") else 0.95
        return {"value": val, "masked": False, "confidence": confidence}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_email(text: str) -> dict:
    match = EMAIL_REGEX.search(text)
    if match:
        return {"value": match.group(0).strip(), "masked": False, "confidence": 0.99}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_cin(text: str) -> dict:
    matches = CIN_REGEX.finditer(text)
    for match in matches:
        val = match.group(0).strip()
        if not re.search(r'(?i)(?:code|id|ref|ver|v)\s*:' + re.escape(val), text):
            return {"value": val, "masked": False, "confidence": 0.96}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_dob(text: str) -> dict:
    match = DOB_REGEX.search(text)
    if match:
        val = match.group(1).strip()
        return {"value": val, "masked": False, "confidence": 0.92}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_linkedin_github(text: str) -> dict:
    match = LINKEDIN_GITHUB_REGEX.search(text)
    if match:
        return {"value": match.group(0).strip(), "masked": False, "confidence": 0.98}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_address(text: str) -> dict:
    cities_pattern = r'(?i)\b(?:' + '|'.join(re.escape(c) for c in MOROCCAN_CITIES) + r')\b'
    city_match = re.search(cities_pattern, text)
    
    if city_match:
        city_name = city_match.group(0)
        postal_match = re.search(r'\b\d{5}\b', text)
        address_str = city_name
        if postal_match:
            address_str = f"{city_name}, {postal_match.group(0)}"
            confidence = 0.92
        else:
            confidence = 0.87
        return {"value": address_str, "masked": False, "confidence": confidence}
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_name(text: str) -> dict:
    match = NAME_CONTEXT_REGEX.search(text)
    if match:
        return {"value": match.group(1).strip(), "masked": False, "confidence": 0.98}
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        first_line = lines[0]
        # Match 2-4 capitalized or uppercase words (e.g., Salma EL AMRANI, Youssef TAICHA)
        if re.match(r'^[A-ZÀ-ÿ][A-Za-zÀ-ÿ\'-]+\s+(?:[A-ZÀ-ÿ][A-Za-zÀ-ÿ\'-]+\s*){1,3}$', first_line):
            return {"value": first_line, "masked": False, "confidence": 0.85}
            
    return {"value": None, "masked": False, "confidence": 0.0}

def detect_pii(text: str) -> dict:
    return {
        "nom_complet": detect_name(text),
        "email": detect_email(text),
        "telephone": detect_phone(text),
        "adresse": detect_address(text),
        "date_naissance": detect_dob(text),
        "cin": detect_cin(text),
        "linkedin_github": detect_linkedin_github(text)
    }
