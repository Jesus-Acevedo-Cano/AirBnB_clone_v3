#!/usr/bin/python3
""" init flask files """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ return status """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def objs_counter():
    """return total count of each obj per class"""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    classes_dic = {}
    for i in classes:
        classes_dic[i] = storage.count(eval(i))
    return jsonify(classes_dic)
