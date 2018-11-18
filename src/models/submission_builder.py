import pandas as pd


# create data to submit in kaggle
def df_to_submit(id_column_name, predictions_column_name, predictions):
    return pd.DataFrame({id_column_name: list(range(1, len(predictions)+1)),
                         predictions_column_name: predictions})


# write csv to submit in kaggle
def write_submission(filename, df):
    df.to_csv(filename, index=False)


def main():
    # create a sample data frame
    data = [[0, 'mad'], [1, 'funny'], [0, 'ugly']]
    df = pd.DataFrame(data, columns=['sentiment', 'review'])
    # write submission file
    submission_filename = '../../data/submissions/sampleSubmission.csv'
    submission_df = df_to_submit('id', 'sentiment', df['sentiment'])
    write_submission(submission_filename, submission_df)


if __name__ == "__main__":
    main()
