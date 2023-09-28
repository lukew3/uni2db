from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import json


# Flask app configuration
app = Flask(__name__)
CORS(app)

# Mongodb setup
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']

# Blueprints
api = Blueprint('api', __name__)


# Api routes
@api.route('/')
def schools():
    """ List schools """
    schools = db['course'].distinct("school");
    return jsonify(schools)


@api.route('/<school>')
def subjects(school):
    """ List subjects at a given school """
    subjects = db['course'].distinct("subject", {'school': school});
    return jsonify(subjects)


@api.route('/<school>/<subject>')
def courses(school, subject):
    """ List courses in a subject at a given school """
    courses = list(db['course'].find({'subject': subject, 'school': school}))
    return jsonify(json.loads(json_util.dumps(courses)))


# Register blueprints
app.register_blueprint(api, url_prefix='/api')


# Run flask app
if __name__ == '__main__':
    app.run()
