"""
Tests for LLM Enrichment Service & Security Gate (Phase 6 / Day 6)
Verifies profile summary generation and asserts that raw PII injection
blocks the API call prior to execution.
"""
import pytest
from app.services.pii_detector import detect_pii
from app.services.pii_masker import mask_pii
from app.services.llm_enrichment import (
    generate_profile_summary,
    assert_no_raw_pii_before_llm,
    SecurityComplianceError,
    DefaultMockLLMClient,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE
)


class MockTrackingLLMClient:
    """Mock client to track call counts and verify API call blocking."""
    def __init__(self):
        self.call_count = 0
        self.last_system_prompt = None
        self.last_user_prompt = None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return "Résumé de profil généré avec succès par l'IA."


def test_generate_profile_summary_success():
    """Verify that clean masked text successfully passes the security gate and generates a summary."""
    raw_cv = """
    Karim Mansouri
    Développeur Python Senior
    Email: karim.mansouri@tech.ma
    Téléphone: +212 661234567
    CIN: AB123456
    Adresse: Casablanca
    Date de naissance: 15/05/1990
    LinkedIn: linkedin.com/in/karim-mansouri

    Expérience Professionnelle
    5 ans d'expérience en développement d'API FastAPI et architecture Cloud.
    
    Formation
    Diplôme d'Ingénieur en Informatique.
    """
    
    # Phase 4 PII Masking
    masked_text, pii_data = mask_pii(raw_cv)
    
    # Mock LLM client
    client = MockTrackingLLMClient()
    
    # Phase 6 LLM Enrichment
    summary = generate_profile_summary(masked_text, pii_data, client=client)
    
    # Assertions
    assert summary is not None
    assert len(summary) > 0
    assert client.call_count == 1, "API call should execute exactly once for clean masked text"
    assert "[NOM_1]" in client.last_user_prompt
    assert "karim.mansouri@tech.ma" not in client.last_user_prompt
    assert "+212 661234567" not in client.last_user_prompt


def test_security_gate_blocks_api_call_when_raw_pii_present():
    """
    SECURITY GATE TEST:
    Intentionally injects raw PII (raw email and raw phone) into the text passed to LLM.
    Asserts SecurityComplianceError is raised AND client.call_count remains 0 (API call BLOCKED).
    """
    raw_cv = """
    Hassan Benali
    Email: hassan.benali@domain.ma
    Tel: 0612345678
    """
    
    pii_data = detect_pii(raw_cv)
    masked_text, _ = mask_pii(raw_cv, pii_data)
    
    # Intentionally corrupt the masked_text by appending unmasked raw email
    leaked_masked_text = masked_text + "\nRAW EMAIL LEAK: hassan.benali@domain.ma"
    
    client = MockTrackingLLMClient()
    
    # Expect SecurityComplianceError
    with pytest.raises(SecurityComplianceError) as exc_info:
        generate_profile_summary(leaked_masked_text, pii_data, client=client)
        
    # Assert exception details
    assert "SECURITY AUDIT FAILURE" in str(exc_info.value)
    assert "hassan.benali@domain.ma" in str(exc_info.value)
    
    # CRITICAL: Verify the LLM API call was NEVER executed
    assert client.call_count == 0, "API call MUST be blocked (0 calls) when raw PII is detected!"


def test_case_insensitive_pii_leak_prevention():
    """Verifies that case-insensitive PII leaks (e.g. UPPERCASE email) are also caught and blocked."""
    pii_data = {
        "email": {"value": "test.user@company.com", "masked": True},
        "nom_complet": {"value": "Amine Tazi", "masked": True}
    }
    
    # Inject uppercase variant of the raw name
    leaked_text = "Candidat: AMINE TAZI - Développeur Web"
    
    client = MockTrackingLLMClient()
    
    with pytest.raises(SecurityComplianceError) as exc_info:
        generate_profile_summary(leaked_text, pii_data, client=client)
        
    assert "Case-insensitive raw PII" in str(exc_info.value)
    assert client.call_count == 0, "API call MUST be blocked on case-insensitive leak!"


def test_assert_no_raw_pii_direct_helper():
    """Directly tests the assert_no_raw_pii_before_llm assertion helper function."""
    pii_data = {
        "telephone": {"value": "+212600000000", "masked": True}
    }
    
    # Clean text should pass without exception
    assert_no_raw_pii_before_llm("CV Texte anonymisé avec [TELEPHONE_1]", pii_data)
    
    # Leaked text should raise SecurityComplianceError
    with pytest.raises(SecurityComplianceError):
        assert_no_raw_pii_before_llm("Contact direct +212600000000", pii_data)
