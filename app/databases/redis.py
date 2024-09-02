import redis

from app.config import Settings

env = Settings()

rd = redis.StrictRedis(
    host=env.redis_host,
    port=env.redis_port,
    db=0,
    decode_responses=True,
    charset="utf-8",
)
