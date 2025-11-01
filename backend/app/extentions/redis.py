from redis import Redis
import os, json
from datetime import datetime
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)

REDIS_ENABLED = os.getenv("ENABLE_REDIS", "false").lower() == "true"
print(REDIS_ENABLED)

redis_instance = None

if REDIS_ENABLED:
    try:
        redis_instance = Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            password=os.getenv("REDIS_PASSWORD", ""),
            decode_responses=True
        )
        if redis_instance.ping():
            logger.info(f"Connected to Redis successfully")
    except Exception as e:
        logger.warning(f"Redis Unavailable: {e}")
        redis_instance = None


class RedisExtension:
    def __init__(self, client: Redis = None):
        self.client = client

    def run_redis_client(self, user, access_token, refresh_token):
        if not self.client:
            logger.debug("Redis not active. Skipping token storage.")
            return

        token_data = {
            "username": user.username,
            "role": user.role,
            "created_at": datetime.utcnow().isoformat()
        }

        try:
            self.client.setex(f"access_token:{access_token}", 1800, json.dumps(token_data))
            self.client.setex(f"refresh_token:{refresh_token}", 604800, json.dumps(token_data))
            self.client.hset(
                f"client_status:{user.username}",
                mapping={"online": "true", "last_login": datetime.utcnow().isoformat()}
            )
        except Exception as e:
            logger.error(f"Redis storage error: {e}")

    def token_exists(self, token):
        if not self.client:
            return False
        try:
            return self.client.exists(f"access_token:{token}") == 1
        except Exception as e:
            logger.error(f"Redis check error: {e}")
            return False

redis_client = RedisExtension(redis_instance)
