import redis.asyncio as redis

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6380,
    db=0,
    decode_responses=True
)