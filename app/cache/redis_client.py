import json
import redis
import logging

from app.config.settings import settings


logger = logging.getLogger(__name__)


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def get_cache(key: str):

    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None

    except Exception as e:
        logger.error(f"Redis get error: {e}")
        return None


def set_cache(key: str, value, ttl: int):

    try:
        redis_client.setex(key, ttl, json.dumps(value))

    except Exception as e:
        logger.error(f"Redis set error: {e}")


def delete_cache(key: str):

    try:
        redis_client.delete(key)

    except Exception as e:
        logger.error(f"Redis delete error: {e}")