import pandas as pd
from helpers.helper_functions import false_value_count
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


def deduplication(df: pd.DataFrame, by_column: list) -> pd.DataFrame:
    x = df.copy()

    x = x.drop_duplicates(by_column)

    logging.info(f"Count of duplicate records: {df.shape[0] - x.shape[0]}")

    return x


def remove_out_of_range_dates(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    x = df.copy()

    x[column_name] = pd.to_datetime(x[column_name])

    x = x[(x[column_name] > '2000-01-01') & (x[column_name] < pd.datetime.now())]

    logging.info(f"Total count of out of date range removed in {column_name} is: {df.shape[0] - x.shape[0]}")

    return x


def outliers_count(df: pd.DataFrame, column_name: str) -> None:
    x = df.copy()

    x[column_name] = pd.to_numeric(x[column_name])
    is_outlier = np.abs(stats.zscore(x[column_name]) < 3)  # using 3 STD to determine if it is outlier

    false_count = false_value_count(x[column_name], is_outlier)

    logging.info(f"Total count of outliers in {column_name} is: {false_count}")


def remove_records_if_negative_value(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    x = df.copy()

    x[column_name] = pd.to_numeric(x[column_name])

    x = x[x[column_name] >= 0]

    logging.info(f"Total count of negative values found in {column_name} is: {df.shape[0] - x.shape[0]}")

    return x


def ensure_quality(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()

    x = remove_null(x, ['id', 'ticket_id', 'created_at', 'replies'])

    x = deduplication(x)

    x = remove_out_of_range_dates(x, 'created_at')

    x = remove_records_if_negative_value(x, 'replies')

    outliers_count(x, 'replies')

    return x


