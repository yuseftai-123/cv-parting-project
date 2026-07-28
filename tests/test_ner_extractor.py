"""
Tests for NER Extractor (Layer 2) — Phase 5
Three sample CVs: French, English, Mixed/Minimal
Each test prints a diff-style comparison of expected vs actual extraction.
"""
import json
import pytest
from app.services.ner_extractor import extract_ner


# ============================================================
# Sample CV 1: Standard French CV
# ============================================================
SAMPLE_CV_FR = """
Nom: Ahmed El Mansouri
Email: ahmed.elmansouri@email.com
Téléphone: +212 6 12 34 56 78

Expérience Professionnelle

Développeur Full Stack — Capgemini Technology Services
Janvier 2020 – Décembre 2023
Conception et développement d'applications web avec React et Node.js.
Mise en place de pipelines CI/CD avec GitLab CI.
Collaboration avec les équipes métier pour la définition des besoins.

Stagiaire Développeur Web — OCP Group
Juin 2019 – Août 2019
Stage de fin d'études portant sur la digitalisation des processus internes.
Développement d'un tableau de bord en Angular pour le suivi de production.

Formation

Master Génie Logiciel — Université Mohammed V, Rabat
2017 – 2019
Spécialisation en génie logiciel et systèmes distribués.

Licence Informatique — Faculté des Sciences, Kénitra
2014 – 2017
Formation générale en informatique, algorithmique et bases de données.
"""

EXPECTED_FR = {
    "experiences": [
        {
            "poste": "Développeur Full Stack",
            "entreprise": "Capgemini Technology Services",
            "date_debut": "Janvier 2020",
            "date_fin": "Décembre 2023",
        },
        {
            "poste": "Stagiaire",
            "entreprise": "OCP Group",
            "date_debut": "Juin 2019",
            "date_fin": "Août 2019",
        },
    ],
    "formations": [
        {
            "diplome": "Master",
            "etablissement": "Université Mohammed V",
            "date_debut": "2017",
            "date_fin": "2019",
        },
        {
            "diplome": "Licence",
            "etablissement": "Faculté des Sciences",
            "date_debut": "2014",
            "date_fin": "2017",
        },
    ],
}


# ============================================================
# Sample CV 2: Standard English CV
# ============================================================
SAMPLE_CV_EN = """
John Smith
john.smith@gmail.com | +1 555-123-4567

Work Experience

Software Engineer — Google LLC
March 2021 – Present
Developed microservices using Go and Python for Google Cloud Platform.
Led a team of 4 engineers on the search indexing pipeline.

Data Analyst — Microsoft Corporation
June 2018 – February 2021
Built data pipelines using Apache Spark and Azure Data Factory.
Created executive dashboards in Power BI for sales analytics.

Education

Bachelor of Science in Computer Science — MIT
2014 – 2018
Graduated with honors. Focus on algorithms and machine learning.

Certification: AWS Solutions Architect Associate — 2022
"""

EXPECTED_EN = {
    "experiences": [
        {
            "poste": "Software Engineer",
            "entreprise": "Google LLC",
            "date_debut": "March 2021",
            "date_fin": "Present",
        },
        {
            "poste": "Data Analyst",
            "entreprise": "Microsoft Corporation",
            "date_debut": "June 2018",
            "date_fin": "February 2021",
        },
    ],
    "formations": [
        {
            "diplome": "Bachelor of Science",
            "etablissement": "MIT",
            "date_debut": "2014",
            "date_fin": "2018",
        },
    ],
}


# ============================================================
# Sample CV 3: Mixed/Minimal (less structured)
# ============================================================
SAMPLE_CV_MIXED = """
Fatima Zahra Benali

Analyste Business chez ENCG Consulting, Casablanca
De 2021 à 2023 — Analyse des processus métier et rédaction de cahiers des charges.

Consultant Junior — Deloitte Maroc
2019-2021
Missions d'audit et de conseil en transformation digitale.

Diplôme d'Ingénieur d'État en Informatique
École Nationale des Sciences Appliquées (ENSA), Marrakech
2014 – 2019

Baccalauréat Sciences Mathématiques
Lycée Ibn Khaldoun, Fès — 2014
"""

EXPECTED_MIXED = {
    "experiences": [
        {
            "poste": "Analyste",
            "entreprise": "ENCG Consulting",
            "date_debut": "2021",
            "date_fin": "2023",
        },
        {
            "poste": "Consultant",
            "entreprise": "Deloitte Maroc",
            "date_debut": "2019",
            "date_fin": "2021",
        },
    ],
    "formations": [
        {
            "diplome": "Ingénieur d'État",
            "etablissement": "ENSA",
            "date_debut": "2014",
            "date_fin": "2019",
        },
        {
            "diplome": "Baccalauréat",
            "etablissement": "Lycée Ibn Khaldoun",
            "date_debut": "2014",
            "date_fin": None,
        },
    ],
}


