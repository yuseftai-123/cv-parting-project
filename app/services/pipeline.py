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
    CompetenceTechnique,
    CompetenceLangue,
    Certification,
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
    logger.info(f"[STAGE 2] Detecting document language...")
    language = detect_language(raw_text)
    logger.info(f"[STAGE 2 COMPLETED] Detected language: {language}")

    # Stage 3: PII Regex Detection
    logger.info(f"[STAGE 3] Running deterministic PII detection regex...")
    pii_data = detect_pii(raw_text)
    logger.info(f"[STAGE 3 COMPLETED] Detected PII fields: {list(pii_data.keys())}")

    # Stage 4: PII Masking
    logger.info(f"[STAGE 4] Applying PII masking & token substitution...")
    masked_text, pii_data = mask_pii(raw_text, pii_data)
    logger.info(f"[STAGE 4 COMPLETED] PII text masked ({len(masked_text)} chars)")

    # Stage 5: NER Entity Extraction
    logger.info(f"[STAGE 5] Running spaCy NER & section extraction...")
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

    # Build Experiences list & sum duration in months
    experiences_list = []
    total_months = 0
    for exp in ner_data.get("experiences", []):
        dur = exp.get("duree_mois")
        if dur:
            total_months += dur
        experiences_list.append(ExperienceEntry(
            entreprise=exp.get("entreprise"),
            poste=exp.get("poste"),
            date_debut=exp.get("date_debut"),
            date_fin=exp.get("date_fin"),
            duree_mois=dur,
            description_masquee=exp.get("description"),
            soft_skills_inferes=[]
        ))

    # Build Formations list
    formations_list = []
    for form in ner_data.get("formations", []):
        formations_list.append(FormationEntry(
            etablissement=form.get("etablissement"),
            diplome=form.get("diplome"),
            domaine=form.get("domaine"),
            annee_obtention=form.get("annee_obtention"),
            niveau_rncp_equivalent=None
        ))

    # Build Competences Pydantic object
    comp_data = ner_data.get("competences", {})
    
    tech_objs = [
        CompetenceTechnique(label=t, niveau=None, source="declaratif")
        for t in comp_data.get("techniques", [])
    ]
    
    lang_objs = []
    for l in comp_data.get("langues", []):
        if isinstance(l, dict):
            lang_objs.append(CompetenceLangue(langue=l.get("langue", ""), niveau=l.get("niveau")))
        else:
            lang_objs.append(CompetenceLangue(langue=str(l), niveau=None))

    cert_objs = []
    for c in comp_data.get("certifications", []):
        if isinstance(c, dict):
            cert_objs.append(Certification(label=c.get("label", ""), date=c.get("date")))
        else:
            cert_objs.append(Certification(label=str(c), date=None))

    competences_obj = Competences(
        techniques=tech_objs,
        langues=lang_objs,
        certifications=cert_objs
    )

    # Determine total experience years & primary sector
    total_years = max(1, round(total_months / 12)) if total_months > 0 else 0
    first_title = experiences_list[0].poste if experiences_list else None
    
    secteur = "Informatique & Data"
    if first_title:
        title_lower = first_title.lower()
        if "data" in title_lower or "ingénieure data" in title_lower:
            secteur = "Informatique & Ingénierie Data"
        elif "développeur" in title_lower or "logiciel" in title_lower:
            secteur = "Développement Logiciel & IT"
        elif "chef de projet" in title_lower:
            secteur = "Management de Projets IT"

    profil_obj = Profil(
        titre_poste_actuel=first_title,
        annees_experience_totale=total_years,
        secteur_principal=secteur,
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
        competences=competences_obj,
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
                name_masked=pii_data.get("nom_complet", {}).get("value"),
                email_masked=pii_data.get("email", {}).get("value"),
                phone_masked=pii_data.get("telephone", {}).get("value"),
                raw_json_response=response_data.model_dump(),
                created_at=datetime.utcnow()
            )
            db.add(record)
            db.commit()
            logger.info(f"[STAGE 8 COMPLETED] Successfully persisted record cv_id={cv_id}")
        except Exception as e:
            logger.error(f"[STAGE 8 FAILED] Failed to persist cv_id={cv_id} into DB: {str(e)}")
            db.rollback()

    return response_data
