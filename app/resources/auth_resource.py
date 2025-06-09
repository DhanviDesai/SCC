from flask import request
from flask_restful import Resource
from app.models.user import User
from app.utils.token_blocklist import add_to_blocklist
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
            refresh_token = create_refresh_token(identity=user.id, additional_claims={"role": user.role})
            return { 'access_token': access_token, 'refresh_token': refresh_token}, 200
        return { 'message': 'Invalid email or password' }, 401

class RefreshTokenResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return { 'access_token': new_access_token }, 200

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        add_to_blocklist(jti)
        return { 'message': 'Access token revoked' }, 200

class LogoutRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        add_to_blocklist(jti)
        return { 'message': 'Refresh token revoked' }, 200
        