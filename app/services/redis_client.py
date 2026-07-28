import redis
from app.config import settings

def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        socket_connect_timeout=2,  # Fail fast if connection cannot be established
        decode_responses=True
    )

import socket

def check_redis_health() -> bool:
    try:
        # Fast socket check to Redis port first
        with socket.create_connection((settings.redis_host, settings.redis_port), timeout=1.0):
            pass
    except Exception as e:
        print(f"Redis port check failed: {e}")
        return False

    try:
        client = get_redis_client()
        # Perform a ping to verify connection is alive
        return bool(client.ping())
    except Exception as e:
        print(f"Redis health check failed: {e}")
        return False
