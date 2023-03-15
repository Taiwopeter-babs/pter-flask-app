from flask import Flask, render_template
from web_app.config import Config
from dotenv import load_dotenv
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


# from web_app.errors import not_found_error, internal_error


# This module manages the environment variables in .env file
# It must be imported before usage
load_dotenv()

# The database 'db' is initialized with sqlalchemy class
db = SQLAlchemy()
# app = Flask(__name__)

# the 'migrate' object is initialized with the database migration class
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

#  create app Factory
# creates the flask app by initializing the Flask class
def create_app():
    # db = SQLAlchemy()
    app = Flask(__name__)

    # Loads the KEY->VALUE pairs from .env in config.py through Config class
    app.config.from_object(Config)

    # database initialization and database migration
    db.init_app(app)
    migrate.init_app(app, db)

    # @dev imports blueprints from views.py and auth.py
    # and registers them with the app
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # models are imported
    from .database_models import User, Note

    # @dev uses the LoginManager class to manage the login so user is
    # directed to the login page
    # Note: flask returns an Attribute error if the login_manager is not initialized
    login_manager.init_app(app)

    # error handlers for client and database error
    # client: not_found_error -> This is triggered when the user is not registered
    # database: internal_error -> This is triggered when an error occurs in the database,
    # session rollback resets the session so the failed database session does not
    # interfere with any other database access
    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return render_template("404.html"), 404

    # @app.errorhandler(500)
    # def internal_error(error):
    #     db.session.rollback()
    #     return render_template("500.html"), 500

    # app.register_error_handler(Exception, not_found_error)
    # app.register_error_handler(Exception, internal_error)

    # This flow control runs only in production mode.
    # the environment vars are loaded from the config class (ln 34)
    # The first nested flow checks for server availability, and then runs the
    # sequential if-statements to configure email loggings
    # ln-102 creates a folder or not . the RotatingFileHandler class takes a
    # filename (errorlog.log is created as an instance of the class), maxBytes is the max amount of space a log file can occupy,
    #  then it rolls over to a backup, until 5 files are created (backupCount)
    if not app.debug:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"],
                subject="Notes App Server Failure",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists("error_logs"):
            os.mkdir("error_logs")

        error_file_handler = RotatingFileHandler(
            "error_logs/errorlog.log", maxBytes=10240, backupCount=5
        )
        error_file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s]:%(lineno)d"
            )
        )
        error_file_handler.setLevel(logging.INFO)
        app.logger.addHandler(error_file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Pter's blog")

    # @dev directly gets the primary_key of the user(see database_models)
    # so flask checks the validity of the user id parsed into the function
    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(int(id))
        except:
            return None

    return app


# this function is put on hold so i understand flask migrations
# function checks if database exists, otherwise creates it
"""def create_database(app):
    if path.exists("web_app/" + DATABASE_NAME):
        print("Database already exists!!!")
    else:
        db.create_all(app=app)
        print("Database Created!")"""
