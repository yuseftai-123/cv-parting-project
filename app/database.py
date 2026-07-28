from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"connect_timeout": 2},
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import socket

def check_db_health() -> bool:
    try:
        # Fast socket check to PostgreSQL port first
        with socket.create_connection((settings.postgres_host, settings.postgres_port), timeout=1.5):
            pass
    except Exception as e:
        print(f"PostgreSQL port check failed: {e}")
        return False

    try:
        # Execute a simple SELECT 1 to verify database connectivity
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        # Logging or printing for visibility
        print(f"PostgreSQL query check failed: {e}")
        return False
