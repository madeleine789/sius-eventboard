from app import cache
from libs.user import User

__author__ = 'mms'

from datetime import datetime

from flask import Blueprint, render_template, request, redirect, g, url_for, session
from flask.ext.login import (current_user, fresh_login_required)
from models import models
from libs import tweets
import elasticsearch

es = elasticsearch.Elasticsearch()
events_app = Blueprint('events_app', __name__, template_folder='templates')



@events_app.before_request
def load_user():
	if current_user.is_authenticated():
		g.user = current_user.get_id()
	else: g.user = None


@events_app.route('/')
@cache.cached(timeout=50)
def index():
	access_token = session.get('access_token')
	if access_token is None:
		return redirect('/login/twitter')
	access_token = access_token[0]
	data = {
		'events': models.Event.objects.order_by("-last_updated")
	}
	return render_template('index.html', **data)

@events_app.route("/events/search", methods=["GET", "POST"])
@fresh_login_required
def admin_entry_search():
        if request.method == "GET":
                data = {
			'title': 'Search for an event',
			'event': None,
		}
		return render_template('event/event_search.html', **data)
        else:
                title = request.form.get('title')
                res = es.search(index='events', q='title:"'+title+'"')
                reslist = [];
                for hit in res['hits']['hits']:
                        reslist.append(hit["_source"])
                data = {
        		'events': reslist
        	}
                return render_template('event/events_list.html', **data)

@events_app.route("/events/create", methods=["GET", "POST"])
@fresh_login_required
def admin_entry_create():

	user = User().get_by_id(g.user)
	if user.is_admin(): pass
	else:
		return render_template('index.html', error="User role: COMMENTER. You are not authorized to post events.", events=models.Event.objects.order_by("-last_updated"))

	if request.method == "POST":
		if request.form.get('starting_at') == '' or request.form.get('ending_at') == '':
			error = 'Fill in DateTime fields'
			data = {
				'title': 'Create event',
				'event': None,
				'error': error
			}
			return render_template('event/event_edit.html', **data)

		event = models.Event()
		event.title = request.form.get('title')
		event.description = request.form.get('content')
		event.starting_at = datetime.strptime(request.form.get('starting_at'), '%Y-%m-%d %H:%M:%S')
		event.ending_at = datetime.strptime(request.form.get('ending_at'), '%Y-%m-%d %H:%M:%S')

		event.user = current_user.get_mongo_doc()
		event.save()
                elastic_save(event.title,event.starting_at,event.ending_at,event.description)
		status = event.title + ': ' + event.description
		if len(status) > 140: status = status[:137] + '...'
		tweets.post(status=status)

		return redirect('/events/%s' % event.id)
	else:
		data = {
			'title': 'Create new event',
			'event': None,
		}
		return render_template('event/event_edit.html', **data)

def elastic_save(title,start,end,description):
        es.index(index='events', doc_type='event', body={
            'title': title,
            'start': start,
            'end': end,
            'description': description
        })

@events_app.route("/events/<event_id>/edit", methods=["GET", "POST"])
@fresh_login_required
def admin_entry_edit(event_id):
	event = models.Event.objects().with_id(event_id)

	if event:
		if event.user.id != current_user.id:
			return render_template('index.html', error="ERROR: You do not have permission to edit this event")

		if request.method == "POST":
			if request.form.get('starting_at') == '' or request.form.get('ending_at') == '':
				error = 'Fill in DateTime fields'
				data = {
					'title': 'Edit event',
					'error': error
				}
				return render_template('event/event_edit.html', **data)
			event.title = request.form.get('title', '')
			event.description = request.form.get('content')
			if request.form.get('starting_at'):
				event.starting_at = datetime.strptime(request.form.get('starting_at'), '%Y-%m-%d %H:%M:%S')
			if request.form.get('ending_at'):
				event.ending_at = datetime.strptime(request.form.get('ending_at'), '%Y-%m-%d %H:%M:%S')

			event.save()
		data = {
			'title': 'Edit event',
			'event': event
		}
		return render_template('event/event_edit.html', **data)
	else:
		return render_template('event/event_edit.html', error="Unable to find entry %s".format(event_id))


@events_app.route('/events/<event_id>')
@cache.cached(timeout=50)
def entry_page(event_id):
	event = models.Event.objects().with_id(event_id)

	if event:
		ids = tweets.search(query=event.title)
		data = {
			'event': event,
			'author': event.user,
			'tweet_ids': ids,
		}
		return render_template('event/event_display.html', **data)
	else:
		return render_template('event/event_display.html', error="Event not found.")


@events_app.route('/events/<event_id>', methods=["POST"])
@fresh_login_required
def post_comment(event_id):
	event = models.Event.objects().with_id(event_id)

	if event:
		if request.method == "POST":
			comment = models.Comment()
			comment.author = current_user.username
			comment.body = request.form.get('body')

			event.comments.append(comment)
			event.save()
			return redirect('/events/%s' % event.id)
	else:
		return render_template('event/event_display.html', error="Event not found.")
