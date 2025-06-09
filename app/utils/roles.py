from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role):
    """
    Decorator to ensure a user has a specific role.

    This decorator checks if the JWT contains a 'role' claim and if that
    claim matches the `required_role`.

    Current limitations and future considerations:
    - Single Role Check: This decorator currently supports checking for only one
      specific role. The 'role' claim in the JWT is expected to be a single string.
    - Multiple Roles: If a user could have multiple roles, the JWT claim might need
      to be changed (e.g., to 'roles': ['editor', 'viewer']). The checking logic
      would then need to be adjusted, for example:
      `if required_role not in user.get('roles', [])`.
    - Hierarchical Roles: For hierarchical roles (e.g., admin > editor > viewer),
      a more complex system would be needed, potentially involving a role hierarchy
      definition and checking if the user's role meets or exceeds the required role level.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Retrieve the decoded JWT
            jwt_claims = get_jwt()

            # Expected: 'role' claim is a single string, e.g., "admin" or "user".
            user_role = jwt_claims.get('role')

            if not user_role or user_role != required_role:
                # Note: Consider a more specific error message if the 'role' claim is missing vs. mismatched.
                return jsonify({'message': "Access forbidden: Insufficient role permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
