"""
SQLAlchemy Candidate Database Models
Stores parsed CV structured records in PostgreSQL.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON
from app.database import Base


class ParsedCVRecord(Base):
    __tablename__ = "parsed_cvs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    source_format = Column(String(50), nullable=False)
    language = Column(String(10), nullable=False)
    structured_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ParsedCVRecord(id={self.id}, filename={self.filename}, language={self.language})>"
