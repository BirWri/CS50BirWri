
"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

print('CHECK HERE')
print(basedir)

TESTING = True
DEBUG = True
SECRET_KEY = environ.get('SECRET_KEY')
DATABASE=path.join(basedir, 'flaskr.sqlite') 

print(DATABASE)

UPLOAD_FOLDER = '/Users/dotdj/Desktop/web-projects/CS50BirWri/flaskr/static/upload/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}