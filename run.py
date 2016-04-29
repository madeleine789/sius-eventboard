__author__ = 'mms'

from app import app, cache

from views.events import events_app
from views.auth import auth_app
from views.users import users_app

app.register_blueprint(events_app)
app.register_blueprint(auth_app)
app.register_blueprint(users_app)

if __name__ == "__main__":

	app.run(host='127.0.0.1', port=5000, debug=True)

	with app.app_context():
		cache.clear()
