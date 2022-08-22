import os
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP_ENV = os.environ.get("FLASK_APP")
    TRAP_HTTP_EXCEPTIONS = os.environ.get("TRAP_HTTP_EXCEPTIONS")
    PROPAGATE_EXCEPTIONS = os.environ.get("PROPAGATE_EXCEPTIONS")

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["taiwoflask@gmail.com"]
