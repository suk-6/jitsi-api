import redis

rd = redis.StrictRedis(
    host="redis.jitsi-api.orb.local",
    port=6379,
    db=0,
    decode_responses=True,
    charset="utf-8",
)
