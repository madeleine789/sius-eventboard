
from services import root_dir, nice_json
from flask import Flask
import json
from werkzeug.exceptions import NotFound


app = Flask(__name__)

with open("{}/database/bookings.json".format(root_dir()), "r") as f:
    bookings = json.load(f)

@app.route("/followers", methods=['GET'])
def followers_list():
    return nice_json(bookings)


@app.route("/followers/<username>", methods=['GET'])
def followers_record(username):
    if username not in bookings:
        raise NotFound

    return nice_json(bookings[username])
