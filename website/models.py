from . import db
from flask_login import UserMixin # helps us log users in
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcard.id'))

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(10000))
    back = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin): # inherits from db.Model and UserMixin (usermixin is only for users, not any other data)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    api_key = db.Column(db.String(150))
    notes = db.relationship('Note') # will be able to access all the note the user has created
    flashcards = db.relationship('Flashcard') # will be able to access all the flashcards the user has created
    groups = db.relationship('Group') # will be able to access all the groups the user has created



# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(10000))
#     answer = db.Column(db.String(10000))
#     choices = db.Column(ARRAY(db.String(10000)))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))