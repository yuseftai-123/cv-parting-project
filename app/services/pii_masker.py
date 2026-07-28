import re
from typing import Tuple, Dict, Any
from app.services.pii_detector import detect_pii

# Map PII dictionary keys to user-friendly token prefixes
TOKEN_MAP = {
    "nom_complet": "NOM",
    "email": "EMAIL",
    "telephone": "TELEPHONE",
    "adresse": "ADRESSE",
    "date_naissance": "DATE_NAISSANCE",
    "cin": "CIN",
    "linkedin_github": "LINKEDIN_GITHUB"
}

def mask_pii(text: str, pii_data: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Replaces all detected PII values in `text` with placeholder tokens (e.g. [NOM_1], [EMAIL_1]).
    
    If `pii_data` is not provided, automatically calls `detect_pii(text)`.
    Returns a tuple of (masked_text, updated_pii_data) where detected PII fields
    have 'masked' set to True.
    """
    if pii_data is None:
        pii_data = detect_pii(text)
        
    masked_text = text
    token_counters: Dict[str, int] = {}
    
    for field, token_prefix in TOKEN_MAP.items():
        field_info = pii_data.get(field)
        if field_info and field_info.get("value"):
            raw_value = str(field_info["value"]).strip()
            if not raw_value:
                continue
                
            # Increment token index for this category
            token_counters[token_prefix] = token_counters.get(token_prefix, 0) + 1
            token = f"[{token_prefix}_{token_counters[token_prefix]}]"
            
            # Replace raw value in text (case-insensitive where applicable)
            # Use re.escape to handle special regex characters in the raw value
            pattern = re.compile(re.escape(raw_value), re.IGNORECASE)
            masked_text = pattern.sub(token, masked_text)
            
            # Update PII metadata record
            field_info["masked"] = True
            field_info["mask_token"] = token

    return masked_text, pii_data
