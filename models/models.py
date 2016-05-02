__author__ = 'mms'

import datetime
from app import db


class User(db.Document):
    username = db.StringField(max_length=50, required=True)
    password = db.StringField(default="")
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField()
    timestamp = db.DateTimeField(default=datetime.datetime.now())


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(max_length=140, required=True)
    author = db.StringField(max_length=32, required=True)


class Event(db.Document):
    title = db.StringField(required=True, max_length=120)
    description = db.StringField(required=True)
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    starting_at = db.DateTimeField(required=True)
    ending_at = db.DateTimeField()
    user = db.ReferenceField(User)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
