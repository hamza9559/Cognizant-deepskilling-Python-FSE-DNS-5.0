import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secure-flask-dev-token-999')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coursemanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False