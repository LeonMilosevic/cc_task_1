from data_quality.quality_check import ensure_quality
from helpers.helper_functions import transform
import pandas as pd
import logging


def logger(file_name: str) -> None:
    logging.basicConfig(
        filename=f'logs/{file_name}',
        format="%(asctime)s - %(filename)s - %(message)s",
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )


def app():
    # fetch data
    data_df = pd.read_json("./source/metrics.json", lines=True)

    # ensure data quality on fetched data
    cleaned_df = ensure_quality(data_df)

    # apply business logic
    transform(cleaned_df)


if __name__ == '__main__':
    logger('data_quality_log')
    app()
