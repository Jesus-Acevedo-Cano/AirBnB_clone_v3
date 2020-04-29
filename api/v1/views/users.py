#!/usr/bin/python3
"""
New view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def to_get_all_users():
    """
    list of all users
    """
    users = storage.all(User)
    users_dic = [val.to_dict() for key, val in data.items()]
    return jsonify(users_dic)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def to_get_user(user_id=None):
    """
    to get individual user obj
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def to_delete_user(user_id=None):
    """
    to delete user by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def to_update_user(user_id=None):
    """
    update an user by given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_data = request.get_json()
    if new_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_data.items():
        if key not in ["id", "email", "updated_at", "created_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def to_create_user():
    """
    to create an user if doesn't exists
    """
    new_data = request.get_json()
    if new_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in new_data:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in new_data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**new_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201
