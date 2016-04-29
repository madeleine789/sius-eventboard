__author__ = 'mms'

from flask import current_app, Blueprint, render_template, request, redirect, session
from app import login_manager, flask_bcrypt
from flask.ext.login import (login_required, login_user, logout_user, confirm_login)

from forms import forms
from libs.user import User

auth_app = Blueprint('auth_app', __name__, template_folder='templates')


@auth_app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST" and "email" in request.form:
		email = request.form["email"]
		u = User()
		user = u.get_by_email_w_password(email)

		if user and flask_bcrypt.check_password_hash(user.password, request.form["password"]) and user.is_active():
			remember = request.form.get("remember", "no") == "no"

			if login_user(user, remember=remember):
				return redirect('/events/create')
			else:
				pass

	return render_template("/auth/login.html")


@auth_app.route("/register", methods=["GET", "POST"])
def register():
	register_form = forms.SignupForm(request.form)
	current_app.logger.info(request.form)
	error = ''
	if request.method == 'POST' and False == register_form.validate():
		error = "Registration error"

	elif request.method == 'POST' and register_form.validate():
		email = request.form['email']

		if u'CREATOR' in request.form['user_role']:
			isAdmin = True
		else:
			isAdmin = False

		password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

		user = User(email=email, password=password_hash, admin=isAdmin)

		try:
			user.save()
			if login_user(user, remember=False):
				return redirect('/')
			else:
				error = "Unable to log in"
		except:
			error = "Error on registration - possible duplicate emails"

	data = {
		'form': register_form,
		'error': error
	}

	return render_template("/auth/register.html", **data)


@auth_app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
	if request.method == "POST":
		confirm_login()
		return redirect(request.args.get("next") or '/admin')
	data = {}
	return render_template("/auth/reauth.html", **data)


@auth_app.route("/logout")
@login_required
def logout():
	logout_user()
	for key in ('identity.name', 'identity.auth_type'):
		session.pop(key, None)
	return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect('/login')


@login_manager.user_loader
def load_user(id):
	if id is None:
		redirect('/login')
	user = User()
	user = user.get_by_id(id)
	if user.is_active():
		return user
	else:
		redirect('/login')
