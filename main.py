from data_quality.quality_check import ensure_quality
from helpers.helper_functions import transform
import pandas as pd
import logging
import os


def logger(file_name: str) -> None:
    logging.basicConfig(
        filename=f'logs/{file_name}',
        format="%(asctime)s - %(filename)s - %(message)s",
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )


def app():
    CWD = os.getcwd()

    # fetch data
    data_df = pd.read_json(f"{CWD}/source/metrics.json", lines=True)

    # ensure data quality on fetched data
    data_df = ensure_quality(data_df)

    # apply business logic
    data_df = transform(data_df)

    # load to storage
    data_df.to_csv(os.path.join(f'{CWD}/storage', f'{data_df.date[0]}_replies_sum'), index=False)


if __name__ == '__main__':
    logger('data_quality_log')
    app()
