from pyparsing import java_style_comment
import flask
from flask import request, url_for, redirect
from flask_login import login_required, current_user

from ..models.article import Article
from ..models.user import User, Rating

from pydantic.error_wrappers import ValidationError

from .. import app, articles, users

from ..models.interactions import Interaction, add_interaction


@app.route("/articles/", methods=["GET"])
def list_articles():
    """
    GET a list of articles, paginated.

    Params:
        page (int): The page number to return.
        per_page (int): The number of results per page.
        sort (str): The field to sort by. Defaults to 'date_added'.
        order ('desc', 'asc'): The direction to sort by. Defaults to 'desc'.
    """
    paginate_params, paginate_metadata = get_sort_and_paginate_params(request)
    page, per_page, sort, order = paginate_params

    cursor = articles.find().sort(sort, order)\
        .skip(per_page * (page - 1)).limit(per_page)

    article_count = articles.count_documents({})

    return {
        "articles": [Article(**doc).to_json() for doc in cursor],
        **paginate_metadata,
        "article_count": article_count,
    }


@app.route("/articles/category/<string:given_category>", methods=["GET"])
def find_articles_with_category(given_category):
    """GET a list of articles, paginated."""
    cursor = articles.find({"category": given_category})
    return {"articles": [Article(**doc).to_json() for doc in cursor]}


@app.route("/articles/tag/<string:given_tag>", methods=["GET"])
def find_articles_with_tag(given_tag):
    """GET a list of articles with a given tag."""
    cursor = articles.find({"tags": {"$all": [given_tag]}})
    return {"articles": [Article(**doc).to_json() for doc in cursor]}


@app.route("/articles/recommended", methods=["GET"])
@login_required
def get_recommended_articles():
    """
    GET a list of recommended articles for a user that's logged in.
    If none are found, redirect to GET /articles.
    """

    user_id = current_user.user_id

    recommended = users.find_one({"user_id": user_id})["recommended_articles"]
    if not recommended:
        return redirect(url_for("list_articles"))

    paginate_params, paginate_metadata = get_sort_and_paginate_params(request)
    page, per_page, sort, order = paginate_params

    cursor = articles.find({"article_id": {"$in": recommended}}) \
        .sort(sort, order) \
        .skip(per_page * (page - 1)).limit(per_page)

    return {
        "articles": [Article(**doc).to_json() for doc in cursor],
        **paginate_metadata
    }

@app.route("/articles/recommended/<int:user_id>", methods=["GET"])
def get_recommended_articles_userid(user_id):
    """GET a list of recommended articles for a user."""
    recommended = users.find_one({"user_id": user_id})["recommended_articles"]

    paginate_params, paginate_metadata = get_sort_and_paginate_params(request)
    page, per_page, sort, order = paginate_params

    cursor = articles.find({"article_id": {"$in": recommended}})\
        .sort(sort, order)\
        .skip(per_page * (page - 1)).limit(per_page)

    return {
        "articles": [Article(**doc).to_json() for doc in cursor],
        **paginate_metadata
    }


@app.route("/articles/<int:given_id>", methods=["GET"])
def get_article(given_id):
    """GET an article by its ID."""
    this_article = articles.find_one_or_404({"article_id": given_id})
    add_interaction(current_user.user_id, given_id, type="view")
    return Article(**this_article).to_json()


@app.route("/articles/tags", methods=["GET"])
def find_all_tags():
    """GET a list of all tags."""
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
    """GET a list of all categories."""
    alls = articles.find()
    all_categories = []
    for article in alls:
        c_article = Article(**article) 
        category = c_article.category
        if category not in all_categories:
                all_categories.append(category)

    return {"categories": all_categories}


@app.route("/articles/highest_index", methods=["GET"]) # ???
def find_index():
    id = 0
    cursor = articles.find().sort("article_id", -1).limit(1)
    for curr_article in cursor:
        op_article = Article(**curr_article)
        id = op_article.article_id
    return {"id": id}


@app.route("/articles/", methods=["POST"])
def add_article():
    """POST a new article."""
    new_id = 0
    cursor = articles.find().sort("article_id", -1).limit(1)
    for curr_article in cursor:
        op_article = Article(**curr_article)
        new_id = op_article.article_id
    new_id += 1

    raw_article = request.get_json()
    raw_article["article_id"] = new_id

    try:
        article = Article(**raw_article)
    except ValidationError as e:
        return {"validation error": e.errors()}, 400

    articles.insert_one(article.to_bson())
    return article.to_json()


@app.route("/articles/<int:given_id>", methods=["DELETE"])
def delete_article(given_id):
    """DELETE an article by its ID."""
    deleted_article = articles.find_one_and_delete(
        {"article_id": given_id},
    )
    if deleted_article:
        return Article(**deleted_article).to_json()
    else:
        flask.abort(404, "Article not found")


@app.route("/articles/<int:given_id>", methods=["PUT"])
def update_article(given_id):
    """Update an article by its ID."""

    try:
        article = Article(**request.get_json())
    except ValidationError as e:
        return {"validation error": e.errors()}, 400

    articles.find_one_and_update(
        {"article_id": given_id},
        {"$set": article.to_bson()}
    )
    up_article = articles.find_one_or_404({"article_id": given_id})
    return Article(**up_article).to_json()


def get_sort_and_paginate_params(request):
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    sort = request.args.get("sort", "")
    if sort not in ("date_added", "title"):
        sort = "date_added"

    order = request.args.get("order", "")
    if order == "desc":
        order = -1
    elif order == "asc":
        order = 1
    else:
        if sort == "date_added":
            order = -1
        else:
            order = 1

    metadata = {
        "_page": page,
        "_per_page": per_page,
        "_sort": sort,
        "_order": order,
    }

    return (page, per_page, sort, order), metadata


@app.route("/articles/<int:given_id>/<int:new_grade>", methods=["PUT"])
@login_required
def add_grade_to_article(given_id, new_grade):
    user_id = current_user.user_id
    this_article = articles.find_one_or_404({"article_id": given_id})
    article = Article(**this_article)
    article.n_of_grades += 1
    article.sum_of_grades += new_grade
    articles.find_one_and_update(
        {"article_id": given_id},
        {"$set": article.to_bson()}
    )
    
    rate = Rating(article_id = given_id, grade = new_grade)
    curr_usr = users.find_one_or_404({"user_id": user_id})
    user = User(**curr_usr)
    user.ratings.append(rate)
    articles.find_one_and_update(
        {"user_id": user_id},
        {"$set": user.to_bson()}
    )

    
