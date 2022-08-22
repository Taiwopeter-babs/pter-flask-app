from tkinter.tix import Form
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    redirect,
    url_for,
    session,
)
from flask_login import login_required, current_user
from web_app.database_models import Note, User
from web_app import db
import json


views = Blueprint("views", __name__)

# function returns user to the home page,
# but requires the user be logged in to view the home page
@views.route("/")
def home():
    return render_template("home.html", user=current_user)


@views.route("/notes", methods=["POST", "GET"])
@login_required
def notes():
    if request.method == "POST":
        note = request.form.get("note")
        note_title = request.form.get("note_title")
        # function checks if the field of text is empty: returns an error if true
        # otherwise, adds the text entered in the field
        if len(note) < 1:
            flash("Nothing to post, Please add a note", category="error")
        else:
            new_note = Note(
                note_data=note, note_title=note_title, user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash("New note added", category="success")
    return render_template("notes.html", user=current_user)


# this function is the endpoint of the javascript function(deleteNote) in index.js
# json loads the converted string of noteId from the deleteNote function and converts
# to a dictionary format 'note'
@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(
        request.data
    )  # request.data is the string from deleteNote function
    # the dictionary format is loaded with 'note' as dictionary name which
    # has the parameter 'noteId'
    noteId = note["noteId"]
    # the database is queried for the note with the id parsed
    note = Note.query.get(noteId)
    # the id is checked for existence
    if note:
        # if note exists, check if user is authenticated
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted.", category="success")
        return render_template("notes.html", user=current_user)
    return jsonify({})


@views.route("/profile/<full_name>", methods=["GET", "POST"])
@login_required
def profile(full_name):
    if current_user.is_authenticated:
        User.query.filter_by(full_name=full_name).first_or_404()
        return render_template("profile.html", user=current_user)


@views.route("/edit_profile/<int:id>", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    if current_user.is_authenticated:
        user = User.query.filter_by(id=id).first()
        full_name_to_update = User.query.get_or_404(id)
        if user and request.method == "POST":
            # set the value in the database to the value entered in the form
            current_user.full_name = request.form.get("full_name")
            current_user.about_user = request.form.get("about_user")
            try:
                db.session.commit()
                render_template(
                    "edit_profile.html",
                    user=current_user,
                    full_name_to_update=session.get("full_name_to_update"),
                )
            except:
                flash("Error! Please try again", category="error")
                render_template(
                    "edit_profile.html",
                    user=current_user,
                    full_name_to_update=session.get("full_name_to_update"),
                )

        elif user and request.method == "GET":
            full_name_to_update.full_name = current_user.full_name
            full_name_to_update.about_user = current_user.about_user
            flash("Your changes have been saved.", category="success")
            render_template(
                "edit_profile.html",
                user=current_user,
                full_name_to_update=full_name_to_update,
            )
        redirect(url_for("views.profile", user=current_user))
