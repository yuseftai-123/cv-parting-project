"""
Pipeline Orchestrator Service (v2)
Executes the full 8-stage CV parsing pipeline with structured logging at each stage.
Includes Interval Union date calculation for total experience years (Rule 17).
"""
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from sqlalchemy.orm import Session

from app.services.extractor import extract_text
from app.services.language_detector import detect_language
from app.services.pii_detector import detect_pii
from app.services.pii_masker import mask_pii
from app.services.ner_extractor import extract_ner, parse_date_to_month_year
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


def calculate_total_experience_years_union(experiences: List[Dict[str, Any]]) -> float:
    """
    Calculate total years of experience using Interval Union (Rule 17).
    Merges overlapping date ranges so concurrent roles are not double-counted.
    """
    intervals: List[Tuple[int, int]] = []

    for exp in experiences:
        d_debut = exp.get("date_debut")
        d_fin = exp.get("date_fin")
        if not d_debut:
            continue

        try:
            y_start, m_start = parse_date_to_month_year(d_debut)
            y_end, m_end = parse_date_to_month_year(d_fin) if d_fin else (datetime.now().year, datetime.now().month)

            start_month_abs = y_start * 12 + m_start
            end_month_abs = y_end * 12 + m_end

            if end_month_abs >= start_month_abs:
                intervals.append((start_month_abs, end_month_abs))
        except Exception:
            continue

    if not intervals:
        return 0.0

    # Sort intervals by start month
    intervals.sort(key=lambda x: x[0])

    # Merge overlapping intervals
    merged: List[Tuple[int, int]] = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end + 1:  # Overlapping or adjacent
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    merged.append((current_start, current_end))

    # Sum total distinct months across merged union intervals
    total_distinct_months = sum((end - start + 1) for start, end in merged)
    return round(total_distinct_months / 12.0, 1)


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
    raw_experiences = ner_data.get("experiences", [])
    exp_count = len(raw_experiences)
    form_count = len(ner_data.get("formations", []))
    logger.info(f"[STAGE 5 COMPLETED] NER extracted {exp_count} experiences and {form_count} formations")

    # Stage 6: LLM Profile Summary Generation (Rule 10: Anti-contamination)
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
    for exp in raw_experiences:
        experiences_list.append(ExperienceEntry(
            entreprise=exp.get("entreprise"),
            poste=exp.get("poste"),
            date_debut=exp.get("date_debut"),
            date_fin=exp.get("date_fin"),
            duree_mois=exp.get("duree_mois"),
            description_masquee=exp.get("description"),
            soft_skills_inferes=[]
        ))

    # Calculate total experience years using Interval Union (Rule 17)
    total_years = calculate_total_experience_years_union(raw_experiences)

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

    first_title = experiences_list[0].poste if experiences_list else None
    
    secteur = "Informatique & Data"
    if first_title:
        title_lower = first_title.lower()
        if "data" in title_lower or "ingénieure data" in title_lower:
            secteur = "Informatique & Ingénierie Data"
        elif "développeur" in title_lower or "logiciel" in title_lower or "backend" in title_lower or "engineer" in title_lower:
            secteur = "Développement Logiciel & IT"
        elif "chef de projet" in title_lower or "manager" in title_lower:
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
