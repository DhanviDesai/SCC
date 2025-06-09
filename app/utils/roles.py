from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_jwt()
            if not user or user.get('role') != required_role:
                return jsonify({'message': "Access forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator