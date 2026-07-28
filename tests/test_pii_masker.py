import pytest
from app.services.pii_detector import detect_pii
from app.services.pii_masker import mask_pii

def test_mask_pii_token_replacement():
    sample_text = """
    Fatima Idrissi
    Software Engineer
    Email: fatima.idrissi@gmail.com
    Tel: +212 612345678
    CIN: AB654321
    Née le 10/08/1997
    Adresse: Casablanca
    LinkedIn: linkedin.com/in/fatima-idrissi
    """
    
    masked_text, pii_data = mask_pii(sample_text)
    
    # Assert mask tokens were inserted into text
    assert "[NOM_1]" in masked_text
    assert "[EMAIL_1]" in masked_text
    assert "[TELEPHONE_1]" in masked_text
    assert "[CIN_1]" in masked_text
    assert "[DATE_NAISSANCE_1]" in masked_text
    assert "[ADRESSE_1]" in masked_text
    assert "[LINKEDIN_GITHUB_1]" in masked_text
    
    # Assert pii_data flags are set to masked: True
    assert pii_data["nom_complet"]["masked"] is True
    assert pii_data["email"]["masked"] is True

def test_compliance_gate_zero_pii_absence():
    """
    COMPLIANCE GATE TEST:
    Asserts absolute absence of PII raw values in the masked output.
    Instead of just checking if a mask token exists, this test explicitly checks
    that ZERO raw PII strings can be found anywhere inside the masked text.
    """
    resumes = [
        """
        Mehdi El Amrani
        Developpeur Fullstack
        Email: mehdi.amrani@company.ma
        Phone: 0612345678
        CIN: CD987654
        Né le 25/12/1992
        Ville: Rabat, 10000
        Github: github.com/mehdiamrani
        """,
        """
        Sophia Alami
        Data Scientist
        Contact: sophia.alami@domain.com
        Mobile: +212-700000000
        Carte d'identité: BK123456
        Born: 1999-04-15
        Location: Marrakech
        LinkedIn: linkedin.com/in/sophia-alami
        """
    ]
    
    for text in resumes:
        pii_data = detect_pii(text)
        masked_text, updated_pii = mask_pii(text, pii_data)
        
        # --- EXACT ASSERTION LOGIC FOR ABSENCE OF PII ---
        for field_name, field_info in pii_data.items():
            raw_value = field_info.get("value")
            if raw_value:
                # 1. Assert raw value string is NOT present anywhere in the masked output
                assert raw_value not in masked_text, (
                    f"Compliance Failure! Raw PII value '{raw_value}' for field '{field_name}' "
                    f"was found inside masked text:\n{masked_text}"
                )
                
                # 2. Case-insensitive check as an extra safety gate
                assert raw_value.lower() not in masked_text.lower(), (
                    f"Compliance Failure! Case-insensitive raw PII '{raw_value}' "
                    f"found in masked text."
                )
