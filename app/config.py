from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "cv_parser"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: str = "postgresql://postgres:postgres@localhost:5432/cv_parser"
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "cv-parser-bucket"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
