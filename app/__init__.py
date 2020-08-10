"""Initialize Flask app."""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'password',
        'tokenUrl': app.config['TOKEN_URL'],
        'authorizationUrl': app.config['AUTH_URL'],
        'scopes': {
            'read': 'Grant read-only access',
            'write': 'Grant read-write access'
        }
    }
}
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'X-API-KEY'
#     }
# }

api = Api(app=app,
          version="1.0",
          title="Flask Api",
          description="Flask Api PostgreSQL",
          # security='apikey',
          security=[{'oauth2': ['read', 'write']}],
          authorizations=authorizations)

name_space1 = api.namespace('Authentication', description='Authentication')
name_space2 = api.namespace('Actors CRUD', description='Actors CRUD Description')
name_space3 = api.namespace('Movies CRUD', description='Movies CRUD Description')
name_space4 = api.namespace('Actor Movie Relations CRUD', description='Actor Movie Relations CRUD Description')


def create_app():
    with app.app_context():
        from .routes import auth_routes  # Import routes
        from .routes import actor_routes  # Import routes
        from .routes import movie_routes  # Import routes
        from .routes import actor_movie_relation_routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app
