__author__ = 'mms'

from flask.ext.cache import Cache
from flask.ext.twitter_oembedder import TwitterOEmbedder
from flask_oauth import OAuth
from flask import Flask
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

from pymongo import ReadPreference

app = Flask("FlaskLoginApp")

app.config['MONGODB_SETTINGS'] = {
    'read_preference': ReadPreference.PRIMARY,
    'db': 'eventboard',
    # 'host':'mongodb://user:eventboard@ds029317.mongolab.com:29317/eventboard'
}

app.config['THREADS_PER_PAGE'] = 4
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-know'

app.config['TWITTER_CONSUMER_KEY'] = 'IRh7xn4AZfryNrsXQI3hXNIPu'
app.config['TWITTER_CONSUMER_SECRET'] = 'YhJ0JWYoS7am327ST6PQVkdxmbkvI10A5dIzJs3xv5FWNrgDjV'
app.config['TWITTER_ACCESS_TOKEN'] = '3305385699-0WEBODjVEuMn48QaK80hPCkA7xTJGNk2CU21YSc'
app.config['TWITTER_TOKEN_SECRET'] = 'g8cgsMCNtx8cohb3tNccJX2gEaKZ9u8QcqY1a8wKV7SiK'

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

twitter_oembedder = TwitterOEmbedder()
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
twitter_oembedder.init(app, cache)

flask_bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.refresh_view = 'auth_app.login'

oauth = OAuth()
twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key=app.config['TWITTER_CONSUMER_KEY'],
                           consumer_secret=app.config['TWITTER_CONSUMER_SECRET']
                           )

app.debug = True
