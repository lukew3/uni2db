from flask import jsonify, Blueprint, request
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
@v0.route('/schools')
def schools():
    """ List schools """
    schools = db['courses'].distinct("school")
    return jsonify(schools)


@v0.route('/subjects')
def subjects():
    """ List subjects at a given school """
    school = request.args.get('school')
    if not school:
        return jsonify({'error': 'school is required'})
    subjects = db['courses'].distinct("subject", {'school': school})
    return jsonify(subjects)


@v0.route('/courses')
def courses():
    """ List courses in a subject at a given school """
    school = request.args.get('school')
    subject = request.args.get('subject')
    if not school or not subject:
        return jsonify({'error': 'school and subject are required'})
    courses = list(db['courses'].find({'subject': subject, 'school': school}))
    return jsonify(json.loads(json_util.dumps(courses)))


@v0.route('/transfers')
def transfers():
    """ List transfer courses from one school to another """
    src_school = request.args.get('src_school')
    dest_school = request.args.get('dest_school')
    if not src_school or not dest_school:
        return jsonify({'error': 'src_school and dest_school are required'})
    transfers = list(db['transfers'].find({'src_school': src_school, 'dest_school': dest_school}))
    return jsonify(json.loads(json_util.dumps(transfers)))


@v0.route('/sections')
def sections():
    """ List sections for a given course """
    school = request.args.get('school')
    code = request.args.get('code')
    if not school or not code:
        return jsonify({'error': 'school and code are required'})
    sections = list(db['sections'].find({'code': code, 'school': school}))
    return jsonify(json.loads(json_util.dumps(sections)))