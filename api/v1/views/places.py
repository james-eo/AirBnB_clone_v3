#!/usr/bin/python3
"""Create a new view for Place objects that
handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False
                 )
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False,
                 )
def places_search():
    """Searches for Place objects based on the JSON in the request body"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    places = []

    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places.extend(city.places)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.extend(city.places)
    if amenities:
        places = [place for place in places if all(
                  amenity_id in place.amenities for amenity_id in amenities
                  )]
    return jsonify([place.to_dict() for place in places])
