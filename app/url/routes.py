from app.resources.user_resource import UserListResource, UserResource
from app.resources.auth_resource import LoginResource, RefreshTokenResource, LogoutResource, LogoutRefreshResource

from app.url import api

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(RefreshTokenResource, '/refresh')
api.add_resource(LogoutResource, '/logout')
api.add_resource(LogoutRefreshResource, '/logout-refresh')