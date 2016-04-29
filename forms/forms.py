__author__ = 'mms'

from models import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import PasswordField
from flask.ext.mongoengine.wtf.orm import validators


user_form = model_form(models.User, exclude=['password'])
event_form = model_form(models.Event, exclude=['comments', 'user', 'last_updated'])

class SignupForm(user_form):
	password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')


class LoginForm(user_form):
	password = PasswordField('Password', validators=[validators.DataRequired()])