# ============================================================
# Helper: Print diff-style comparison
# ============================================================
def _print_diff(label: str, expected: dict, actual: dict):
    """Print a human-readable diff between expected and actual results."""
    print(f"\n{'='*70}")
    print(f"  DIFF: {label}")
    print(f"{'='*70}")

    for section in ["experiences", "formations"]:
        print(f"\n--- Expected {section} ---")
        for i, entry in enumerate(expected.get(section, [])):
            print(f"  [{i}] {entry}")

        print(f"+++ Actual {section} +++")
        for i, entry in enumerate(actual.get(section, [])):
            # Show only the key fields for readability
            summary = {k: v for k, v in entry.items() if k != "description"}
            print(f"  [{i}] {summary}")

        exp_count = len(expected.get(section, []))
        act_count = len(actual.get(section, []))
        if exp_count != act_count:
            print(f"  [!] Count mismatch: expected {exp_count}, got {act_count}")

    print(f"{'='*70}\n")


# ============================================================
# Tests
# ============================================================
class TestNerExtractorFrenchCV:
    """Test NER extraction on a standard French CV."""

    def test_extracts_experiences(self):
        result = extract_ner(SAMPLE_CV_FR)
        _print_diff("French CV", EXPECTED_FR, result)

        assert len(result["experiences"]) >= 1, (
            "Should extract at least 1 experience entry from the French CV"
        )

    def test_extracts_formations(self):
        result = extract_ner(SAMPLE_CV_FR)

        assert len(result["formations"]) >= 1, (
            "Should extract at least 1 formation entry from the French CV"
        )

    def test_detects_job_titles(self):
        result = extract_ner(SAMPLE_CV_FR)

        # At least one experience should have a job title
        titles = [e.get("poste") for e in result["experiences"] if e.get("poste")]
        assert len(titles) >= 1, "Should detect at least one job title"
        print(f"  Detected job titles: {titles}")

    def test_detects_organizations(self):
        result = extract_ner(SAMPLE_CV_FR)

        orgs = [e.get("entreprise") for e in result["experiences"] if e.get("entreprise")]
        assert len(orgs) >= 1, "Should detect at least one organization"
        print(f"  Detected organizations: {orgs}")

    def test_detects_dates(self):
        result = extract_ner(SAMPLE_CV_FR)

        has_dates = any(
            e.get("date_debut") or e.get("date_fin")
            for e in result["experiences"] + result["formations"]
        )
        assert has_dates, "Should extract at least one date"


class TestNerExtractorEnglishCV:
    """Test NER extraction on a standard English CV."""

    def test_extracts_experiences(self):
        result = extract_ner(SAMPLE_CV_EN)
        _print_diff("English CV", EXPECTED_EN, result)

        assert len(result["experiences"]) >= 1, (
            "Should extract at least 1 experience entry from the English CV"
        )

    def test_extracts_formations(self):
        result = extract_ner(SAMPLE_CV_EN)

        assert len(result["formations"]) >= 1, (
            "Should extract at least 1 formation entry from the English CV"
        )

    def test_detects_english_job_titles(self):
        result = extract_ner(SAMPLE_CV_EN)

        titles = [e.get("poste") for e in result["experiences"] if e.get("poste")]
        assert len(titles) >= 1, "Should detect English job titles"
        print(f"  Detected job titles: {titles}")

    def test_detects_english_organizations(self):
        result = extract_ner(SAMPLE_CV_EN)

        orgs = [e.get("entreprise") for e in result["experiences"] if e.get("entreprise")]
        assert len(orgs) >= 1, "Should detect English organizations"
        print(f"  Detected organizations: {orgs}")


class TestNerExtractorMixedCV:
    """Test NER extraction on a less-structured mixed CV."""

    def test_extracts_experiences(self):
        result = extract_ner(SAMPLE_CV_MIXED)
        _print_diff("Mixed CV", EXPECTED_MIXED, result)

        # This is the harder case — may not find structured sections
        assert len(result["experiences"]) >= 1 or len(result["formations"]) >= 1, (
            "Should extract at least 1 entry from the mixed CV"
        )

    def test_handles_missing_headers(self):
        """The mixed CV has no clear 'Expérience Professionnelle' header.
        The extractor should still find entities via full-text fallback."""
        result = extract_ner(SAMPLE_CV_MIXED)

        total_entries = len(result["experiences"]) + len(result["formations"])
        assert total_entries >= 1, (
            "Should extract entities even without clear section headers"
        )
        print(f"  Total entries found: {total_entries}")


class TestNerEdgeCases:
    """Edge case tests."""

    def test_empty_text_returns_empty(self):
        result = extract_ner("")
        assert result["experiences"] == []
        assert result["formations"] == []

    def test_no_entities_text(self):
        result = extract_ner("This is just a random paragraph with no CV content at all.")
        # Should return empty or minimal results without crashing
        assert isinstance(result["experiences"], list)
        assert isinstance(result["formations"], list)

    def test_result_structure(self):
        """Verify that all returned entries have the expected keys."""
        result = extract_ner(SAMPLE_CV_FR)

        for exp in result["experiences"]:
            assert "poste" in exp, "Experience entry missing 'poste'"
            assert "entreprise" in exp, "Experience entry missing 'entreprise'"
            assert "date_debut" in exp, "Experience entry missing 'date_debut'"
            assert "date_fin" in exp, "Experience entry missing 'date_fin'"
            assert "description" in exp, "Experience entry missing 'description'"

        for form in result["formations"]:
            assert "diplome" in form, "Formation entry missing 'diplome'"
            assert "etablissement" in form, "Formation entry missing 'etablissement'"
            assert "date_debut" in form, "Formation entry missing 'date_debut'"
            assert "date_fin" in form, "Formation entry missing 'date_fin'"
            assert "description" in form, "Formation entry missing 'description'"
