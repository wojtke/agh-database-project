from pymongo.collection import Collection
from flask import Flask
from flask_pymongo import PyMongo

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()

pymongo = PyMongo(app)

recipes: Collection = pymongo.db.recipes
articles: Collection = pymongo.db.articles
users: Collection = pymongo.db.users
comments: Collection = pymongo.db.comments


from .routes import cocktails
from .models import cocktails, objectid