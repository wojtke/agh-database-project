from pymongo.collection import Collection
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_login import LoginManager

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

pymongo = PyMongo(app)
recipes: Collection = pymongo.db.recipes
articles: Collection = pymongo.db.articles
users: Collection = pymongo.db.users
comments: Collection = pymongo.db.comments


from .routes import cocktails, articles, users, comments, auth
