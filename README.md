# KINOVATECH CV Parser Engine (3-Layer Processing MVP)

> A production-grade, privacy-first Resume/CV Parsing Engine built with FastAPI, spaCy NER (`fr_core_news_lg`), Deterministic PII Masking, LLM Profile Summarization, and a modern React SaaS Dashboard.

---

## System Architecture

The engine processes uploaded CVs through an **8-Stage, 3-Layer Processing Pipeline**:

```
[Uploaded File (.pdf / .docx)]
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
    [STAGE 7 & 8: Section 3.3 JSON Validation & Database Storage]
```

---

## Prerequisites

* **Python**: `3.11.x`
* **Node.js**: `v18.x` or higher
* **Package Manager**: `npm` or `yarn`
* **Optional**: Docker Desktop (for PostgreSQL, Redis, MinIO)

---

## Quickstart Setup Guide

### 1. Run the FastAPI Backend (Port 8000)

Open your first terminal tab (`cmd` or `PowerShell`):

```cmd
cd C:\Users\pc\Desktop\cv-parting-project
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```
* Backend API base URL: `http://localhost:8000`
* Interactive OpenAPI Docs: `http://localhost:8000/docs`

---

### 2. Run the React Dashboard Frontend (Port 5173)

Open your second terminal tab:

```powershell
cd C:\Users\pc\Desktop\cv-parting-project\frontend
npm run dev
```
* Open your browser and navigate to: **`http://localhost:5173`**

---

### 3. Optional: Run Infrastructure Services via Docker Compose

```cmd
docker compose up -d
```
* **PostgreSQL Database**: `localhost:5432` (Database: `cv_parser_db`)
* **Redis Cache**: `localhost:6379`
* **MinIO Storage Console**: `http://localhost:9001` (Credentials: `minioadmin` / `minioadmin`)

---

## API Reference Endpoints

| Endpoint | Method | Description | Payload / Query |
| :--- | :--- | :--- | :--- |
| `/api/v1/health` | `GET` | System health check for Postgres, Redis, MinIO | None |
| `/api/v1/cvs/upload` | `POST` | Upload & parse a single `.pdf` or `.docx` file | `Multipart Form: file` |
| `/api/v1/cvs/batch` | `POST` | Upload & parse a `.zip` archive containing CVs | `Multipart Form: file` |
| `/api/v1/cvs/search` | `POST` | Search & filter parsed CV records | `JSON: {skills, min_experience, language}` |

---

## Running the Pytest Suite

To execute all 43 automated unit and integration test cases:

```cmd
cd C:\Users\pc\Desktop\cv-parting-project
venv\Scripts\python.exe -m pytest tests/ -v
```

---

## Privacy & Compliance

This engine operates in full compliance with the Moroccan **Loi n° 09-08** relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel (enforced by **CNDP**). Refer to [`cndp_compliance.md`](file:///c:/Users/pc/Desktop/cv-parting-project/cndp_compliance.md) and [`registre_des_traitements.md`](file:///c:/Users/pc/Desktop/cv-parting-project/registre_des_traitements.md) for official documentation.
