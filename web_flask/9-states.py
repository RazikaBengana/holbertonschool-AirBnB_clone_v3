#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from models import storage
from flask import Flask
from flask import render_template
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage connection after each request"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Display a list of all states from storage"""
    all_states = storage.all(State).values()
    return render_template('7-states_list.html', all_states=all_states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Display a specific state by its ID or a default page if not found"""
    all_states = storage.all(State).values()

    for state in all_states:
        if state.id == id:
            return render_template('9-states.html', state=state, id=True)

    return render_template('9-states.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
