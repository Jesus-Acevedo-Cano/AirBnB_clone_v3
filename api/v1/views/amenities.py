#!/usr/bin/python3
"""
New view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def to_get_amenities(amenity_id=None):
    """
    list of all amenities
    """
    list_amenities_obj = []

    if amenity_id is None:
        for item in storage.all(Amenity).values():
            list_amenities_obj.append(item.to_dict())

        return jsonify(list_amenities_obj)
    else:
        data_amenities = storage.get(Amenity, amenity_id)
        if data_amenities is None:
            abort(404)
        return jsonify(data_amenities.to_dict())

    return jsonify(data_amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """
    Delete aminity by id
    """
    del_amenity = storage.get(Amenity, amenity_id)

    if del_amenity is None:
        abort(404)

    del_amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """
    To create amenities
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    json = request.get_json()
    if "name" not in json:
        abort(400, "Missing name")

    amenity_new = Amenity(**json)
    storage.new(amenity_new)
    storage.save()

    return (jsonify(amenity_new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """
    To update the amenity by id
    """
    amenity_upt = storage.get(Amenity, amenity_id)
    if amenity_upt is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    json = request.get_json()
    if "name" not in json:
        abort(400, "Missing name")

    for key, value in json.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(amenity_upt, key, value)
    amenity_upt.save()

    return jsonify(amenity_upt.to_dict())
