import os

from flask import Flask
from auth import login_required

from helpers import number_of_comments


# to run the application
# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run
# OR
# python -m flask run



UPLOAD_FOLDER = '/Users/dotdj/Desktop/web-projects/CS50BirWri/flaskr/static/upload/'
# SHOULD I DELETE THIS HERE OR WIL THIS BE ADDED TO THE CONFIG.PY?
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.jinja_env.filters['number_of_comments'] = number_of_comments

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # db connection
    from . import db
    db.init_app(app)

    # db connection
    from . import helpers
    db.init_app(app)

    # authentication
    from . import auth
    app.register_blueprint(auth.bp)

    # blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import upload
    app.register_blueprint(upload.bp)


    return app
    