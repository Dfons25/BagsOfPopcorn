import pandas as pd
from bs4 import BeautifulSoup


# Removes htlm tags from a review
def review_remove_html(review):
    return BeautifulSoup(review, 'lxml').get_text()


# Removes htlm tags from reviews
def reviews_remove_html(reviews):
    reviews_no_html = []
    num_reviews = len(reviews.index)
    for i in range(0, num_reviews):
        reviews_no_html.append(review_remove_html(reviews[i]))
    return reviews_no_html


def main():
    # read training data
    train = pd.read_csv("../../data/raw/labeledTrainData.tsv", sep='\t')
    reviews_cleaned = reviews_remove_html(train["review"])

    # build clean train data
    train_cleaned = pd.DataFrame({'id':  train["id"], 'sentiment': train['sentiment'], 'review': reviews_cleaned})
    # write clean train data to csv
    train_cleaned.to_csv("../../data/processed/labeledTrainData.tsv", sep='\t', index=False)


if __name__ == "__main__":
    main()