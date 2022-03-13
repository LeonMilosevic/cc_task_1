import datetime as dt
import pandas as pd


def difference(df_1: pd.DataFrame, df_2: pd.DataFrame) -> int:
    """Gets the length difference between two dataframes.

    Args:
        df_1 (pd.DataFrame)
        df_2 (pd.DataFrame)

    Returns:
        x (int): Difference between two dataframes as int.
    """
    return len(df_1) - len(df_2)


def get_tickets_by_date(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Returns tickets for a given date based on date argument. Example: return all tickets that were updated
    on 5th of March.

    Args:
        df (pd.DataFrame):
        date (pd.DataFrame): date to return.

    Returns:
        x (pd.DataFrame): Dataframe consisting of rows only on specified date.
    """

    return df[df['updated_at'].dt.date == date]


def keep_latest_ticket_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Removes tickets that were updated multiple times per day, and keeps the last occurrence of given ticket.
    Example: same ticket was updated 3 times in a day, will keep only last updated one.

    Args:
        df (pd.DataFrame):

    Returns:
        pd.DataFrame: Dataframe consisting of tickets with last occurrence for that day.
    """
    x = df.copy()

    return x.sort_values('updated_at')\
        .drop_duplicates(['id', 'ticket_id', 'created_at'], keep="last")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function that calls multiple transformation functions on the data.

    Args:
        df (pd.DataFrame): Dataframe on which to perform transformations.

    Returns:
        x (pd.DataFrame): date and sum of replies for that date.
    """
    date = dt.datetime.strptime('2022-03-05', '%Y-%m-%d').date()

    x = df.copy()

    x = get_tickets_by_date(x, date)
    x = keep_latest_ticket_by_date(x)

    return pd.DataFrame({'date': date, 'replies_sum': x['replies'].sum()}, index=[0])
