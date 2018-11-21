import pandas as pd
from bs4 import BeautifulSoup
import csv


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


# Replace the data in the column column_name by new_data
def df_replace_column(df, column_name, new_data):
    df[column_name] = new_data
    return df


# Read filepath
def read_from_csv(filepath):
    return pd.read_csv(filepath, sep='\t', quoting=3)


# Write df to filepath
def write_to_csv(df, filepath):
    df.to_csv(filepath, sep='\t', quoting=3, index=False)


# Read input_filenames in the input_folder, clean and write them to the output folder.
def create_and_write_cleaned_data_files(input_folder, input_filenames, output_folder):
    for filename in input_filenames:
        input_filepath = input_folder + "/" + filename
        output_filepath = output_folder + "/" + filename
        df = read_from_csv(input_filepath)
        df_cleaned = df_replace_column(df, 'review', reviews_remove_html(df["review"]))
        write_to_csv(df_cleaned, output_filepath)


def main():
    input_filenames = ["labeledTrainData.tsv", "testData.tsv", "unlabeledTrainData.tsv"]
    input_folder = "../../data/raw"
    output_folder = "../../data/processed"
    create_and_write_cleaned_data_files(input_folder, input_filenames, output_folder)


if __name__ == "__main__":
    main()