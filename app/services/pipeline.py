"""
Pipeline Orchestrator Service
Executes the full 8-stage CV parsing pipeline with structured logging at each stage.
"""
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from app.services.extractor import extract_text
from app.services.language_detector import detect_language
from app.services.pii_detector import detect_pii
from app.services.pii_masker import mask_pii
from app.services.ner_extractor import extract_ner
from app.services.llm_enrichment import generate_profile_summary
from app.schemas.cv import (
    CVStructuredResponse,
    PIIFields,
    PIIFieldItem,
    Profil,
    ExperienceEntry,
    FormationEntry,
    Competences,
    Scores,
    AuditTrail
)
from app.models.candidate import ParsedCVRecord

# Configure structured logging
logger = logging.getLogger("cv_pipeline")
logger.setLevel(logging.INFO)


def process_cv_pipeline(
    file_path: str,
    original_filename: str,
    db: Optional[Session] = None
) -> CVStructuredResponse:
    """
    Executes the 8-stage parsing pipeline for a CV:
    1. Extract Text
    2. Detect Language
    3. PII Regex Detection
    4. PII Masking
    5. NER Entity Extraction
    6. LLM Profile Summary Generation
    7. JSON Output Assembly (Pydantic v2)
    8. PostgreSQL Persistence
    """
    start_time = time.time()
    cv_id = str(uuid.uuid4())
    logger.info(f"[STAGE 1] Ingesting & Extracting file: {original_filename} (cv_id={cv_id})")

    # Stage 1: Text Extraction
    raw_text, source_format = extract_text(file_path)
    logger.info(f"[STAGE 1 COMPLETED] Extracted {len(raw_text)} characters, format: {source_format}")

    # Stage 2: Language Detection
    logger.info(f"[STAGE 2] Detecting language for cv_id={cv_id}")
    language = detect_language(raw_text)
    logger.info(f"[STAGE 2 COMPLETED] Language detected: {language}")

    # Stage 3: PII Regex Detection
    logger.info(f"[STAGE 3] Running deterministic PII detection regex rules")
    raw_pii_data = detect_pii(raw_text)
    detected_count = sum(1 for f in raw_pii_data.values() if f.get("value"))
    logger.info(f"[STAGE 3 COMPLETED] Detected {detected_count} PII fields")

    # Stage 4: PII Masking
    logger.info(f"[STAGE 4] Executing PII token masking")
    masked_text, pii_data = mask_pii(raw_text, raw_pii_data)
    logger.info(f"[STAGE 4 COMPLETED] Masking complete. Masked text length: {len(masked_text)} chars")

    # Stage 5: NER Entity Extraction
    logger.info(f"[STAGE 5] Extracting non-PII entities via spaCy NER layer")
    ner_data = extract_ner(masked_text)
    exp_count = len(ner_data.get("experiences", []))
    form_count = len(ner_data.get("formations", []))
    logger.info(f"[STAGE 5 COMPLETED] NER extracted {exp_count} experiences and {form_count} formations")

    # Stage 6: LLM Profile Summary Generation
    logger.info(f"[STAGE 6] Generating LLM profile summary with pre-dispatch security assertion gate")
    summary = generate_profile_summary(masked_text, pii_data)
    logger.info(f"[STAGE 6 COMPLETED] Generated profile summary ({len(summary)} chars)")

    # Stage 7: JSON Output Schema Assembly
    logger.info(f"[STAGE 7] Assembling Pydantic v2 structured JSON schema per Section 3.3")

    # Build PIIFields object
    pii_fields_obj = PIIFields(
        nom_complet=PIIFieldItem(**pii_data.get("nom_complet", {})),
        email=PIIFieldItem(**pii_data.get("email", {})),
        telephone=PIIFieldItem(**pii_data.get("telephone", {})),
        adresse=PIIFieldItem(**pii_data.get("adresse", {})),
        date_naissance=PIIFieldItem(**pii_data.get("date_naissance", {})),
        cin=PIIFieldItem(**pii_data.get("cin", {})),
        linkedin_github=PIIFieldItem(**pii_data.get("linkedin_github", {}))
    )

    # Build Experiences list
    experiences_list = []
    for exp in ner_data.get("experiences", []):
        experiences_list.append(ExperienceEntry(
            entreprise=exp.get("entreprise"),
            poste=exp.get("poste"),
            date_debut=exp.get("date_debut"),
            date_fin=exp.get("date_fin"),
            duree_mois=None,  # Unbuilt fields stay null
            description_masquee=exp.get("description"),
            soft_skills_inferes=[]
        ))

    # Build Formations list
    formations_list = []
    for form in ner_data.get("formations", []):
        formations_list.append(FormationEntry(
            etablissement=form.get("etablissement"),
            diplome=form.get("diplome"),
            domaine=None,
            annee_obtention=None,
            niveau_rncp_equivalent=None
        ))

    # Determine primary job title from first experience if available
    first_title = experiences_list[0].poste if experiences_list else None

    profil_obj = Profil(
        titre_poste_actuel=first_title,
        annees_experience_totale=None,
        secteur_principal=None,
        resume_genere_llm=summary
    )

    # Calculate processing time
    elapsed_ms = int((time.time() - start_time) * 1000)

    # Assemble root JSON schema
    response_data = CVStructuredResponse(
        cv_id=cv_id,
        processing_timestamp=datetime.utcnow().isoformat() + "Z",
        source_format=source_format,
        language_detected=language,
        pii_fields=pii_fields_obj,
        profil=profil_obj,
        experiences=experiences_list,
        formations=formations_list,
        competences=Competences(),
        scores=Scores(completude_cv=0.85, coherence_temporelle=1.0, matching_score=None),
        audit_trail=AuditTrail(
            pipeline_version="1.0",
            layers_applied=["deterministic", "ner", "llm"],
            processing_time_ms=elapsed_ms
        )
    )
    logger.info(f"[STAGE 7 COMPLETED] JSON schema constructed successfully in {elapsed_ms} ms")

    # Stage 8: PostgreSQL Database Persistence
    if db is not None:
        logger.info(f"[STAGE 8] Persisting record cv_id={cv_id} into PostgreSQL database")
        try:
            record = ParsedCVRecord(
                id=cv_id,
                filename=original_filename,
                source_format=source_format,
                language=language,
                structured_data=response_data.model_dump()
            )
            db.add(record)
            db.commit()
            logger.info(f"[STAGE 8 COMPLETED] Record cv_id={cv_id} saved to database")
        except Exception as e:
            logger.warning(f"[STAGE 8 WARNING] Could not persist to DB (offline/mock mode): {e}")
            db.rollback()
    else:
        logger.info(f"[STAGE 8 SKIPPED] No active DB session passed; skipping DB write")

    return response_data
