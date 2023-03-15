from email.policy import default
from web_app import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


# @dev uses a relationship object to associate the User class to
# the Notes class so the user is uniquely matched with all notes created
# this is a one -> many relationship
class User(db.Model, UserMixin):
    __tablename__ = "USER"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    full_name = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    notes_of_user = db.relationship("Note", backref="author", lazy="dynamic")
    user_last_seen = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    about_user = db.Column(db.String(150))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # This function generates avatar for each user profile
    # the user email is converted to lower case
    # md5 works on bytes, hence email is converted to bytes from strings
    # before passing the hashing function
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=mp&s={}".format(digest, size)


# @dev uses a ForeignKey object to associate the notes created to the user
# this is a many -> one relationship
# !!!IMPORTANT!!! => The argument in the foreignkey object was changed from string to
# the actual name of the model 1.e instead of 'user.id', it became User.id
#  otherwise an attribute error
class Note(db.Model, UserMixin):
    __tablename__ = "NOTE"
    id = db.Column(db.Integer, primary_key=True)
    note_data = db.Column(db.String(10000))
    note_time = db.Column(
        db.DateTime(timezone=True), index=True, default=datetime.now(timezone.utc)
    )
    note_title = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
