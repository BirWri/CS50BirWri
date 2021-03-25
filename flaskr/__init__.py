import os

from flask import Flask
from auth import login_required

from helpers import number_of_comments
from flask_bootstrap import Bootstrap
from extensions import csrf


# to run the application
# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Figure out how to make config.py set up
    #https://hackersandslackers.com/configure-flask-applications/
    #https://itnext.io/how-and-why-have-a-properly-configuration-handling-file-using-flask-1fd925c88f4c
    #https://pythonise.com/series/learning-flask/flask-configuration-files
    
    # Best explanation for instance_relative_config=True importance
    #https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    #Ensure templates are auto-reloaded
    print("Before")
    print(app.config)

    app.config.from_pyfile('config.py')

    print("after")
    print(app.config)
    
    # custom filter to retrieve number of comments a post have. Can be seen as
    # in index page on the comment button
    app.jinja_env.filters['number_of_comments'] = number_of_comments
   
    Bootstrap(app)

    # CSRF, which stands for Cross-Site Request Forgery, is an attack against a web application in which 
    # the attacker attempts to trick an authenticated user into performing a malicious action. 
    # https://testdriven.io/blog/csrf-flask/
    # https://flask-wtf.readthedocs.io/en/stable/csrf.html

    csrf.init_app(app)



    # testing section

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
    