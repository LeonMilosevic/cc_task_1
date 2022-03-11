from data_quality import quality_check
import pandas as pd
import pytest


def test_remove_out_of_range_dates():
    test_df = pd.DataFrame({
        "ticket_id": [1, 2, 3],
        "created_at": ["2022-03-03T15:20:17", "1994-01-01T15:20:17", "2022-03-10T15:20:17"]
    })

    # pd = remove_out_of_range_dates(x, 'created_at', start_date)
