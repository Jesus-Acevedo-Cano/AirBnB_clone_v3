#!/usr/bin/python3
"""
New view for Places objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def to_get_places(city_id):
    """
    Get all the palces for city_id
    """
    list_places_obj = []

    data_city = storage.get(City, city_id)
    if data_city is None:
        abort(404)

    data_places = data_city.places
    for place in data_places:
        list_places_obj.append(place.to_dict())
    return jsonify(list_places_obj)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def to_get_places_by_id(place_id):
    """
    Get all the palces by id
    """
    data_places = storage.get(Place, place_id)
    if data_places is None:
        abort(404)

    return jsonify(data_places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def to_delete_places(place_id):
    """
    Delete places by id
    """
    del_place = storage.get(Place, place_id)
    if del_place is None:
        abort(404)

    del_place.delete()
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places_reg(city_id):
    """
    To create places by city id
    """
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)

    json = request.get_json()
    if json is None:
        abort(400, "Not a JSON")

    if "user_id" not in json:
        abort(400, "Missing user_id")

    user_by_id = storage.get(User, json.get("user_id"))
    if user_by_id is None:
        abort(404)

    if "name" not in json:
        abort(400, "Missing name")

    json["city_id"] = city_id
    place_new = Place(**json)
    storage.new(place_new)
    storage.save()

    return (jsonify(place_new.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_places(place_id):
    """
    To update places by id
    """
    place_upt = storage.get(Place, place_id)
    if place_upt is None:
        abort(404)

    json = request.get_json()
    if json is None:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_upt, key, value)
    place_upt.save()
    return jsonify(place_upt.to_dict())
