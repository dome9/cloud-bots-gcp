import logging
from functools import wraps
from flask import abort, request
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, decode_token
)
import redis

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

logger = logging.getLogger(__name__)

jwt = JWTManager()
redis_client = redis.Redis()

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]
            logger.info(f"Access Token: {access_token}")
            decoded_token = decode_token(access_token)
            logger.info(f"Decoded Token: {decoded_token}")
            if 'handshake' not in decoded_token.get('data', {}):
                logger.error("Invalid handshake token")
                abort(401, 'Invalid handshake token')
            jwt_required()(request)
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication Error: {str(e)}")
            abort(401, str(e))
    return wrapper

@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    token_id = decoded_token.get("jti")
    return redis_client.get(token_id) is not None

def revoke_token(token_id):
    redis_client.set(token_id, "revoked")

def unrevoke_token(token_id):
    redis_client.delete(token_id)

def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return access_token
