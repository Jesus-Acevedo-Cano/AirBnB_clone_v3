#!/usr/bin/python3
""" init flask files """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


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
