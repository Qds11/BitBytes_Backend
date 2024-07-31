from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    #  Retrieves the IP address of the client making the request
    key_func=get_remote_address,
    # Redis is the backend for storing rate limit data
    storage_uri='redis://redis:6379'

    # local storage
    #storage_uri='memory://'
)
