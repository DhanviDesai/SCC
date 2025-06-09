from app.resources.user_resource import UserListResource, UserResource
from flask_restful import Api

def register_routes(app):
    api = Api(app)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    print("Done registering")