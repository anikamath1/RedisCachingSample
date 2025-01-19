import aioredis

async def get_redis_connection():
    redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True)
    print("Connected to Redis")
    return redis
