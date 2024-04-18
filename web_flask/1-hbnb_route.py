#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Route to return a greeting 'Hello HBNB!' when accessed at the root URL"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Route to return 'HBNB' when '/hbnb' URL is accessed"""
    return "HBNB"


if __name__ == "__main__":
    # Starts the Flask application on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port='5000')
