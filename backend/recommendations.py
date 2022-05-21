from pymongo import MongoClient
import dotenv
import os

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import svds

from models.user import User, Rating

"""
Na wejsciu powinnny byc user i jego ratingi dla artykulow.
Moze tez byc pobrana aktywnosc uzytkownika (wyswietlenia dla artykulow).

Chcemy zrobic z tego score dla kazdej pary user-artykul. Dataframe taki.


svd - redukcja wymiarowości tak żeby dla każdego usera i artykulu było po k featurow
mozna to robic lepiej niz svd, ale trudno juz

potem mając te featurey, mozemy zrobic regresję zeby oceniło jak bardzo user pasuje do artykułu
czyli regrsja score dla tej pary user-artykul. Chcemy żeby było większe niż średnio user ma.
...

Ostatecznie dla danego usera chcemy moc wywolac metode, ktora zwroci nam liste
artykulow, ktore powinny sie mu podobac (wykluczając te, ktore juz oceniali).

Taką listę najlepiej zapisać w dokumencie usera żeby nie wołać funkcji cały czas.
"""


class Recommendations:
    def __init__(self, user_ids, article_ids):
        self.users = {user_ids[i]: i for i in range(len(user_ids))}
        self.user_ids = user_ids
        self.articles = {article_ids[i]: i for i in range(len(article_ids))}
        self.article_ids = article_ids

        self.df = pd.DataFrame(columns=['user_id', 'article_id', 'score'])
        self.matrix = None
        self.article_features = None
        self.user_features = None

    def add_user_score(self, user_id, scores):
        for article_id, score in scores:
            self.df.loc[len(self.df)] = [user_id, article_id, score]

    def get_avg_score(self, per=None):
        if per is None:
            return self.df.score.mean()
        elif per == 'user':
            groupby_col = 'user_id'
        elif per == 'article':
            groupby_col = 'article_id'
        else:
            raise ValueError('per must be one of: user, article or None')

        return self.df.groupby(groupby_col).mean()['score'].to_dict()

    def build_matrix(self):
        self.df['user_no'] = self.df['user_id'].map(self.users)
        self.df['article_no'] = self.df['article_id'].map(self.articles)

        self.matrix = sparse.coo_matrix(
            (self.df.score, (self.df.user_no, self.df.article_no)),
            shape=(len(self.articles), len(self.users)),
            dtype=np.float32).tocsr()

    def build_svd(self, k=5):
        u, s, vt = svds(self.matrix, k)

        v_norms = np.linalg.norm(vt.T, axis=1, keepdims=True)
        v_norms[v_norms == 0] = 1
        self.article_features = vt.T / v_norms

        u_norms = np.linalg.norm(u, axis=1, keepdims=True)
        u_norms[u_norms == 0] = 1
        self.user_features = u / u_norms

    def get_user_recommendations(self, user_id, n=10, unseen_only=True):
        user_no = self.users[user_id]
        user_features = self.user_features[user_no]

        matches = self.article_features @ user_features
        if unseen_only:
            unseen = self.matrix[user_no].toarray().flatten() == 0
            matches = matches[unseen]

        rec_article_nos = np.argsort(-matches)[:n]

        return [self.article_ids[x] for x in rec_article_nos]


if __name__ == '__main__':
    # init db connection
    dotenv.load_dotenv()
    client = MongoClient(os.environ["FLASK_MONGO_URI"])
    db = client.get_default_database()
    users = db.get_collection("users")
    articles = db.get_collection("articles")

    # Init the recommender
    user_ids = [user['user_id'] for user in users.find()]
    article_ids = [article['article_id'] for article in articles.find()]
    R = Recommendations(user_ids, article_ids)

    # load all users' ratings
    for user_ratings in users.find({}, {"user_id": True, 'ratings': True}):
        user_id = user_ratings['user_id']
        ratings = [(r['article_id'], r['grade']) for r in user_ratings.get('ratings')]
        print(user_id, ratings)
        R.add_user_score(user_id, ratings)

    # build
    R.build_matrix()
    R.build_svd(k=2)

    # get recommendations for each user TODO and save them
    for user in user_ids:
        print(user, R.get_user_recommendations(user, n=20))


