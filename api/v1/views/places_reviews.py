#!/usr/bin/python3
"""
New view for Review objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def to_get_reviews(place_id):
    """
     list of all Review objects of a Place
    """
    review_list = []

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    for review_obj in reviews:
        review_list.append(review_obj.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews_by_id(review_id):
    """
    list of reviews by given id
    """
    reviews = storage.get(Review, review_id)
    if reviews is None:
        abort(404)

    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def to_delete_reviews(review_id):
    """
    Delete a review obj by given id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def to_create_reviews(place_id):
    """
    Create a new review with POST method
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    new_data = request.get_json()
    if new_data is None:
        abort(400, "Not a JSON")

    if "user_id" not in new_data:
        abort(400, "Missing user_id")

    user = storage.get(User, new_data.get("user_id"))
    if user is None:
        abort(404)

    if "text" not in new_data:
        abort(400, "Missing text")

    new_data["place_id"] = place_id
    new_review = Review(**new_data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def to_update_reviews(review_id):
    """
    Update review obj with metod PUT
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    new_data = request.get_json()
    if new_data is None:
        abort(400, "Not a JSON")

    for key, value in new_data.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
