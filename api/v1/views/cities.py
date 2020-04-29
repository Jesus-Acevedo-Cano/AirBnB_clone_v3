#!/usr/bin/python3
"""
New view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def to_get_cities(state_id=None):
    """
    list of all cities on a given state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = storage.all(City)
    list_cities_obj = []
    for city in cities.values():
        if city.state_id == state_id:
            list_cities_obj.append(city.to_dict())

    return jsonify(list_cities_obj)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def to_get_city(city_id=None):
    """
    to get an individual city obj
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    city_obj = city_obj.to_dict()
    return jsonify(city_obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def to_delete_city(city_id=None):
    """
    to delete a city by id
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def to_create_city(state_id=None):
    """
    to create a city if it doesn't exists
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_data = request.get_json()
    if new_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in new_data:
        return jsonify({"error": "Missing name"}), 400
    new_data['state_id'] = state_id
    new_city = City(**new_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def to_update_city(city_id=None):
    """
    to update an entry if exists
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    new_data = request.get_json()
    if new_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_data.items():
        if key not in ["id", "state_id", "updated_at", "created_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
