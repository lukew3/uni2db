from flask import jsonify, Blueprint
from bson import json_util
from pymongo import MongoClient
import json

# Create blueprint
v0 = Blueprint('v0', __name__)

# Mongodb setup
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']

# Api routes
@v0.route('/')
def schools():
    """ List schools """
    schools = db['courses'].distinct("school")
    return jsonify(schools)


@v0.route('/<school>')
def subjects(school):
    """ List subjects at a given school """
    subjects = db['courses'].distinct("subject", {'school': school})
    return jsonify(subjects)


@v0.route('/<school>/<subject>')
def courses(school, subject):
    """ List courses in a subject at a given school """
    courses = list(db['courses'].find({'subject': subject, 'school': school}))
    return jsonify(json.loads(json_util.dumps(courses)))