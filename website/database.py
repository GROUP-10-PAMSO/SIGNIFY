from flask_login import UserMixin
from . import db
from datetime import datetime

# For list of registered users
class UserDatabase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    countPictures = db.Column(db.Integer, nullable=False)
    signature = db.Column(db.String(150))
    dateCreated = db.Column(db.DateTime, default=datetime.now)

# For list of user's verified signatures
class SignDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserDatabase.id), nullable=False)
    picture1 = db.Column(db.String(150), nullable=False)
    picture2 = db.Column(db.String(150), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)
    accurate = db.Column(db.Boolean, nullable=True)
    isUserSignature = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)


