"""
FastAPI Router for CV Operations
POST /api/v1/cvs/upload — Uploads & parses a single CV file.
POST /api/v1/cvs/batch — Uploads a ZIP archive and processes CVs in a synchronous loop (SF-09 / SF-10).
"""
import os
import time
import uuid
import shutil
import zipfile
import tempfile
import logging
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cv import (
    CVStructuredResponse, 
    BatchProcessingSummary, 
    BatchItemResult,
    CVSearchRequest,
    CVSearchResponse,
    CVSearchResultItem
)
from app.models.candidate import ParsedCVRecord
from app.services.pipeline import process_cv_pipeline

logger = logging.getLogger("cv_batch_router")
router = APIRouter(prefix="/api/v1/cvs", tags=["CVs"])


@router.post(
    "/upload",
    response_model=CVStructuredResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload & Parse Single CV",
    description="Accepts a PDF or DOCX file, runs the 8-stage parsing pipeline, and returns structured JSON."
)
def upload_cv(
    file: UploadFile = File(...),
    db: Optional[Session] = Depends(get_db)
):
    filename = file.filename or "uploaded_cv"
    _, ext = os.path.splitext(filename.lower())

    if ext not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Only .pdf and .docx are supported."
        )

    # Save uploaded bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        response = process_cv_pipeline(
            file_path=tmp_path,
            original_filename=filename,
            db=db
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CV pipeline: {str(e)}"
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post(
    "/batch",
    response_model=BatchProcessingSummary,
    status_code=status.HTTP_200_OK,
    summary="Upload & Parse Batch CV Archive (ZIP)",
    description="Accepts a ZIP archive containing CVs, runs each through the pipeline synchronously, and returns a batch summary."
)
def upload_cv_batch(
    file: UploadFile = File(...),
    db: Optional[Session] = Depends(get_db)
):
    filename = file.filename or "batch.zip"
    _, ext = os.path.splitext(filename.lower())

    if ext != ".zip":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid batch archive format '{ext}'. Only .zip archives are supported."
        )

    batch_id = str(uuid.uuid4())
    batch_start_time = time.time()
    logger.info(f"[BATCH START] Initiating batch parsing job batch_id={batch_id} for file '{filename}'")

    tmp_dir = tempfile.mkdtemp(prefix="cv_batch_")
    zip_path = os.path.join(tmp_dir, "archive.zip")

    results = []
    failed_details = []
    success_count = 0
    fail_count = 0

    try:
        # Save ZIP archive bytes
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract ZIP archive
        extract_dir = os.path.join(tmp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Scan extracted directory recursively for supported files
        extracted_files = []
        for root, _, files in os.walk(extract_dir):
            for fname in files:
                # Ignore hidden files / macOS metadata
                if fname.startswith(".") or fname.startswith("__MACOSX"):
                    continue
                extracted_files.append((fname, os.path.join(root, fname)))

        logger.info(f"[BATCH {batch_id}] Found {len(extracted_files)} files in ZIP archive")

        # Synchronous sequential processing loop
        for fname, fpath in extracted_files:
            file_start = time.time()
            _, file_ext = os.path.splitext(fname.lower())

            if file_ext not in [".pdf", ".docx"]:
                fail_count += 1
                err_msg = f"Unsupported file extension '{file_ext}'"
                logger.warning(f"[BATCH {batch_id}] Skipping file '{fname}': {err_msg}")
                results.append(BatchItemResult(
                    filename=fname,
                    status="failed",
                    cv_id=None,
                    processing_time_ms=0,
                    error_detail=err_msg
                ))
                failed_details.append({"filename": fname, "reason": err_msg})
                continue

            try:
                logger.info(f"[BATCH {batch_id}] Processing file '{fname}' through pipeline")
                parsed_res = process_cv_pipeline(
                    file_path=fpath,
                    original_filename=fname,
                    db=db
                )
                elapsed_ms = int((time.time() - file_start) * 1000)
                success_count += 1
                results.append(BatchItemResult(
                    filename=fname,
                    status="success",
                    cv_id=parsed_res.cv_id,
                    processing_time_ms=elapsed_ms,
                    error_detail=None
                ))
                logger.info(f"[BATCH {batch_id}] Successfully processed '{fname}' in {elapsed_ms} ms")
            except Exception as e:
                elapsed_ms = int((time.time() - file_start) * 1000)
                fail_count += 1
                err_msg = str(e)
                logger.error(f"[BATCH {batch_id}] Failed processing '{fname}': {err_msg}")
                results.append(BatchItemResult(
                    filename=fname,
                    status="failed",
                    cv_id=None,
                    processing_time_ms=elapsed_ms,
                    error_detail=err_msg
                ))
                failed_details.append({"filename": fname, "reason": err_msg})

        total_batch_time_ms = int((time.time() - batch_start_time) * 1000)
        logger.info(f"[BATCH COMPLETED {batch_id}] Processed {len(extracted_files)} files ({success_count} succeeded, {fail_count} failed) in {total_batch_time_ms} ms")

        return BatchProcessingSummary(
            batch_id=batch_id,
            total_files=len(extracted_files),
            successful_files=success_count,
            failed_files=fail_count,
            total_processing_time_ms=total_batch_time_ms,
            results=results,
            failed_details=failed_details
        )

    finally:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)


