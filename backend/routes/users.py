import flask
from flask import request, url_for
from ..models.user import User

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