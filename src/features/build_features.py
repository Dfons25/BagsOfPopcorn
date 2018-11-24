from sklearn.feature_extraction.text import CountVectorizer


def bag_of_words(corpus, max_words):
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None,
                                 max_features = max_words)
    return vectorizer.fit_transform(corpus)