@router.post(
    "/search",
    response_model=CVSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search & Filter Parsed CVs (SF-10)",
    description="Filters parsed CV records by skills, min/max experience years, language, and search query using SQL."
)
def search_cvs(
    req: CVSearchRequest,
    db: Optional[Session] = Depends(get_db)
):
    if db is None:
        # DB offline fallback: return empty result set
        logger.warning("[SEARCH WARNING] DB session unavailable. Returning empty search result.")
        return CVSearchResponse(total_results=0, results=[])

    try:
        query = db.query(ParsedCVRecord)

        # 1. Filter by language
        if req.language:
            query = query.filter(ParsedCVRecord.language == req.language.lower())

        # 2. Filter by search query (filename or current role title)
        if req.search_query:
            pattern = f"%{req.search_query}%"
            query = query.filter(ParsedCVRecord.filename.ilike(pattern))

        records = query.all()
        matched_items = []

        # Python-level JSON attributes evaluation for skills & experience
        for rec in records:
            data = rec.structured_data or {}
            profile = data.get("profil", {})
            title = profile.get("titre_poste_actuel", "")
            
            # Experience filtering
            total_exp = profile.get("annees_experience_totale") or 0
            if req.min_experience is not None and total_exp < req.min_experience:
                continue
            if req.max_experience is not None and total_exp > req.max_experience:
                continue

            # Skills matching
            competences = data.get("competences", {})
            tech_skills = [s.get("label", "").lower() for s in competences.get("techniques", [])] if isinstance(competences, dict) else []
            
            # Collect matched skills
            matched_skills = []
            if req.skills:
                req_skills_lower = [s.lower() for s in req.skills]
                # check matching
                matched_skills = [s for s in req_skills_lower if any(s in ts for ts in tech_skills)]
                if not matched_skills:
                    continue

            matched_items.append(CVSearchResultItem(
                cv_id=rec.id,
                filename=rec.filename,
                source_format=rec.source_format,
                language=rec.language,
                titre_poste_actuel=title,
                skills_matched=matched_skills,
                created_at=rec.created_at.isoformat() if rec.created_at else "",
                structured_data=data
            ))

        return CVSearchResponse(
            total_results=len(matched_items),
            results=matched_items
        )

    except Exception as e:
        err_msg = str(e)
        if "OperationalError" in err_msg or "timeout expired" in err_msg or "connection to server" in err_msg:
            logger.warning(f"[SEARCH WARNING] DB offline/unreachable: {err_msg}. Returning empty results.")
            return CVSearchResponse(total_results=0, results=[])

        logger.error(f"[SEARCH ERROR] Query failed: {err_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing search query: {err_msg}"
        )

