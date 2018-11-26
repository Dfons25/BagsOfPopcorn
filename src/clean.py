from sklearn.base import BaseEstimator
from clean_documents import clean_text


class ReviewCleaner(BaseEstimator):

    def clean(self, x):
        return clean_text(x)

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.apply(lambda k: self.clean(k))
