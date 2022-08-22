from flask import Blueprint, render_template, request, flash, redirect, url_for
from web_app.database_models import User
from web_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from web_app.views import views
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from datetime import datetime, timezone


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if current_user.is_authenticated:
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("views.home")
            return redirect(next_page)

        # @dev queries the database and checks if the email exists,
        # since it's unique, the first email is returned,
        # and the password is checked for correctness by the hashing function
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                flash("Logged in successfully", category="success")
                # function remembers user in the current session
                login_user(user, remember=True)

                # returns user to the initial page requested
                next_page = request.args.get("next")
                if not next_page or url_parse(next_page).netloc != "":
                    next_page = url_for("views.home")
                return redirect(next_page)

                # return redirect(url_for("views.home"))
            else:
                flash("Incorrect email or password", category="error")
                return redirect(url_for("auth.login"))
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)


# This fuction requires the user is logged in to the server and
# redirects user to the login page after logout is requested.
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


# This function checks the http method before proceeding to other
# queries
@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        full_name = request.form.get("Name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # function queries the database and checks if the email exists,
        # since it's unique, the first email is returned, otherwise user is prompted
        # to register
        user = User.query.filter_by(email=email).first()
        if user:
            flash(
                "Account already exists, Please Sign up",
                category="error",
            )

        elif len(email) < 4:
            flash("Email must be at least 4 characters.", category="error")
        elif len(full_name) < 2:
            flash("Name must be at least 2 characters.", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters!", category="error")
        elif password1 != password2:
            flash("Passwords don't match!", category="error")
        else:
            # add user account
            new_user = User(email=email, full_name=full_name)
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()
            # @function remembers the user and redirects to HomePage after registration
            flash("Account created successfully!", category="success")
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("auth.login")
            return redirect(next_page)

    return render_template("sign-up.html", user=current_user)


# This function checks if the user is logged in and then inserts the
# current time to user_last_seen
@auth.before_request
def last_seen_time_before_request():
    if current_user.is_authenticated:
        current_user.user_last_seen = datetime.now(timezone.utc)
        db.session.commit()
