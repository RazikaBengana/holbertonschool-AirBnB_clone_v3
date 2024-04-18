#!/usr/bin/python3
"""This is a Flask application setup script for a RESTful API server"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")  # Enable CORS for all domains


@app.teardown_appcontext
def teardown_appcont(exception):
    """Close the database session at the end of the request or when the application shuts down"""
    storage.close()

@app.errorhandler(404)
def page_not_found(exception):
    """Return a custom 404 JSON response when a page is not found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")),
            threaded=True, debug=True)  # Run the app with dynamic host and port configuration
