from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .redis_client import redis_client


redis_uri = f'redis://{redis_client.connection_pool.connection_kwargs["host"]}:{redis_client.connection_pool.connection_kwargs["port"]}/{redis_client.connection_pool.connection_kwargs["db"]}'
limiter = Limiter(
    #  Retrieves the IP address of the client making the request
    key_func=get_remote_address,
    # Redis is the backend for storing rate limit data
    storage_uri=redis_uri
    #storage_uri='redis://redis:6379'
    # local storage
    #storage_uri='memory://'
)
