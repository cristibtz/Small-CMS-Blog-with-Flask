from . import db
from flask_login import UserMixin

class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(100), nullable=False)
        CTF_website = db.Column(db.String(100), nullable=False)
        category = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))


       