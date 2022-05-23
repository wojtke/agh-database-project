import json
import os

import dotenv
from pymongo import MongoClient

from backend.models.article import Article

lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam aliquet dui non diam condimentum, nec tincidunt enim ornare. Integer ac dignissim nisi. Pellentesque id ex ullamcorper ex tincidunt tristique. Vestibulum lobortis tortor eu ornare fermentum. Nulla vulputate turpis tortor. Proin sapien nisi, congue nec pellentesque id, ullamcorper vel tortor. Aenean molestie massa nec augue euismod consectetur. Aenean ultricies suscipit elementum. Donec metus est, varius ut tempus at, varius mattis nulla. Suspendisse potenti. Nam vulputate arcu nibh, vitae tincidunt tellus vehicula id. Duis eleifend erat posuere dolor sodales, ut luctus odio sollicitudin. Duis id quam et nibh fringilla sagittis. Nulla sed odio tempus libero ornare finibus. Etiam sed orci ut lorem vulputate mattis a ut tortor. Nam imperdiet tristique risus id eleifend."
img_url_base = "https://source.unsplash.com/random/600x600/?"
MAX_ARTICLES = 1000

if __name__ == '__main__':
    # init db connection
    dotenv.load_dotenv()
    client = MongoClient(os.environ["FLASK_MONGO_URI"])
    db = client.get_default_database()
    articles = db.get_collection("articles")

    new_articles = []

    cursor = articles.find().sort("article_id", -1).limit(1)
    article_id = cursor[0]["article_id"] + 1 if cursor else 1

    for i, line in enumerate(open('news_headline_dataset.json', 'r')):
        if i > MAX_ARTICLES:
            break

        data = json.loads(line)

        category = data['category'].lower()
        tags = [data['category'].lower(), data['headline'].split()[0].lower()]
        img_src = img_url_base + '&'.join(tags)

        article = {
            'title': data['headline'],
            'category': category,
            'tags': tags,
            'content': data['short_description'] + ' ' + lorem_ipsum,
            'image_source': img_src,
            'article_id': article_id
        }
        article_id += 1

        new_articles.append(Article(**article).to_bson())

    articles.insert_many(new_articles)


