from app import cache

__author__ = 'mms'


from flask import Blueprint, render_template
from flask.ext.login import (current_user, login_required)
from models import models

users_app = Blueprint('users_app', __name__, template_folder='templates')


@users_app.route('/users')
@cache.cached(timeout=50)
def index():
	data = {
		'users': models.User.objects
	}
	return render_template('user/list.html', **data)

@users_app.route("/profile")
@login_required
@cache.cached(timeout=50)
def show_my_profile():
	return render_template('user/profile.html', user=current_user)


@users_app.route("/users/<user_id>")
@cache.cached(timeout=50)
def show_profile(user_id):
	user = models.User.objects().with_id(user_id)

	if user:
		data = {
			'user': user,
		}
		return render_template('user/profile.html', **data)
	else:
		return render_template('user/profile.html', error="User not found.")