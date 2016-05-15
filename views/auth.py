from time import sleep

__author__ = 'mms'

from flask import current_app, Blueprint, render_template, request, redirect, session, url_for
from app import login_manager, flask_bcrypt, twitter
from flask.ext.login import (login_required, login_user, logout_user, confirm_login)

from forms import forms
from libs.user import User

auth_app = Blueprint('auth_app', __name__, template_folder='templates')


@auth_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        u = User()
        user = u.get_by_username_w_password(username)

        if user and flask_bcrypt.check_password_hash(user.password, request.form["password"]) and user.is_active():
            remember = request.form.get("remember", "no") == "no"

            if login_user(user, remember=remember):
                return redirect('/events/create')
            else:
                pass

    return render_template("auth/login.html")


@auth_app.route("/register", methods=["GET", "POST"])
def register():
    register_form = forms.SignupForm(request.form)
    current_app.logger.info(request.form)
    error = ''
    if request.method == 'POST' and not register_form.validate():
        error = "Registration error"

    elif request.method == 'POST' and register_form.validate():
        username = request.form['username']

        if u'CREATOR' in request.form['user_role']:
            isAdmin = True
        else:
            isAdmin = False

        password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

        user = User(username=username, password=password_hash, admin=isAdmin)

        try:
            user.save()
            if login_user(user, remember=False):
                return redirect('/')
            else:
                error = "Unable to log in"
        except:
            error = "Error on registration - possible duplicate logins"

    data = {
        'form': register_form,
        'error': error
    }

    return render_template("auth/register.html", **data)


@auth_app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        return redirect(request.args.get("next") or '/admin')
    return redirect('/login/twitter')


@auth_app.route("/logout")
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect('/login/twitter')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@auth_app.route('/login/twitter')
def sign_in_twitter():
    if session.has_key('twitter_token'):
        del session['twitter_token']
        del session['access_token']
        del session['screen_name']
    url = url_for('auth_app.oauth_authorized', next=request.args.get('next'))
    return twitter.authorize(callback=url or request.referrer or None)


@auth_app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or '/'
    if resp is None:
        return redirect(next_url)
    username = resp['screen_name']
    session['access_token'] = resp['oauth_token']
    session['screen_name'] = username
    session['twitter_token'] = (resp['oauth_token'], resp['oauth_token_secret'])

    user = User().get_by_username(username=username)
    if user is None:
        user = User(username=username, admin=True)  # , password=flask_bcrypt.generate_password_hash(username))
        user.save()
        sleep(50)
        if login_user(user, remember=False):
            return redirect('/')
    else:
        login_user(user)
        sleep(50)
        return redirect('/')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login/twitter')
    user = User()
    user = user.get_by_id(id)
    if user.is_active():
        return user
    else:
        redirect('/login/twitter')
