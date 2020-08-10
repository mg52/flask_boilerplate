"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv
import consul
import json
from io import StringIO

basedir = path.abspath(path.dirname(__file__))
load_dotenv(dotenv_path=path.join(basedir, '.env'))

# Read env values from Consul
# c = consul.Consul(host='localhost', port=8500)
# index, data = c.kv.get('MyApp/Development')
# load_dotenv(stream=StringIO(data['Value'].decode("utf-8")), override=True)

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    TOKEN_URL = environ.get('TOKEN_URL')
    AUTH_URL = environ.get('AUTH_URL')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
