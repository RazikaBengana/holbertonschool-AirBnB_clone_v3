#!/usr/bin/python3
"""Module that provides RESTful API actions for State objects"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieve a list of all State objects as JSON"""
    states = []

    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object by its ID as JSON"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a specific State object by its ID and return an empty JSON response"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new State object from JSON input data and return the new state as JSON"""
    data = request.get_json()

    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    if "name" not in data:
        return make_response("Missing name", 400)

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update a State object by its ID from JSON input data and return the updated state as JSON"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
