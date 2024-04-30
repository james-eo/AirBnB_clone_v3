#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    """
    city_list = []
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    for obj in state.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific City object by ID
    """

    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    return jsonify(city.to_json())


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes City by id
    """

    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({})
