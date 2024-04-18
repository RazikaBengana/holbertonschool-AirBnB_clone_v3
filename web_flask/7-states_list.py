#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def removeSql(exception):
    """Close the storage connection to properly clean up after the request handling"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def listState():
    """Render a list of states to a web page using Flask's templating engine"""
    list = storage.all(State).values()
    return render_template("7-states_list.html", list=list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
