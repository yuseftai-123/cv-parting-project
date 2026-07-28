"""
Pydantic v2 JSON Schema Models matching Section 3.3 of Cdc_CV_Parser_130726.pdf
Unbuilt/optional fields default to null or empty arrays.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PIIFieldItem(BaseModel):
    value: Optional[str] = None
    masked: bool = False
    confidence: float = 0.0


class PIIFields(BaseModel):
    nom_complet: PIIFieldItem = Field(default_factory=PIIFieldItem)
    email: PIIFieldItem = Field(default_factory=PIIFieldItem)
    telephone: PIIFieldItem = Field(default_factory=PIIFieldItem)
    adresse: PIIFieldItem = Field(default_factory=PIIFieldItem)
    date_naissance: PIIFieldItem = Field(default_factory=PIIFieldItem)
    cin: PIIFieldItem = Field(default_factory=PIIFieldItem)
    linkedin_github: Optional[PIIFieldItem] = Field(default_factory=PIIFieldItem)


class Profil(BaseModel):
    titre_poste_actuel: Optional[str] = None
    annees_experience_totale: Optional[int] = None
    secteur_principal: Optional[str] = None
    resume_genere_llm: Optional[str] = None


class ExperienceEntry(BaseModel):
    entreprise: Optional[str] = None
    poste: Optional[str] = None
    date_debut: Optional[str] = None
    date_fin: Optional[str] = None
    duree_mois: Optional[int] = None
    description_masquee: Optional[str] = None
    soft_skills_inferes: List[str] = Field(default_factory=list)


class FormationEntry(BaseModel):
    etablissement: Optional[str] = None
    diplome: Optional[str] = None
    domaine: Optional[str] = None
    annee_obtention: Optional[int] = None
    niveau_rncp_equivalent: Optional[str] = None


class CompetenceTechnique(BaseModel):
    label: str
    niveau: Optional[str] = None
    source: str = "declaratif"


class CompetenceLangue(BaseModel):
    langue: str
    niveau: Optional[str] = None


class Certification(BaseModel):
    label: str
    date: Optional[str] = None


class Competences(BaseModel):
    techniques: List[CompetenceTechnique] = Field(default_factory=list)
    langues: List[CompetenceLangue] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)


class Scores(BaseModel):
    completude_cv: float = 0.0
    coherence_temporelle: float = 1.0
    matching_score: Optional[float] = None


class AuditTrail(BaseModel):
    pipeline_version: str = "1.0"
    layers_applied: List[str] = Field(default_factory=lambda: ["deterministic", "ner", "llm"])
    processing_time_ms: int = 0


class CVStructuredResponse(BaseModel):
    """
    Root JSON Output Schema per Section 3.3 (SF-07)
    """
    cv_id: str
    processing_timestamp: str
    source_format: str  # pdf | docx | image
    language_detected: str  # fr | ar | en
    pii_fields: PIIFields = Field(default_factory=PIIFields)
    profil: Profil = Field(default_factory=Profil)
    experiences: List[ExperienceEntry] = Field(default_factory=list)
    formations: List[FormationEntry] = Field(default_factory=list)
    competences: Competences = Field(default_factory=list)
    scores: Scores = Field(default_factory=Scores)
    audit_trail: AuditTrail = Field(default_factory=AuditTrail)


class BatchItemResult(BaseModel):
    filename: str
    status: str  # "success" | "failed"
    cv_id: Optional[str] = None
    processing_time_ms: int = 0
    error_detail: Optional[str] = None


class BatchProcessingSummary(BaseModel):
    batch_id: str
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_processing_time_ms: int = 0
    results: List[BatchItemResult] = Field(default_factory=list)
    failed_details: List[Dict[str, str]] = Field(default_factory=list)


class CVSearchRequest(BaseModel):
    """
    Search and Filter parameters for POST /api/v1/cvs/search (SF-10)
    """
    skills: Optional[List[str]] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    language: Optional[str] = None
    search_query: Optional[str] = None


class CVSearchResultItem(BaseModel):
    cv_id: str
    filename: str
    source_format: str
    language: str
    titre_poste_actuel: Optional[str] = None
    skills_matched: List[str] = Field(default_factory=list)
    created_at: str
    structured_data: Dict[str, Any] = Field(default_factory=dict)


class CVSearchResponse(BaseModel):
    total_results: int = 0
    results: List[CVSearchResultItem] = Field(default_factory=list)


