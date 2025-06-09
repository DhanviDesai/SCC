from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from datetime import timedelta

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

from app.utils.token_blocklist import is_token_revoked

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload['jti'])

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from app.url import api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
    
    return app