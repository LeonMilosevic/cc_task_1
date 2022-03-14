import datetime as dt

from typing import List

from helpers.helper_functions import difference
import pandas as pd
import logging


def remove_null(df: pd.DataFrame, by_column: List[str]) -> pd.DataFrame:
    """Remove rows if null value is present in by_column argument.

    Args:
        df (pd.DataFrame): Dataframe on which to perform quality checks.
        by_column (list): list of columns that mustn't have null values.

    Returns:
        x (pd.DataFrame): Rows that don't contain null values in specified columns.
    """
    x = df.copy()

    x = x.dropna(subset=by_column)
    logging.info(f"Total values remove due to missing values in {by_column}: {difference(df, x)}")

    return x


def deduplication(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicates from df by considering all columns.

    Args:
        df (pd.DataFrame): Dataframe on which to perform deduplication.

    Returns:
        x (pd.DataFrame): Deduplicated dataframe.
    """
    x = df.copy()

    x = x.drop_duplicates()

    logging.info(f"Count of duplicate records: {difference(df, x)}")

    return x


def remove_out_of_range_dates(df: pd.DataFrame, column_name: str, start_date: str) -> pd.DataFrame:
    """Remove rows that have inaccurate date ranges, example: We don't want to manipulate
    data that has a date from the future, or very far back in the past.

    Args:
        df (pd.DataFrame): Dataframe on which to date range accuracy.
        column_name (str): Name of date column.
        start_date (date): Lower limit of date range.

    Returns:
        x (pd.DataFrame): Rows that qualified based on date range.
    """
    x = df.copy()

    x = x[(x[column_name].dt.date > start_date) & (x[column_name].dt.date < dt.date.today())]

    logging.info(f"Total count of out of date range removed in {column_name} is: {difference(df, x)}")

    return x


def remove_records_if_negative_value(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Remove rows if inaccurate representation of column value, example: Records that have value -1 for
    replies column.

    Args:
        df (pd.DataFrame): Dataframe on which to perform quality checks.
        column_name (str): Name of the column.

    Returns:
        x (pd.DataFrame): Rows that passed accuracy test.
    """
    x = df.copy()

    x = x[x[column_name] >= 0]

    logging.info(f"Total count of negative values found in {column_name} is: {difference(df, x)}")

    return x


def ensure_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function that calls multiple quality check functions on data.

    Args:
        df (pd.DataFrame): Dataframe on which to perform quality checks.

    Returns:
        x (pd.DataFrame): Cleaned and comforted dataframe.
    """
    x = df.copy()
    start_date = dt.datetime.strptime('2010-01-01', '%Y-%m-%d').date()
    must_not_null_columns = ['id', 'ticket_id', 'created_at', 'replies']

    x = remove_null(x, must_not_null_columns)
    x = deduplication(x)
    x = remove_out_of_range_dates(x, 'created_at', start_date)
    x = remove_records_if_negative_value(x, 'replies')

    return x


