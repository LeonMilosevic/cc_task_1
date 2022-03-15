import datetime as dt
from typing import List

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


def keep_latest_updated_ticket(df: pd.DataFrame, unique_identifiers: List[str]) -> pd.DataFrame:
    x = df.copy()

    return x.sort_values('updated_at').drop_duplicates(unique_identifiers, keep='last')


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function that calls multiple transformation functions on the data.

    Args:
        df (pd.DataFrame): Dataframe on which to perform transformations.

    Returns:
        x (pd.DataFrame): date and sum of replies for that date.
    """
    date_wanted = dt.datetime.strptime('2022-03-05', '%Y-%m-%d').date()
    unique_identifiers = ['id', 'ticket_id', 'created_at']

    x = df.copy()

    df_for_date_wanted = x[x['updated_at'].dt.date == date_wanted]
    df_history = x[x['updated_at'].dt.date < date_wanted]

    df_for_date_wanted = keep_latest_updated_ticket(df_for_date_wanted, unique_identifiers)
    df_history = keep_latest_updated_ticket(df_history, unique_identifiers)

    df_for_date_wanted = pd.merge(df_for_date_wanted, df_history[['id', 'ticket_id', 'replies']], how='left',
                                  on=['id', 'ticket_id']) \
        .dropna(subset=['replies_y'])

    df_for_date_wanted['replies_for_03_05'] = df_for_date_wanted['replies_x'] - df_for_date_wanted['replies_y']

    return pd.DataFrame({'date': date_wanted, 'replies_sum': df_for_date_wanted['replies_for_03_05'].sum()}, index=[0])
