import boto3
from botocore.config import Config
from app.config import settings
import socket
from urllib.parse import urlparse

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=settings.minio_endpoint,
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        config=Config(
            signature_version='s3v4',
            connect_timeout=2,
            read_timeout=2,
            retries={'max_attempts': 0}
        ),
        region_name='us-east-1'
    )

def check_minio_health() -> bool:
    try:
        # Fast socket check to MinIO port first
        parsed_url = urlparse(settings.minio_endpoint)
        host = parsed_url.hostname or "127.0.0.1"
        port = parsed_url.port or 9000
        
        with socket.create_connection((host, port), timeout=1.0):
            pass
    except Exception as e:
        print(f"MinIO port check failed: {e}")
        return False

    try:
        client = get_minio_client()
        # List buckets to verify credentials and endpoint reachability
        client.list_buckets()
        return True
    except Exception as e:
        print(f"MinIO health check failed: {e}")
        return False
