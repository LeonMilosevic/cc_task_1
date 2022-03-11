from data_quality import quality_check
from helpers import helper_functions
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
    data_df = pd.read_json("./source/metrics.json", lines=True, dtype=object)

    quality_check.deduplication(data_df, ['id', 'ticket_id'])


if __name__ == '__main__':
    logger('data_quality_log')
    app()
