import flask
from flask import request, url_for
from ..models.comment import Comment

from .. import app, comments


@app.route("/comments/article/<int:article_id>", methods=["GET"])
def find_comments_to_article(article_id):
    cursor = comments.find({"article_id" : article_id})
    return {"comments": [Comment(**doc).to_json() for doc in cursor]}


@app.route("/comment/<int:given_id>", methods=["DELETE"])
def delete_comment(given_id):
    deleted_comment = comments.find_one_and_delete(
        {"comment_id": given_id},
    )
    if deleted_comment:
        return Comment(**deleted_comment).to_json()
    else:
        flask.abort(404, "Comment not found")


@app.route("/comment/<int:given_id>", methods=["PUT"])
def update_comment(given_id):
    comment = Comment(**request.get_json())
    comments.find_one_and_update(
        {"comment_id": given_id},
        {"$set": comment.to_bson()}
    )
    up_comment = comments.find_one_or_404({"comment_id": given_id})
    return Comment(**up_comment).to_json()


@app.route("/comments/", methods=["POST"])
def add_comment():
    new_id = 0
    cursor = comments.find().sort("comment_id", -1).limit(1)
    for curr_com in cursor:
        op_com = Comment(**curr_com)
        new_id = op_com.comment_id
    new_id += 1

    raw_com = request.get_json()
    raw_com["comment_id"] = id

    comment = Comment(**raw_com)
    comments.insert_one(comment.to_bson())
    return comment.to_json()

