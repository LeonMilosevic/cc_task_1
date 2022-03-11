import pandas as pd
from helpers.helper_functions import false_value_count
import logging
from scipy import stats
import numpy as np


# extract tests:
# - test for completness (check if id and ticket_id is not null, replies is not null, created_at is not null.)
# - test for accuracy (is id always a number? is ticket id always a number? is created_at having normal date range? Is replies not skewed? Does reply have negative values?)
# - mention consistency (are current values similar to the ones from other runs?) in better approach
# - validity (is created_at always a date, is reply always a number)
# - uniqueness (by id and ticket_id)

def deduplication(df: pd.DataFrame, by_column: list) -> pd.DataFrame:
    x = df.copy()

    x = x.drop_duplicates(by_column)

    logging(f"Count of duplicate records: {df.shape[0] - x.shape[0]}")

    return x


def is_null_count(df: pd.DataFrame, column_name: str) -> None:
    null_count = df[column_name].isna().sum()
    logging.info(f"Total count of null values in {column_name} is: {null_count} ")


def not_number_count(df: pd.DataFrame, column_name: str) -> None:
    false_count = false_value_count(df[column_name], df[column_name].str.isnumeric())

    logging.info(f"Total count of non numeric values in {column_name} is: {false_count}")


def date_out_of_range_count(df: pd.DataFrame, column_name: str) -> None:
    x = df.copy()

    x[column_name] = pd.to_datetime(x[column_name])
    is_date_out_of_range = x[column_name].between('2000-01-01', pd.datetime.now())

    false_count = false_value_count(x[column_name], is_date_out_of_range)

    logging.info(f"Total count of out of date range in {column_name} is: {false_count}")


def outliers_count(df: pd.DataFrame, column_name: str) -> None:
    x = df.copy()

    x[column_name] = pd.to_numeric(x[column_name])
    is_outlier = np.abs(stats.zscore(x[column_name]) < 3)  # using 3 STD to determine if it is outlier

    false_count = false_value_count(x[column_name], is_outlier)

    logging.info(f"Total count of outliers in {column_name} is: {false_count}")


def negative_count(df: pd.DataFrame, column_name: str) -> None:
    x = df.copy()

    x[column_name] = pd.to_numeric(x[column_name])

    is_positive = (x[column_name] >= 0)

    false_count = false_value_count(x[column_name], is_positive)

    logging.info(f"Total count of negative values in {column_name} is: {false_count}")


