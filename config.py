import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bellybox_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:root@localhost/bellybox_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
