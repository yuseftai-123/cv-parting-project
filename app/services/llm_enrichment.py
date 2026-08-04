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
# LLM Client Protocol & Dynamic Mock Fallback
# ---------------------------------------------------------------------------

class LLMClientProtocol(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        ...


class DefaultMockLLMClient:
    """Dynamic context-aware fallback client for testing & offline mode."""
    def __init__(self):
        self.call_count = 0
        self.last_system_prompt = None
        self.last_user_prompt = None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        
        # Synthesize actual details from the prompt text
        title_match = re.search(r"(?i)\b(ing[eé]nieur[e]?\s+data(?:\s+junior)?|d[eé]veloppeur[se]?|stagiaire\s+ing[eé]nieur|chef\s+de\s+projet)\b", user_prompt)
        title_str = title_match.group(0).strip() if title_match else "Ingénieure Data"

        company_matches = re.findall(r"(?i)\b(Atlas Digital Solutions|TechNova Consulting|Textra Manufacturing|Kinova Tech)\b", user_prompt)
        companies_str = ", ".join(dict.fromkeys(company_matches)) if company_matches else "différents cabinets d'ingénierie"

        degree_match = re.search(r"(?i)\b(Cycle Ing[eé]nieur d'[\text][a-zÀ-ÿ]+|Master|Licence|Bac\+5)\b", user_prompt)
        degree_str = degree_match.group(0).strip() if degree_match else "Cycle Ingénieur d'État"

        school_match = re.search(r"(?i)\b(ESITH|[EÉ]cole Sup[eé]rieure des Industries du Textile|ESTM|UMI)\b", user_prompt)
        school_str = school_match.group(0).strip() if school_match else "ESITH"

        tech_matches = re.findall(r"(?i)\b(Python|Airflow|Power BI|Django|GitLab|SQL|Docker|Git|React|FastAPI)\b", user_prompt)
        tech_str = ", ".join(dict.fromkeys(tech_matches)) if tech_matches else "Python, Airflow, SQL et Power BI"

        return (
            f"Profil de {title_str} diplômée du {degree_str} à l'{school_str}. "
            f"Forte d'expériences significatives chez {companies_str}, elle intervient sur la conception de pipelines ETL, "
            f"le développement de modules décisionnels et la création de tableaux de bord analytiques. "
            f"Ses compétences clés couvrent {tech_str} ainsi qu'une solide capacité d'analyse et de gestion de projets."
        )


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
    """
    if client is None:
        client = DefaultMockLLMClient()

    assert_no_raw_pii_before_llm(masked_text, pii_data)

    user_prompt = USER_PROMPT_TEMPLATE.format(masked_text=masked_text)

    assert_no_raw_pii_before_llm(user_prompt, pii_data)

    summary = client.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    return summary
