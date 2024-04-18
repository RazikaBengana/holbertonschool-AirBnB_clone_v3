#!/usr/bin/python3
"""Module that provides a RESTful API interface for user management"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieve a list of all users and return it as a JSON response"""
    all_users = []

    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return(jsonify(all_users))


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by user_id and return the user as a JSON response or 404 if not found"""
    user = storage.get('User', user_id)
    return (abort(404) if user is None else jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user by user_id; return empty JSON response with status 200, or 404 if not found"""
    user = storage.get(User, user_id)

    if user is None:
        return abort(404)

    user.delete()
    storage.save()
    return(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user from JSON input; return new user data as JSON response with status 201"""
    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")

    if res.get("email") is None:
        abort(400, "Missing email")

    if res.get("password") is None:
        abort(400, "Missing password")

    new_user = User(**res)
    new_user.save()
    return(jsonify(new_user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update a user by user_id from JSON input; return updated user data as JSON response, or 404 if not found"""
    user = storage.get('User', user_id)

    if user is None:
        return(abort(404))

    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")

    for key, value in res.items():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(user, key, value)
    user.save()

    return(jsonify(user.to_dict()), 200)
