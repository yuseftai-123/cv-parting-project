from fastapi import APIRouter, Response, status
from app.database import check_db_health
from app.services.redis_client import check_redis_health
from app.services.minio_client import check_minio_health

router = APIRouter(prefix="/api/v1")

@router.get("/health")
def health_check(response: Response):
    db_ok = check_db_health()
    redis_ok = check_redis_health()
    minio_ok = check_minio_health()
    
    all_healthy = db_ok and redis_ok and minio_ok
    status_text = "healthy" if all_healthy else "unhealthy"
    
    if not all_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    return {
        "status": status_text,
        "details": {
            "database": "up" if db_ok else "down",
            "redis": "up" if redis_ok else "down",
            "minio": "up" if minio_ok else "down"
        }
    }
