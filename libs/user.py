from mongoengine import DoesNotExist

__author__ = 'mms'

from flask.ext.login import (UserMixin, AnonymousUserMixin)

from models import models


class User(UserMixin):
    def __init__(self, username=None, password=None, admin=False, active=True, id=None):
        self.username = username
        self.password = password
        self.active = active
        self.isAdmin = admin
        self.id = None

    def save(self):
        new_user = models.User(username=self.username, password=self.password, isAdmin=self.isAdmin, active=self.active)
        new_user.save()
        print "new user id = %s " % new_user.id
        self.id = new_user.id
        return self.id

    def get_by_username(self, username):
        try:
            db_user = models.User.objects.get(username=username)
            if db_user:
                self.username = db_user.username
                self.active = db_user.active
                self.isAdmin = db_user.isAdmin
                self.id = db_user.id
                return self
            else:
                return None
        except DoesNotExist:
            return None

    def get_by_username_w_password(self, username):

        try:
            db_user = models.User.objects.get(username=username)
            if db_user:
                self.username = db_user.username
                self.active = db_user.active
                self.password = db_user.password
                self.isAdmin = db_user.isAdmin
                self.id = db_user.id
                return self
            else:
                return None
        except DoesNotExist:
            return None

    def get_mongo_doc(self):
        if self.id:
            return models.User.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, id):
        db_user = models.User.objects.with_id(id)
        if db_user:
            self.username = db_user.username
            self.active = db_user.active
            self.isAdmin = db_user.isAdmin
            self.id = db_user.id
            return self
        else:
            return None

    def is_admin(self):
        return self.isAdmin


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
