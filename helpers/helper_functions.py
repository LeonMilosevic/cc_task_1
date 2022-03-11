import pandas as pd


def false_value_count(total_value_count: pd.Series, positive_value_count: int) -> int:
    return total_value_count.size - positive_value_count.sum()


def difference_count(df_1: pd.DataFrame, df_2: pd.DataFrame) -> int:
    return df_1.shape[0] - df_2.shape[0]