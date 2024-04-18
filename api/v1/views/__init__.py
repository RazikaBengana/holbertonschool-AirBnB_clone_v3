#!/usr/bin/python3
"""
This is the initialization file for the Flask Blueprint;
The Blueprint 'app_views' is defined here with the specified URL prefix '/api/v1';
This setup facilitates modular routing in a Flask application;
Each module within the 'views' subpackage can have its own route handlers,
improving the structure and scalability of the application
"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.users import *
    from api.v1.views.amenities import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
