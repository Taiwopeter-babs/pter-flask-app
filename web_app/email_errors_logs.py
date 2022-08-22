"""from web_app.blog import app
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


def email_errors():
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
        app.logger.info("Pter's blog")"""
