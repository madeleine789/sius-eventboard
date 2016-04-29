__author__ = 'mms'

from TwitterSearch import *
from app import app
import tweepy


def search(query='cheeky nandos ledge banter', max=5):
    keywords = query.split()
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(keywords)
        # tso.set_language('en')
        # tso.set_include_entities(False)

        ts = TwitterSearch(
            consumer_key=app.config['TWITTER_CONSUMER_KEY'],
            consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
            access_token=app.config['TWITTER_ACCESS_TOKEN'],
            access_token_secret=app.config['TWITTER_TOKEN_SECRET']
        )
        results = []
        for tweet in ts.search_tweets_iterable(tso):
            results.append(tweet['id'])
            # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
            max -= 1
            if not max: break
        # print results
        return results

    except TwitterSearchException as e:  # take care of all those ugly errors if there are some
        print(e)


def post(status='New status'):
    auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'], app.config['TWITTER_TOKEN_SECRET'])
    twitter = tweepy.API(auth)
    twitter.update_status(status=status)
