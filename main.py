import pandas as pd
import logging


def logger(file_name: str) -> None:
    logging.basicConfig(
        filename=f'logs/{file_name}', format="%(asctime)s - %(filename)s - %(message)s"
    )
    logging.getLogger().setLevel(logging.DEBUG)


def app():
    logger('data_quality_logs')
    logger('pipeline_execution_logs')

    data_df = pd.read_json("./source/metrics.json", lines=True)

    # extract tests:
    # - test for completness (check if id and ticket_id is not null, replies is not null, created_at is not null.)
    # - test for accuracy (is id always a number? is ticket id always a number? is created_at having normal date range? is replies not skewed?)
    # - mention consistency (are current values similar to the ones from other runs?) in better approach
    # - validity (is created_at always a date, is reply always a number)
    # - uniqueness (by id and ticket_id)


if __name__ == '__main__':
    app()
