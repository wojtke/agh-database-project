import flask
from flask import request, url_for
from ..models.article import Article

from .. import app, articles


@app.route("/articles/")
def list_articles():
    page = int(request.args.get("page", 1))
    per_page = 10  # A const value.

    cursor = articles.find().sort("name").skip(per_page * (page - 1)).limit(per_page)

    article_count = articles.count_documents({})

    links = {
        "self": {"href": url_for(".list_articles", page=page, _external=True)},
        "last": {
            "href": url_for(
                ".list_articles", page=(article_count // per_page) + 1, _external=True
            )
        },
    }
    if page > 1:
        links["prev"] = {
            "href": url_for(".list_articles", page=page - 1, _external=True)
        }
    if page - 1 < article_count // per_page:
        links["next"] = {
            "href": url_for(".list_articles", page=page + 1, _external=True)
        }

    return {
        "articles": [Article(**doc).to_json() for doc in cursor],
        "_links": links,
    }


@app.route("/articles/<int:given_id>", methods=["GET"])
def get_article(given_id):
    this_article = articles.find_one_or_404({"article_id": given_id})
    return Article(**this_article).to_json()


@app.route("/articles/<int:given_id>", methods=["DELETE"])
def delete_article(given_id):
    deleted_article = articles.find_one_and_delete(
        {"article_id": given_id},
    )
    if deleted_article:
        return Article(**deleted_article).to_json()
    else:
        flask.abort(404, "Article not found")


@app.route("/articles/category/<string:given_category>", methods=["GET"])
def find_articles_with_category(given_category):
    cursor = articles.find({"category" : given_category})
    return {"articles": [Article(**doc).to_json() for doc in cursor]}


@app.route("/articles/tag/<string:given_tag>", methods=["GET"])
def find_articles_with_tag(given_tag):
    cursor = articles.find({"tags" : {"$all" : [given_tag]}})
    return {"articles": [Article(**doc).to_json() for doc in cursor]}


@app.route("/articles/tags", methods=["GET"])
def find_all_tags():
    alls = articles.find()
    all_tags = []
    for article in alls:
        c_article = Article(**article) 
        for tag in c_article.tags:
            if tag not in all_tags:
                all_tags.append(tag)

    return {"tags": all_tags}


@app.route("/articles/categories", methods=["GET"])
def find_all_categories():
    alls = articles.find()
    all_categories = []
    for article in alls:
        c_article = Article(**article) 
        category = c_article.category
        if category not in all_categories:
                all_categories.append(category)

    return {"categories": all_categories}