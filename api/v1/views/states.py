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


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def to_get_states(state_id=None):
    """
    Get all the states of all or get
    """
    list_states_obj = []

    if state_id is None:
        for state in storage.all(State).values():
            list_states_obj.append(state.to_dict())

        return jsonify(list_states_obj)
    else:
        data_state = storage.get(State, state_id)
        if data_state is None:
            abort(404)
        return jsonify(data_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def to_delete_state(state_id):
    """
    Delete a state by id
    """
    del_state = storage.get(State, state_id)

    if del_state is None:
        abort(404)

    del_state.delete()
    storage.save()

    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_reg():
    """
    To create a state
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    json = request.get_json()
    if "name" not in json:
        abort(400, "Missing name")

    state_new = State(**json)
    storage.new(state_new)
    storage.save()

    return (jsonify(state_new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def to_update_state(state_id):
    """
    To update the state by id
    """
    state_upt = storage.get(State, state_id)
    if state_upt is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    json = request.get_json()
    if "name" not in json:
        abort(400, "Missing name")

    for key, value in json.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(state_upt, key, value)
    state_upt.save()

    return jsonify(state_upt.to_dict())
