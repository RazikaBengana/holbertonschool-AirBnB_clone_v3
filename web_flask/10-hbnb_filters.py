#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from models import storage
from flask import Flask
from flask import render_template
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def cities():
    """Render a template that displays states and amenities from the storage"""
    all_amenities = storage.all(Amenity).values()
    all_states = storage.all(State).values()
    return render_template('10-hbnb_filters.html', all_states=all_states,
                           all_amenities=all_amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
