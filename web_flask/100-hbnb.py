#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from flask import Flask, render_template
from os import environ
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)


# Set the environment to development to enable debug and auto-reload
environ['FLASK_ENV'] = 'development'


@app.teardown_appcontext
def states_list_teardown(self):
    """Close the database session at the end of each request to clean up any connection issues"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Render the '100-hbnb.html' template on the '/hbnb' route and pass data models from storage"""
    return render_template('100-hbnb.html',
                           states=storage.all(State),
                           cities=storage.all(City),
                           amenities=storage.all(Amenity),
                           places=storage.all(Place),
                           users=storage.all(User))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
