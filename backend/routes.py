from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {"message": "Data not found"}, 404

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    id = int(id)
    for item in data:
        if int(item.get('id')) == id:
            return jsonify(item), 200
    return {"message": "Data not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    for picture in data:
        if picture['id'] == new_picture['id']:
            return {"message": f"picture with id {picture['id']} already present"}, 302
    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.get_json()
    for picture in data:
        if picture['id'] == id:
            picture['pic_url'] = new_picture['pic_url']
            picture['event_country'] = new_picture['event_country']
            picture['event_city'] = new_picture['event_city']
            picture['event_state'] = new_picture['event_state']
            picture['event_date'] = new_picture['event_date']
            return jsonify(picture), 200
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"message": ""}, 204
    return {"message": "picture not found"}, 404
