import pandas as pd


def false_value_count(total_value_count: pd.Series, positive_value_count: int) -> int:
    return total_value_count.size - positive_value_count.sum()


def difference_count(df_1: pd.DataFrame, df_2: pd.DataFrame) -> int:
    return df_1.shape[0] - df_2.shape[0]


def get_tickets_by_date(df: pd.DataFrame, date: str) -> pd.DataFrame:
    x = df.copy()

    x['updated_at_date'] = x['updated_at'].dt.date

    return x[x['updated_at_date'] == pd.to_datetime(date)]


def keep_latest_ticket_by_date(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()

    return x.sort_values('updated_at').drop_duplicates(['ticket_id', 'updated_at_date'], keep="last")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    date = '2022-03-05'

    x = df.copy()

    x = get_tickets_by_date(x, date)
    x = keep_latest_ticket_by_date(x)

    return pd.DataFrame({'date': date, 'replies_sum': x['replies'].sum()})
