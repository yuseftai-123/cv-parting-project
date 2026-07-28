from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import health, cvs
from app.models import candidate  # Register model metadata

# Initialize database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database table creation check: {e}")

app = FastAPI(
    title="KINOVATECH CV Parser API",
    version="1.0.0",
    description="MVP of KINOVATECH CV Parsing Engine API"
)

# Enable CORS for React frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local Vite React dev server & browser origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(cvs.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the KINOVATECH CV Parser API MVP",
        "health_check_url": "/api/v1/health",
        "upload_url": "/api/v1/cvs/upload"
    }
