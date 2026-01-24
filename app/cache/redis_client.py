import os
import json
import redis
import logging
from typing import Any

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Redis Configuration (ENV ONLY)
# --------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

EVENTS_CACHE_TTL = int(os.getenv("EVENTS_CACHE_TTL", "600"))      # 10 minutes
SUMMARY_CACHE_TTL = int(os.getenv("SUMMARY_CACHE_TTL", "120"))    # 2 minutes

# --------------------------------------------------
# Redis Client
# --------------------------------------------------
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None

# --------------------------------------------------
# Cache Helpers
# --------------------------------------------------
def get_cache(key: str) -> Any | None:
    if not redis_client:
        return None

    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except Exception as e:
        logger.error(f"Redis GET error: {e}")
        return None


def set_cache(key: str, value: Any, ttl: int):
    if not redis_client:
        return

    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.error(f"Redis SET error: {e}")


def delete_cache(key: str):
    if not redis_client:
        return

    try:
        redis_client.delete(key)
    except Exception as e:
        logger.error(f"Redis DELETE error: {e}")
