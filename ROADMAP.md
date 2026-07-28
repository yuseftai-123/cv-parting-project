# DEFERRED.md — Architectural Exclusion Log & Production Upgrade Roadmap

This document records all architectural components and feature enhancements intentionally deferred from the MVP release scope, detailing the exact rationale for exclusion and the concrete production upgrade path.

---

## 1. Arabic NLP & Morphological Tokenization

* **Why Skipped in MVP**: French (`fr`) and English (`en`) represent over 90% of target tech resumes in Morocco, and complex Arabic morphological segmentation requires specialized heavy tokenization pipelines outside MVP scope.
* **Production Path**: Integrate `camel_tools` or spaCy `ar_core_news_lg` models with custom Arabic root lemmatizers into the Layer 2 NER pipeline.

---

## 2. Model Fine-Tuning (Custom Transformer / NER Model)

* **Why Skipped in MVP**: Pre-trained `fr_core_news_lg` combined with deterministic regex rules achieved high entity extraction accuracy without the dataset annotation overhead required for model training.
* **Production Path**: Annotate a dataset of 1,000+ Moroccan CVs in Prodigy format and fine-tune a domain-specific `CamemBERT-NER` transformer model for custom diploma and enterprise extraction.

---

## 3. Kubernetes Orchestration (k8s / Helm Charts)

* **Why Skipped in MVP**: Docker Compose provided sufficient container orchestration for local multi-service testing without the operational complexity of managing Kubernetes clusters.
* **Production Path**: Deploy containerized FastAPI, Redis, and PostgreSQL microservices to Managed Kubernetes (AWS EKS / Azure AKS) using Helm charts with Horizontal Pod Autoscaling (HPA).

---

## 4. Production Monitoring & Observability (Prometheus / Grafana)

* **Why Skipped in MVP**: Structured application logging and simple `/api/v1/health` checks provided adequate visibility during initial development.
* **Production Path**: Instrument FastAPI endpoints with `prometheus-fastapi-instrumentator` and deploy Grafana dashboards monitoring request latencies, PII masking rates, and error rates.

---

## 5. Async Job Queue & Worker Pool (Celery + Redis)

* **Why Skipped in MVP**: Batch archives were processed synchronously in a sequential loop to minimize local process overhead during early prototype validation.
* **Production Path**: Offload batch ZIP extraction and parsing tasks to Celery background workers backed by Redis message queues and WebSocket status updates.

---

## 6. OCR for Scanned PDF Images (Tesseract / EasyOCR)

* **Why Skipped in MVP**: Native text-based PDFs and `.docx` files represent the vast majority of digital job candidate applications.
* **Production Path**: Integrate `pdf2image` with Tesseract OCR or AWS Textract to automatically extract text when PyMuPDF detects zero text characters.

---

## 7. Enterprise Full-Text Search Engine (Elasticsearch / OpenSearch)

* **Why Skipped in MVP**: Simple SQL `WHERE` queries on PostgreSQL `parsed_cvs` JSON attributes provided fast filtering for initial database volumes.
* **Production Path**: Replicate parsed candidate profiles into an Elasticsearch or OpenSearch cluster supporting fuzzy skill matching, BM25 scoring, and vector embeddings.
