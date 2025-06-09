import redis
import os
from flask import current_app

# Initialize Redis client from app config
# We can't initialize it directly with current_app.config here as it's not available at import time.
# Instead, we'll get the Redis client within the functions or use a lazy initialization approach.
# For simplicity in this context, we'll initialize it globally but it would be better
# to manage it within the app context if this were a larger application.
# However, the instructions imply direct use.

redis_client = None

def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_url = current_app.config.get('REDIS_URL')
        if not redis_url:
            raise RuntimeError("REDIS_URL is not configured in the Flask app.")
        redis_client = redis.from_url(redis_url)
    return redis_client

def add_to_blocklist(jti):
    """Adds a JTI to the Redis blocklist with an expiry time."""
    r = get_redis_client()
    # Use JWT_REFRESH_TOKEN_EXPIRES as the TTL for the JTI in Redis.
    # This is a timedelta object, so we need its total seconds.
    expiry_seconds = current_app.config['JWT_REFRESH_TOKEN_EXPIRES'].total_seconds()
    r.setex(jti, int(expiry_seconds), "revoked")

def is_token_revoked(jwt_payload):
    """
    Checks if the given JTI is in the Redis blocklist.
    This function will be called by flask_jwt_extended.
    The `jwt_payload` argument is a dictionary containing the decoded JWT payload.
    We need to extract the `jti` from it.
    """
    r = get_redis_client()
    jti = jwt_payload["jti"]
    return r.exists(jti) > 0
