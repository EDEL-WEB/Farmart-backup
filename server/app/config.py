

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os


load_dotenv()


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()

# Configuration class
class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_URI") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY")

    # JWT secret key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
