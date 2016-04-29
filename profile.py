from views.auth import auth_app
from views.events import events_app
from views.users import users_app

__author__ = 'mms'

from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app, cache
import flask_debugtoolbar

app.register_blueprint(events_app)
app.register_blueprint(auth_app)
app.register_blueprint(users_app)

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

app.config['DEBUG_TB_PANELS'] = [
		'flask_debugtoolbar.panels.versions.VersionDebugPanel',
		'flask_debugtoolbar.panels.timer.TimerDebugPanel',
		'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
		'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
		'flask_debugtoolbar.panels.template.TemplateDebugPanel',
		'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
		'flask_debugtoolbar.panels.logger.LoggingPanel',
		'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
		# Add the MongoDB panel
		'flask_debugtoolbar_mongo.panel.MongoDebugPanel',
	]

toolbar = flask_debugtoolbar.DebugToolbarExtension(app)

if __name__ == "__main__":
	# Specify the debug panels you want

	app.run(debug=True)

	with app.app_context():
		cache.clear()
