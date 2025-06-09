from flask import Blueprint
from flask_restful import Api

from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

from app.utils.output_marshal import marshal_error

def handle_global_error(e):
    # Handle HTTP exceptions like 404, 400
    if isinstance(e, HTTPException):
        return marshal_error(e.description, e.code)
    
    if isinstance(e, JWTExtendedException) or isinstance(e, ExpiredSignatureError):
        return marshal_error(str(e), 401)

    # Handle all other uncaught exceptions
    return marshal_error(str(e), 500)


api_bp = Blueprint('api', __name__, url_prefix='/v1')
api = Api(api_bp)

from app.v1.url import routes

api.handle_error = handle_global_error