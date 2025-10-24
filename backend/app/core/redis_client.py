from redis import Redis
import os

redis_client = Redis(host=os.getenv("REDIS_HOST", "redis"),
                     port=os.getenv("REDIS_PORT", 6379), 
                     db=0,
                     password=os.getenv("REDIS_PASSWORD", "password123"),
                     decode_responses=True)