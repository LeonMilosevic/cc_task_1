from data_quality import quality_check
import datetime as dt
from helpers import helper_functions
import pandas as pd
import pytest


def test_remove_out_of_range_dates():
    df = pd.DataFrame({
        "ticket_id": [1, 2, 3],
        "created_at": pd.to_datetime(["2022-03-03T15:20:17", "1994-01-01T15:20:17", "2022-03-10T15:20:17"])
    })
    start_date = dt.datetime.strptime('2000-01-01', '%Y-%m-%d').date()

    x = quality_check.remove_out_of_range_dates(df, 'created_at', start_date)

    assert len(x) == 2


def test_remove_records_if_negative_value():
    df = pd.DataFrame({
        "ticket_id": [1, 2, 3],
        "replies": [-1, 0, 1]
    })

    x = quality_check.remove_records_if_negative_value(df, 'replies')

    assert len(x) == 2


def test_get_tickets_by_date():
    date = dt.datetime.strptime('2022-03-05', '%Y-%m-%d').date()
    df = pd.DataFrame({
        "ticket_id": [1, 2, 3],
        "updated_at": pd.to_datetime(["2022-03-05T15:20:17", "2022-03-05T15:20:17", "2022-03-10T15:20:17"])
    })

    x = helper_functions.get_tickets_by_date(df, date)

    assert len(x) == 2


def test_keep_latest_ticket_by_date():
    df = pd.DataFrame({
        "id": [1, 1, 1],
        "ticket_id": [1, 1, 1],
        "created_at": pd.to_datetime(["2022-03-05T15:20:00", "2022-03-05T15:20:00", "2022-03-05T15:20:00"]),
        "updated_at": pd.to_datetime(["2022-03-05T16:00:00", "2022-03-05T17:00:00", "2022-03-10T18:00:00"]),
        "updated_at_date": ['2022-03-05', '2022-03-05', '2022-03-05']
    })

    x = helper_functions.keep_latest_ticket_by_date(df)

    assert x.updated_at.values[0] == pd.to_datetime("2022-03-10T18:00:00")


