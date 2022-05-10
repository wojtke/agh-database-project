import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import svds

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


# TODO ogarnąć żeby było indeksowane albo tym dataframem albo sparse matrix, nie obie na raz
class Recommendations:
    def __init__(self, user_ids, article_ids):
        self.users = {user_ids[i]: i for i in range(len(user_ids))}
        self.articles = {article_ids[i]: i for i in range(len(article_ids))}

        self.df = pd.DataFrame(columns=['customer_id', 'article_id', 'score'])
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
            groupby_col = 'customer_id'
        elif per == 'article':
            groupby_col = 'article_id'
        else:
            raise ValueError('per must be one of: user, article or None')

        return self.df.groupby(groupby_col).mean()['score'].to_dict()

    def build_matrix(self):
        self.df['customer_no'] = self.df['customer_id'].map(self.users)
        self.df['article_no'] = self.df['article_id'].map(self.articles)

        self.matrix = sparse.csr_matrix((self.df.score, (self.df.customer_no, self.df.article_no)), dtype=np.float32)

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

        recs = np.argsort(-(self.article_features @ user_features))
        if unseen_only:
            unseen = self.matrix[user_no].toarray().flatten() == 0

            recs = recs[unseen]

        return recs[:n]


if __name__ == '__main__':
    # TODO żeby to było pobierane z bazy danych
    users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7"]
    articles = ["article1", "article2", "article3", "article4", "article5", "article6"]
    scores = {
        "user1": [("article1", 1), ("article2", 2)],
        "user2": [("article2", 1), ("article3", 6)],
        "user3": [("article2", 8)],
        "user4": [("article3", 9), ("article4", 2), ("article5", 6), ("article6", 4)],
        "user5": [("article1", 1), ("article4", 2), ("article6", 4)],
        "user6": [("article1", 3), ("article2", 6), ("article3", 6), ("article4", 2), ("article5", 6), ("article6", 4)],
        "user7": [("article3", 6), ("article6", 9)]
    }

    R = Recommendations(users, articles)
    for user, scores in scores.items():
        R.add_user_score(user, scores)
    R.build_matrix()
    R.build_svd()

    for user in users:
        recs = R.get_user_recommendations(user)
        # TODO żeby to było zapisane do bazy danych
        print(user, np.array(articles)[recs])






