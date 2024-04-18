#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from models import storage
from flask import Flask
from flask import render_template
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Close the storage connection at the end of the request or when the application shuts down"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Fetch a list of states and their cities from the storage
    and renders them to the '8-cities_by_states.html' template
    """
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
