import flask
from flask import request, url_for
from ..models.user import User
from pydantic.error_wrappers import ValidationError

from .. import app, users


@app.route("/users/")
def list_users():
    page = int(request.args.get("page", 1))
    per_page = 10  # A const value.

    cursor = users.find().sort("name").skip(per_page * (page - 1)).limit(per_page)

    users_count = users.count_documents({})

    links = {
        "self": {"href": url_for(".list_users", page=page, _external=True)},
        "last": {
            "href": url_for(
                ".list_users", page=(users_count // per_page) + 1, _external=True
            )
        },
    }
    if page > 1:
        links["prev"] = {
            "href": url_for(".list_users", page=page - 1, _external=True)
        }
    if page - 1 < users_count // per_page:
        links["next"] = {
            "href": url_for(".list_users", page=page + 1, _external=True)
        }

    return {
        "users": [User(**doc).to_json() for doc in cursor],
        "_links": links,
    }


@app.route("/users/<int:given_id>", methods=["GET"])
def get_user(given_id):
    this_user = users.find_one_or_404({"user_id": given_id})
    return User(**this_user).to_json()


@app.route("/users/<int:given_id>", methods=["DELETE"])
def delete_user(given_id):
    deleted_user = users.find_one_and_delete(
        {"user_id": given_id},
    )
    if deleted_user:
        return User(**deleted_user).to_json()
    else:
        flask.abort(404, "Article not found")


@app.route("/users/<int:given_id>", methods=["PUT"])
def update_user(given_id):
    try:
        user = User(**request.get_json())
    except ValidationError as e:
        return {"validation error": e.errors()}, 400
        
    users.find_one_and_update(
        {"user_id": given_id},
        {"$set": user.to_bson()}
    )
    up_user = users.find_one_or_404({"user_id": given_id})
    return User(**up_user).to_json()


@app.route("/users/", methods=["POST"])
def add_user():
    new_id = 0
    cursor = users.find().sort("user_id", -1).limit(1)
    for curr_usr in cursor:
        op_usr = User(**curr_usr)
        new_id = op_usr.comment_id
    new_id += 1

    raw_usr = request.get_json()
    raw_usr["user_id"] = id

    try:
        user = User(**raw_usr)
    except ValidationError as e:
        return {"validation error": e.errors()}, 400

    users.insert_one(user.to_bson())
    return user.to_json()
