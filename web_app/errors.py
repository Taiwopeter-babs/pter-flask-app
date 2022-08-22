"""from web_app import db, app
from flask import render_template


# error handlers for client and database error
# client: not_found_error -> This is triggered when the user is not registered
# database: internal_error -> This is triggered when an error occurs in the database,
# session rollback resets the session so the failed database session does not
# interfere with any other database access
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500"""


# blog.py holds the registration of the error handlers,
