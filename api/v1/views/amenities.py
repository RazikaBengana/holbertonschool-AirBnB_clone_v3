#!/usr/bin/python3
"""Module to manage amenities operations in a RESTful API architecture"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieve a list of all amenities and return them as JSON"""
    all_amenities = []

    for amenity in storage.all(Amenity).values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a specific amenity by its ID and return it as JSON, or return 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    return abort(404) if amenity is None else jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specific amenity by its ID. Returns 404 if not found, or an empty JSON response on success"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        return abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new amenity from JSON data provided in the request. Returns 400 if data is invalid or name is missing"""
    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")

    if res.get("name") is None:
        abort(400, "Missing name")
    new_amenity = Amenity(**res)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """
    Update an existing amenity with JSON data provided;
    Ignores 'id', 'created_at', and 'updated_at';
    Returns 404 if not found
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        return abort(404)
    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")

    for key, value in res.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
