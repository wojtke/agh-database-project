import flask
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
