import datetime as dt
import pandas as pd


def get_tickets_by_date(df: pd.DataFrame, date: str) -> pd.DataFrame:
    x = df.copy()

    x['updated_at_date'] = x['updated_at'].dt.date

    return x[x['updated_at_date'] == date]


def keep_latest_ticket_by_date(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()

    return x.sort_values('updated_at')\
        .drop_duplicates(['id', 'ticket_id', 'created_at', 'updated_at_date'], keep="last")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    date = dt.datetime.strptime('2022-03-05', '%Y-%m-%d').date()

    x = df.copy()

    x = get_tickets_by_date(x, date)
    x = keep_latest_ticket_by_date(x)

    return pd.DataFrame({'date': date, 'replies_sum': x['replies'].sum()}, index=[0])
