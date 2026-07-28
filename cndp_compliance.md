# CNDP Privacy & Data Protection Compliance Document (Loi 09-08)

This document establishes the compliance posture of the **KINOVATECH CV Parser Engine** in accordance with the Moroccan **Loi n° 09-08** relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel and enforced by the **Commission Nationale de contrôle de la protection des Données à caractère Personnel (CNDP)**.

---

## 1. Principles of Data Minimization & PII Anonymization (Article 4 & 5)

* **Pre-LLM Masking Security Gate**: Personal Identifiable Information (PII) including full candidate names, email addresses, Moroccan phone numbers (`+212`), national identity card numbers (CIN), dates of birth, and personal home addresses are masked at **Layer 1** using deterministic regex rules prior to any downstream AI/LLM dispatch.
* **Deterministic Tokens**: Raw PII text is converted to anonymous structural tokens (`[NOM_1]`, `[EMAIL_1]`, `[TEL_1]`, `[CIN_1]`).
* **Zero PII Exposure Guarantee**: Pre-dispatch assertions (`assert_no_raw_pii_before_llm`) raise a `SecurityComplianceError` and block outbound API calls if unmasked personal data is present in prompt payloads.

---

## 2. Right to Erasure / "Droit à l'oubli" (Article 7)

* Candidates have the explicit legal right to request the complete deletion of their stored structured CV profiles from PostgreSQL databases and MinIO object storage.
* Administrative endpoints allow immediate cascading purge of candidate records and associated file artifacts.

---

## 3. Storage Isolation & Security Controls (Article 23)

* **Local Storage Isolation**: Candidate files and extracted JSON profiles are stored in private network zones with restricted access.
* **Audit Logging**: All pipeline execution events log timestamps, source formats, and processing latencies without logging raw PII tokens.
