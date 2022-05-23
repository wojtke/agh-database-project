import os
from random import randrange

import dotenv
import numpy as np
from pymongo import MongoClient

from datetime import datetime, timedelta

from backend.models.comment import Comment
from backend.models.interactions import InteractionBucket
from backend.models.user import View, Rating

DATE_START = datetime(2022, 3, 12)

categories = [
    "zoologia",
    "sport",
    "technologia",
    "test",
    "crime",
    "entertainment",
    "world news",
    "impact",
    "politics",
    "weird news",
    "black voices",
    "women",
    "comedy",
    "queer voices",
    "sports",
    "business",
    "travel",
    "media",
    "tech",
    "religion",
    "science",
    "latino voices",
    "education"
  ]
def add_view(user_id, article_id):
    users.update_one({"user_id": user_id}, {"$addToSet": {
        "views": View(article_id=article_id, n_view=1).to_bson()
    }})
    articles.update_one({"article_id": article_id}, {"$inc": {"n_of_views": 1}})
    print("Added view: ", user_id, article_id)


def add_grade(user_id, article_id, grade):
    users.update_one({"user_id": user_id}, {"$addToSet": {
        "ratings": Rating(article_id=article_id, grade=grade).to_bson()
    }})
    articles.update_one({"article_id": article_id}, {
        "$inc": {"n_of_grades": 1, "sum_of_grades": grade}
    })
    print("Added grade: ", user_id, article_id, grade)


def add_comment(user_id, article_id, content):
    comments.insert_one(Comment(user_id=user_id, article_id=article_id, content=content).to_bson())
    print("Added comment: ", user_id, article_id, content)


def add_interaction(user_id, article_id, type, date):
    inter = interactions.find_one({
            "date_start": {"$lte": date},
            "date_end": {"$gt": date},
        })
    if inter is None:
        inter = InteractionBucket(
            date_start=date.replace(hour=0, minute=0, second=0, microsecond=0),
            date_end=date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
        ).to_bson()
        interactions.insert_one(inter)
        inter = interactions.find_one({
            "date_start": {"$lte": date},
            "date_end": {"$gt": date},
        })

    interactions.update_one({
            "_id": inter["_id"]
        }, {
            "$inc": { "n_interactions": 1 },
            "$addToSet": {
                "interactions": {
                    "user_id": user_id,
                    "article_id": article_id,
                    "interaction_type": type,
                    "date": date,
                }
            }
    })

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

dotenv.load_dotenv()
client = MongoClient(os.environ["FLASK_MONGO_URI"])
db = client.get_default_database()
articles = db.get_collection("articles")
users = db.get_collection("users")
interactions = db.get_collection("interactions")
comments = db.get_collection("comments")
print("Connected to database")

if __name__ == '__main__':
    users_list = list(users.find({}))
    articles_list = list(articles.find({}))

    for user in users_list:
        user_activity_weights = (np.random.rand(len(categories))**4)*np.random.rand()**2*0.3

        for article in articles_list:
            cat = article["category"]
            if user_activity_weights[categories.index(cat)] > np.random.rand(): #view
                date = random_date(DATE_START, datetime.now())
                add_view(user["user_id"], article["article_id"])
                add_interaction(user["user_id"], article["article_id"], "view", date)

                if np.random.rand() > 0.7: # comment

                    add_comment(user["user_id"], article["article_id"], "nice")
                    add_interaction(user["user_id"], article["article_id"], "comment", date)

                if np.random.rand() > 0.6: # grade
                    add_grade(user["user_id"], article["article_id"], randrange(1, 6))
                    add_interaction(user["user_id"], article["article_id"], "grade", date)

