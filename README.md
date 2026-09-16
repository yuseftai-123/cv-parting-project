# 🎯 CV Parser Engine — Privacy-First Intelligent Resume Parsing SaaS

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![spaCy](https://img.shields.io/badge/spaCy-3.8-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Compliance](https://img.shields.io/badge/Compliance-CNDP%20%7C%20Loi%2009--08-success?style=for-the-badge)](cndp_compliance.md)
[![Tests](https://img.shields.io/badge/Tests-44%2F44%20Passing-brightgreen?style=for-the-badge)](tests/)

> **A production-grade, privacy-first Resume/CV Parsing Engine built with FastAPI, spaCy NER (`fr_core_news_lg`), Deterministic PII Masking, LLM Profile Summarization, and a modern React SaaS Dashboard.**

---

## 🌟 Key Highlights

- **Multi-Format Ingestion**: High-throughput parsing for `.pdf` and `.docx` documents via PyMuPDF and python-docx.
- **Language Detection**: Automatic language classification (French, English, Arabic) powered by `langdetect`.
- **Zero-Leak PII Masking (Loi 09-08 & GDPR)**: Deterministic regex masking for sensitive identifiers (names, emails, Moroccan phone numbers `+212`, CIN, physical addresses, international contacts) with neutral tokens (`[NOM_1]`, `[EMAIL_1]`, `[TEL_1]`).
- **spaCy Named Entity Recognition (NER)**: Sourced with `fr_core_news_lg` to accurately extract job titles, diplomas, institutions, and core skill sets.
- **Pre-LLM Security Gate**: Strict automated barrier (`assert_no_raw_pii_before_llm`) that guarantees no raw personal data is ever dispatched to LLMs or external APIs.
- **Batch Processing**: Ingestion of `.zip` archives containing up to 500 CVs simultaneously.
- **Interactive SaaS Dashboard**: Modern React + Vite UI offering real-time parsing previews, dynamic multi-criteria candidate search (skills, experience, language), and masking audit logs.
- **Full Test Coverage**: 44 automated unit and integration tests covering the entire pipeline.

---

## 🏗️ System Architecture (8-Stage, 3-Layer Pipeline)

```
[Uploaded CV File (.pdf / .docx)]
              │
              ▼
    [STAGE 1: Ingestion & Text Extraction (PyMuPDF / python-docx)]
              │
              ▼
    [STAGE 2: Language Detection (langdetect -> fr/en/ar)]
              │
              ▼
 ┌────────────┴────────────────────────────────────────┐
 │ LAYER 1: Deterministic PII Regex Detection (SF-04)  │
 └────────────┬────────────────────────────────────────┘
              │
              ▼
    [STAGE 4: PII Token Masking ([NOM_1], [EMAIL_1], [TEL_1])]
              │
              ▼
 ┌────────────┴────────────────────────────────────────┐
 │ LAYER 2: spaCy NER Entity Extraction (SF-05)        │
 │ Model: fr_core_news_lg + Job Titles & Diplomas      │
 └────────────┬────────────────────────────────────────┘
              │
              ▼
 ┌────────────┴────────────────────────────────────────┐
 │ LAYER 3: LLM Profile Enrichment & Security Gate     │
 │ Pre-dispatch Gate: assert_no_raw_pii_before_llm     │
 └────────────┬────────────────────────────────────────┘
              │
              ▼
    [STAGE 7 & 8: Strict JSON Schema Validation & Database Storage]
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend API** | Python 3.11, FastAPI, Pydantic v2, Uvicorn |
| **NLP & Extraction** | spaCy (`fr_core_news_lg`), PyMuPDF (fitz), python-docx, langdetect |
| **Frontend UI** | React 18, Vite, Tailwind CSS / Vanilla CSS, Lucide Icons |
| **Database & Cache** | PostgreSQL, Redis (Caching & Task Queues) |
| **Object Storage** | MinIO (S3-compatible storage) |
| **Testing** | Pytest, Pytest-AnyIO (44 test cases) |
| **DevOps** | Docker, Docker Compose |

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python**: `3.11.x`
- **Node.js**: `v18.x` or higher
- **Docker Desktop** (Optional, for PostgreSQL, Redis, MinIO)

---

### 1. Clone the Repository

```bash
git clone https://github.com/yuseftai-123/cv-parting-project.git
cd cv-parting-project
```

---

### 2. Backend Setup (FastAPI)

1. Create and activate a Python virtual environment:
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install backend dependencies and the spaCy language model:
   ```bash
   pip install -r requirements.txt
   python -m spacy download fr_core_news_lg
   ```

3. Configure environment variables:
   ```bash
   # Copy sample configuration if needed
   cp .env.example .env
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   - API Base URL: `http://localhost:8000`
   - Interactive Swagger Docs: `http://localhost:8000/docs`

---

### 3. Frontend Setup (React Dashboard)

In a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

- Web Dashboard URL: `http://localhost:5173`

---

### 4. Optional: Start Infrastructure Services (Docker)

To run PostgreSQL, Redis, and MinIO storage locally:

```bash
docker compose up -d
```

- **PostgreSQL**: `localhost:5432` (Database: `cv_parser_db`)
- **Redis Cache**: `localhost:6379`
- **MinIO Console**: `http://localhost:9001` (Credentials: `minioadmin` / `minioadmin`)

---

## 🧪 Running Automated Tests

The test suite covers PII detection, masking security gates, spaCy NER parsing on French/English resumes, batch ZIP ingestion, and candidate search endpoints:

```bash
pytest tests/ -v
```

Output:
```text
======================= 44 passed in 16.40s =======================
```

---

## 📡 API Reference Endpoints

| Method | Endpoint | Description | Payload / Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Health check for PostgreSQL, Redis, and MinIO | None |
| `POST` | `/api/v1/cvs/upload` | Parse & anonymize a single `.pdf` or `.docx` file | `Multipart Form: file` |
| `POST` | `/api/v1/cvs/batch` | Upload & batch-parse a `.zip` archive (up to 500 CVs) | `Multipart Form: file` |
| `POST` | `/api/v1/cvs/search` | Multi-criteria search (skills, experience, language) | `JSON: {skills, min_experience, language}` |

---

## 🔒 Privacy, CNDP & GDPR Compliance

This project was engineered from the ground up to respect data privacy regulations, specifically the Moroccan **Loi n° 09-08** (supervised by the **CNDP**) and European **GDPR**:
- **Reversible Tokenization**: Sensitive candidate identifiers are substituted by deterministic tokens (`[NOM_1]`, `[EMAIL_1]`, etc.).
- **Zero Third-Party Leakage**: The `assert_no_raw_pii_before_llm` gate intercepts and blocks any unmasked data prior to external LLM processing.
- Detailed audit records and compliance documentation:
  - [`cndp_compliance.md`](cndp_compliance.md)
  - [`registre_des_traitements.md`](registre_des_traitements.md)

---

## 🎓 Academic & Internship Context

- **Developer**: Youssef Taicha
- **Program**: DUT Génie Informatique — École Supérieure de Technologie de Meknès (ESTM), Université Moulay Ismaïl (UMI)
- **Host Company**: Kinova Tech (Casablanca, Morocco)
- **Academic Supervisor**: Prof. A. Aboulfaraj

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
