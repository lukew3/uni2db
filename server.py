from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from api.v0 import v0


# Flask app configuration
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(v0, url_prefix='/v0')

# Run flask app
if __name__ == '__main__':
    app.run(debug=True)
