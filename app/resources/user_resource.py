from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.models.user import User
from app.schemas.user_schema import UserSchema
from app import db
from app.utils.roles import role_required
from uuid import uuid4

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListResource(Resource):
    @jwt_required()
    @role_required('user')
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200
    
    def post(self):
        data = request.get_json()
        user = User(
            id = str(uuid4()),
            username = data['username'],
            email = data['email'],
            role = data.get('role', 'user')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user), 200
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return user_schema.dump(user), 200
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204