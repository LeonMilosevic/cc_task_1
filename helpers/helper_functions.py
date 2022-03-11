import pandas as pd


def false_value_count(total_value_count: pd.Series, positive_value_count: int) -> int:
    return total_value_count.size - positive_value_count.sum()
