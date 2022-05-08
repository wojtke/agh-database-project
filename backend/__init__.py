from pymongo.collection import Collection
from flask import Flask
from flask_pymongo import PyMongo

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()

pymongo = PyMongo(app)

recipes: Collection = pymongo.db.recipes


from .routes import cocktails
from .models import cocktails, objectid