import nltk
from nltk.corpus import stopwords
import pandas as pd


def remove_adjadv_from_stopwords(stopwords, pos_to_remove):
    stopwords_no_adjadv = []
    for w, pos_tag in stopwords:
        if pos_tag not in pos_to_remove:
            stopwords_no_adjadv.append(w)
    return stopwords_no_adjadv


def tokenize_review(review):
    return nltk.word_tokenize(review)


def remove_stopwords(review, stopwords):
    relevant_words = [w for w in review if not w in stopwords]
    return " ".join(relevant_words)


def remove_stopwords_from_corpus(corpus, stopwords):
    corpus_no_stopwords = []
    for sentence in corpus:
        tokens = tokenize_review(sentence)
        sentence_no_stops = remove_stopwords(tokens, stopwords)
        corpus_no_stopwords.append(sentence_no_stops)
    return corpus_no_stopwords


def main():
    train = pd.read_csv("../../data/processed/labeledTrainData.tsv", sep='\t', quoting=3)

    english_stopwords = stopwords.words('english')
    english_stopwords_postags = nltk.pos_tag(english_stopwords)

    # remove adjectives and adverbs from stopwords
    pos_to_remove = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
    stopwords_no_adjadv = remove_adjadv_from_stopwords(english_stopwords_postags, pos_to_remove)

    train_no_stops = remove_stopwords_from_corpus(train['review'], stopwords_no_adjadv)


if __name__ == "__main__":
    main()