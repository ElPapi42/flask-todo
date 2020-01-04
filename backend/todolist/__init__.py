import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

from todolist.api import api_bp
from todolist.web import web_bp
from todolist.auth import auth_bp, github_bp

def create_app(testing=False):
    """ 
    Init core application 

    args:
        testing (bool): if true, the app will be ready for be tested using the test suit, default: False
    
    """
    # Load .env vars
    dotenv_path = join(dirname(dirname(__file__)), '.env')
    load_dotenv(dotenv_path)
    
    app = Flask("todolist", instance_relative_config=True)
    app.config.from_object("config")

    if(app.env == "development"):
        app.config.from_pyfile("development.py")
    
    if(testing):
        app.debug = True
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TESTING_DATABASE_URI")

    # Init Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(web_bp)
        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(github_bp, url_prefix="/auth")
        
        # Drop all the tables from test database if in test mode
        if(app.testing):
            db.drop_all()
        
        # Create table for models
        db.create_all()

        return app


