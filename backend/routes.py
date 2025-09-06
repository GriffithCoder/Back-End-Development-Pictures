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
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a single picture by ID"""
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.get_json()  # Extract JSON from request body

    # Check if picture with the same id already exists
    for p in data:
        if p.get("id") == picture.get("id"):
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture to our in-memory list
    data.append(picture)
    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture by ID"""
    picture_data = request.get_json()

    # find the picture in the data list
    for picture in data:
        if picture["id"] == id:
            picture.update(picture_data)
            return jsonify(picture), 200

    # if not found, return 404
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    for i, picture in enumerate(data):
        if picture["id"] == id:
            del data[i]
            return "", 204  # No content

    return jsonify({"message": "picture not found"}), 404
