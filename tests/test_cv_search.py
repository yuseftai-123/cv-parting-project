"""
Integration Tests for POST /api/v1/cvs/search (SF-10)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_cvs_endpoint_empty():
    response = client.post(
        "/api/v1/cvs/search",
        json={
            "language": "fr",
            "search_query": "Developpeur"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_results" in data
    assert "results" in data
    assert isinstance(data["results"], list)


def test_search_cvs_with_skills_filter():
    response = client.post(
        "/api/v1/cvs/search",
        json={
            "skills": ["Python", "FastAPI"],
            "min_experience": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] >= 0
