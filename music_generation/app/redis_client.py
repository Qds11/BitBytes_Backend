import redis
# Initialize Redis connection
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
print("Redis Connection: ",redis_client)

# Export the Redis client
__all__ = ['redis_client']