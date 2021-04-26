
"""Flask configuration."""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV='development'
SECRET_KEY = environ.get('SECRET_KEY')
DATABASE=path.join(basedir, 'flaskr.sqlite') 

UPLOAD_FOLDER ='static/upload/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}