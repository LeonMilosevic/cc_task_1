import datetime as dt
import pandas as pd
import logging
from scipy import stats
import numpy as np


# extract tests:
# - test for completeness (check if id and ticket_id is not null, replies is not null, created_at is not null.)
# - test for accuracy (is id always a number? is ticket id always a number? is created_at having normal date range? Is replies not skewed? Does reply have negative values?)
# - mention consistency (are current values similar to the ones from other runs?) in better approach
# - validity (is created_at always a date, is reply always a number)
# - uniqueness (by id and ticket_id)

def remove_null(df: pd.DataFrame, by_column: list) -> pd.DataFrame:
    x = df.copy()

    x = x.dropna(subset=by_column)
    logging.info(f"Total values remove due to missing values in {by_column}: {df.shape[0] - x.shape[0]}")

    return x


def deduplication(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()

    x = x.drop_duplicates()

    logging.info(f"Count of duplicate records: {df.shape[0] - x.shape[0]}")

    return x


def remove_out_of_range_dates(df: pd.DataFrame, column_name: str, start_date: str) -> pd.DataFrame:
    x = df.copy()

    x = x[(x[column_name].dt.date > start_date) & (x[column_name].dt.date < dt.date.today())]

    logging.info(f"Total count of out of date range removed in {column_name} is: {df.shape[0] - x.shape[0]}")

    return x


# def outliers_by_date_count(df: pd.DataFrame, column_name: str, date: str) -> None:
#     x = df.copy()
#
#     # x = x[x[column_name].dt.date == pd.to_datetime(date)]
#     x = x.drop_duplicates()
#     test = x[x['id'] == 1902140799269].sort_values('updated_at').drop_duplicates(['ticket_id', 'updated_at'], keep='last')
#     test
#     # is_outlier = np.abs(stats.zscore(x[column_name]) < 3)  # using 3 STD to determine if it is outlier
#     #
#     # false_count = false_value_count(x[column_name], is_outlier)
#     #
#     # logging.info(f"Total count of outliers in {column_name} is: {false_count}")
      # outliers_by_date_count(x, 'status_updated_at', '2022-03-06')


def remove_records_if_negative_value(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    x = df.copy()

    x = x[x[column_name] >= 0]

    logging.info(f"Total count of negative values found in {column_name} is: {df.shape[0] - x.shape[0]}")

    return x


def ensure_quality(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    start_date = dt.datetime.strptime('2010-01-01', '%Y-%m-%d').date()

    x = remove_null(x, ['id', 'ticket_id', 'created_at', 'replies'])
    x = deduplication(x)
    x = remove_out_of_range_dates(x, 'created_at', start_date)
    x = remove_records_if_negative_value(x, 'replies')

    return x


