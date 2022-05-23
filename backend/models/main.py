"""from multiprocessing.dummy import Array
from urllib import request
from flask import Flask, jsonify, make_response
from flask_mongoengine import MongoEngine

app = Flask(__name__)

DB_URL = "mongodb+srv://hehe:hehe@cluster0.kd0x9.mongodb.net/projekt_bazy_danych?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URL


db = MongoEngine()
db.init_app()


class Article(db.Document):
    id: db.StringField()
    title: db.StringField()
    tags: Array[db.StringField()]
    category: db.StringField()
    content: db.StringField()
    image_source: db.StringField()
    n_of_grades: db.IntField()
    sum_of_grades: db.IntField()
    n_of_views: db.IntField()

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "tags" : self.tags,
            "category":  self.category,
            "content": self.content,
            "image_source": self.image_source,
            "n_of_grades": self.n_of_grades,
            "sum_of_grades": self.sum_of_grades,
            "n_of_views": self.n_of_views
        }


class Rating(db.Document):
    article_id: db.StringField()
    grade: db.IntField()
    def to_json(self):
        return {
            "article_id" : self.article_id,
            "grade" : self.grade 
        }


class View(db.Document):
    article_id: db.StringField()
    n_view: db.IntField()
    def to_json(self):
        return {
            "article_id" : self.article_id,
            "n_view" : self.n_view 
        }


class User(db.Document):
    id: db.StringField()
    name: db.StringField()
    login: db.StringField()
    ratings: Array[Rating]
    views: Array[View]

    def to_json(self):
        return{
            "id" : self.id,
            "name": self.name,
            "login": self.login,
            "rating": [rt.to_json() for rt in self.ratings],
            "views": [vw.to_json() for vw in self.views]
        }


class Comment(db.Document):
    id: db.StringField()
    user_id: db.StringField()
    article_id: db.StringField()
    content: db.StringField()

    def to_json(self):
        return jsonify(self)


@app.route('/articles', methods=['GET', 'PUT'])
def articles():
    if request.method == "GET":
        article_list = []
        for article in Article.object:
            article_list.append(article)
        return make_response(jsonify(article_list))
    elif request.method == "PUT":
        pass


@app.route('/articles/<article_id>', methods = ['GET', 'DELETE'])
def article_with_id(article_id):
    if request.method == "GET":
        article = Article.objects(id=article_id) 
        if article:
            return(make_response(jsonify(article.to_json())))
    elif request.method == "DELETE":
        pass


@app.route('/article/user/<user_id>', methods = ['GET'])
def articles_recommendend_for_user(user_id):
    pass


@app.route('/article/teg/<tag>', methods = ['GET'])
def articles_with_tag(tag):
    article_list = []
    for article in Article.object:
        if tag in article.tags:
            article_list.append(article)
    return make_response(jsonify(article_list))


@app.route('/article/<article_id>/rate', methods = ['PUT'])
def new_article_rate(article_id):
    pass


@app.route('/comments/article/<article_id>', methods = ['GET', "PUT"])
def comments_for_article(article_id):
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass


@app.route('/comments/<comment_id>', methods = ['DEL'])
def delete_comment(comment_id):
    pass


@app.route('/users', methods = ['GET', 'PUT'])
def get_users():
    if request.method == "GET":
        users_list = []
        for usr in User.object:
            users_list.append(usr)
        return make_response(jsonify(users_list))
    elif request.method == "PUT":
        pass


@app.route('/users/<user_id>', methods = ['GET', 'DEL'])
def get_users(comment_id):
    if request.method == "GET":
        pass
    elif request.method == "DEL":
        pass


if __name__ == '__main__':
    app.run(debug = True)


"""