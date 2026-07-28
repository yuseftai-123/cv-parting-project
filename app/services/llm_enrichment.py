"""
LLM Enrichment Service (Layer 3) — Profile Summary Generation (SF-06)

Provides profile summary generation using ONLY PII-masked text.
Includes a pre-dispatch security assertion gate that physically blocks transmission
and halts execution if any raw PII value is detected prior to sending.
"""
import re
import logging
from typing import Dict, Any, Optional, Protocol

logger = logging.getLogger(__name__)


class SecurityComplianceError(Exception):
    """Raised when raw PII is detected in data bound for an external LLM API call."""
    pass


# ---------------------------------------------------------------------------
# Exact Prompt Templates (SF-06)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "Vous êtes un assistant RH expert. Votre rôle est de générer un résumé "
    "professionnel synthétique à partir du CV anonymisé fourni. N'inventez aucune "
    "information et respectez strictement l'anonymat du candidat."
)

USER_PROMPT_TEMPLATE = """Voici le texte d'un CV anonymisé (les données personnelles ont été remplacées par des balises comme [NOM_1], [EMAIL_1]) :

---
{masked_text}
---

Veuillez générer un résumé professionnel synthétique en 3 à 4 phrases résumant le profil du candidat, ses compétences clés, son expérience principale et sa formation."""


# ---------------------------------------------------------------------------
# Pre-Dispatch Security Assertion Gate
# ---------------------------------------------------------------------------

def assert_no_raw_pii_before_llm(payload_text: str, pii_data: Dict[str, Any]) -> None:
    """
    CRITICAL SECURITY GATE:
    Inspects payload_text (the prompt bound for the LLM) against all raw PII values
    stored in pii_data.

    If ANY raw PII string is present anywhere inside payload_text (exact or case-insensitive),
    raises SecurityComplianceError IMMEDIATELY, preventing the API call from executing.
    """
    if not pii_data:
        return

    for field_name, field_info in pii_data.items():
        if not isinstance(field_info, dict):
            continue
            
        raw_val = field_info.get("value")
        if not raw_val:
            continue
            
        raw_str = str(raw_val).strip()
        # Ignore extremely short strings (e.g. single digit or character) to avoid false positives
        if len(raw_str) < 3:
            continue

        # 1. Exact string search
        if raw_str in payload_text:
            err_msg = (
                f"SECURITY AUDIT FAILURE: Raw PII value '{raw_str}' for field '{field_name}' "
                f"was detected in text bound for LLM. API call BLOCKED."
            )
            logger.critical(err_msg)
            raise SecurityComplianceError(err_msg)

        # 2. Case-insensitive search
        if raw_str.lower() in payload_text.lower():
            err_msg = (
                f"SECURITY AUDIT FAILURE: Case-insensitive raw PII '{raw_str}' for field "
                f"'{field_name}' was detected in text bound for LLM. API call BLOCKED."
            )
            logger.critical(err_msg)
            raise SecurityComplianceError(err_msg)


# ---------------------------------------------------------------------------
# LLM Client Protocol & Mock Fallback
# ---------------------------------------------------------------------------

class LLMClientProtocol(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        ...


class DefaultMockLLMClient:
    """Deterministic fallback client for testing & offline mode."""
    def __init__(self):
        self.call_count = 0
        self.last_system_prompt = None
        self.last_user_prompt = None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return (
            "Profil professionnel qualifié avec une solide expérience technique. "
            "Le candidat démontre une expertise en développement logiciel et gestion de projets. "
            "Titulaire d'un diplôme supérieur en informatique, il présente un parcours adapté "
            "aux exigences des postes de haut niveau."
        )


# ---------------------------------------------------------------------------
# Profile Summary Generator API (SF-06)
# ---------------------------------------------------------------------------

def generate_profile_summary(
    masked_text: str,
    pii_data: Dict[str, Any],
    client: Optional[LLMClientProtocol] = None
) -> str:
    """
    Generates a profile summary from PII-masked text (SF-06).
    
    1. Runs pre-dispatch security assertion on `masked_text`.
    2. Constructs the final prompt string.
    3. Runs pre-dispatch security assertion on the formatted prompt string.
    4. Invokes the LLM client ONLY if both security assertions pass.
    
    Raises `SecurityComplianceError` if any raw PII leaks into the input.
    """
    if client is None:
        client = DefaultMockLLMClient()

    # Gate Check 1: Check masked_text before prompt construction
    assert_no_raw_pii_before_llm(masked_text, pii_data)

    # Construct user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(masked_text=masked_text)

    # Gate Check 2: Check complete compiled prompt string
    assert_no_raw_pii_before_llm(user_prompt, pii_data)

    # Dispatch to LLM (executes ONLY if checks above succeed)
    summary = client.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    return summary
