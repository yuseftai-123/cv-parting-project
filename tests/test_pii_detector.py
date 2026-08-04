import pytest
from app.services.pii_detector import (
    detect_phone,
    detect_email,
    detect_cin,
    detect_dob,
    detect_linkedin_github,
    detect_address,
    detect_name,
    detect_pii
)

# --- Phone Number Tests ---
def test_detect_phone_valid():
    text1 = "Contact: +212 612345678"
    res1 = detect_phone(text1)
    assert res1["value"] == "+212 612345678"
    assert res1["confidence"] == 0.98

    text2 = "Appelez le 0612345678 pour me contacter"
    res2 = detect_phone(text2)
    assert res2["value"] == "0612345678"
    assert res2["confidence"] == 0.95

    text3 = "Fixe: 0522-123456"
    res3 = detect_phone(text3)
    assert res3["value"] == "0522-123456"

    text4 = "Mobile: +212-700000000"
    res4 = detect_phone(text4)
    assert res4["value"] == "+212-700000000"

def test_detect_phone_invalid():
    # Number starting with 01 (not Moroccan 05/06/07)
    text = "Tel: 0123456789"
    res = detect_phone(text)
    assert res["value"] is None
    assert res["confidence"] == 0.0

# --- Email Tests ---
def test_detect_email_valid():
    text1 = "Email me at john.doe@domain.ma for queries"
    res1 = detect_email(text1)
    assert res1["value"] == "john.doe@domain.ma"
    assert res1["confidence"] == 0.99

    text2 = "Contact: yassine.el-amrani+test@company.co.ma"
    res2 = detect_email(text2)
    assert res2["value"] == "yassine.el-amrani+test@company.co.ma"

def test_detect_email_invalid():
    text = "Contact: john.doe@domain"
    res = detect_email(text)
    assert res["value"] is None

# --- CIN (National ID) Tests ---
def test_detect_cin_valid():
    text1 = "CIN: AB123456"
    res1 = detect_cin(text1)
    assert res1["value"] == "AB123456"
    assert res1["confidence"] == 0.96

    text2 = "Carte Nationale: C12345"
    res2 = detect_cin(text2)
    assert res2["value"] == "C12345"

def test_detect_cin_invalid():
    text = "Random string ABC12345678"
    res = detect_cin(text)
    assert res["value"] is None

# --- Date of Birth Tests ---
def test_detect_dob_valid():
    text1 = "Né le 15/05/1995 à Casablanca"
    res1 = detect_dob(text1)
    assert res1["value"] == "15/05/1995"
    assert res1["confidence"] == 0.92

    text2 = "Date de naissance: 1998-12-01"
    res2 = detect_dob(text2)
    assert res2["value"] == "1998-12-01"

    text3 = "Born: 01.01.2000"
    res3 = detect_dob(text3)
    assert res3["value"] == "01.01.2000"

def test_detect_dob_missing_context():
    # Date without birth prefix keyword should not match DOB
    text = "Project started on 12/05/2021"
    res = detect_dob(text)
    assert res["value"] is None

# --- Social Profile (LinkedIn / GitHub) Tests ---
def test_detect_linkedin_github_valid():
    text1 = "LinkedIn: linkedin.com/in/johndoe"
    res1 = detect_linkedin_github(text1)
    assert res1["value"] == "linkedin.com/in/johndoe"
    assert res1["confidence"] == 0.98

    text2 = "Github profile: https://github.com/developer123"
    res2 = detect_linkedin_github(text2)
    assert res2["value"] == "https://github.com/developer123"

def test_detect_linkedin_github_invalid():
    text = "Visit twitter.com/johndoe"
    res = detect_linkedin_github(text)
    assert res["value"] is None

# --- Moroccan Address Tests ---
def test_detect_address_valid():
    text1 = "Adresse: 123 Rue Principale, Casablanca"
    res1 = detect_address(text1)
    assert "Casablanca" in res1["value"]
    assert res1["confidence"] == 0.87

    text2 = "Residence Hay Riad, Rabat, 10000"
    res2 = detect_address(text2)
    assert res2["value"] == "Rabat, 10000"
    assert res2["confidence"] == 0.92

def test_detect_address_non_moroccan():
    text = "Lives in Paris, France"
    res = detect_address(text)
    assert res["value"] is None

# --- Name Detection Tests ---
def test_detect_name_context():
    text = "Nom complet: Fatima Idrissi\nRole: Python Developer"
    res = detect_name(text)
    assert res["value"] == "Fatima Idrissi"
    assert res["confidence"] == 0.98

def test_detect_name_first_line_heuristic():
    text = "Yassine El Amrani\nDeveloppeur Fullstack\nEmail: yassine@test.ma"
    res = detect_name(text)
    assert res["value"] == "Yassine El Amrani"
    assert res["confidence"] == 0.95

# --- Full PII Aggregation & JSON Schema Compliance Test ---
def test_detect_pii_full_schema():
    resume_text = """
    Fatima Idrissi
    Developpeur Backend Python
    Email: fatima.idrissi@gmail.com
    Tel: +212 612345678
    CIN: AB654321
    Née le 10/08/1997
    Adresse: Quartier Maarif, Casablanca
    LinkedIn: linkedin.com/in/fatima-idrissi
    """
    pii_output = detect_pii(resume_text)
    
    # Verify JSON Schema fields exist and match expected values
    assert pii_output["nom_complet"]["value"] == "Fatima Idrissi"
    assert pii_output["email"]["value"] == "fatima.idrissi@gmail.com"
    assert pii_output["telephone"]["value"] == "+212 612345678"
    assert pii_output["cin"]["value"] == "AB654321"
    assert pii_output["date_naissance"]["value"] == "10/08/1997"
    assert "Casablanca" in pii_output["adresse"]["value"]
    assert pii_output["linkedin_github"]["value"] == "linkedin.com/in/fatima-idrissi"

    for field, item in pii_output.items():
        assert "value" in item
        assert "masked" in item
        assert "confidence" in item
        assert isinstance(item["masked"], bool)
        assert isinstance(item["confidence"], float)
