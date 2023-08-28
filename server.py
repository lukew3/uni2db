from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import json


app = Flask(__name__)
CORS(app)

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['collegedb']


@app.route('/')
def schools():
    """ List schools """
    return "Works!"

@app.route('/<school>')
def subjects(school):
    """ List subjects at a given school """
    subjects = db['course'].distinct("subject");
    return jsonify(subjects)

@app.route('/<school>/<subject>')
def courses(school, subject):
    """ List courses in a subject at a given school """
    courses = list(db['course'].find({'subject': subject}))
    return jsonify(json.loads(json_util.dumps(courses)))


if __name__ == '__main__':
    app.run()
