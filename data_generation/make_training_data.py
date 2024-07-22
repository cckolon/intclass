import logging
import sqlite3
from time import time

from wrapt_timeout_decorator import timeout

from data_generation.generate_functions import get_multiple_functions
from data_generation.integration import integrate_functions_with_timeout
from database import verify_migrations
from settings import (
    DATA_GENERATION_BATCH_SIZE,
    DATA_GENERATION_BATCH_TIMEOUT_SECONDS,
    DATABASE_DIRECTORY,
    DATABASE_NAME,
    FUNCTION_COMPLEXITY,
    INTEGRATION_TIMEOUT,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL)


def make_training_data(num_rows: int):
    verify_migrations()
    for _ in range(num_rows // DATA_GENERATION_BATCH_SIZE):
        try:
            data = make_training_data_batch(DATA_GENERATION_BATCH_SIZE)
            write_training_data_batch(data)
        except Exception as e:  # pylint: disable=broad-except
            logging.error(
                "Failed to generate and integrate functions: %s",
                e,
            )
    data = make_training_data_batch(
        num_rows % DATA_GENERATION_BATCH_SIZE
    )
    write_training_data_batch(data)


@timeout(DATA_GENERATION_BATCH_TIMEOUT_SECONDS, use_signals=False)
def make_training_data_batch(batch_size):
    start_time = time()
    functions = get_multiple_functions(batch_size, FUNCTION_COMPLEXITY)
    results = integrate_functions_with_timeout(
        functions, INTEGRATION_TIMEOUT
    )
    end_time = time()
    logging.info(
        "Generated and integrated %d functions in %.2f seconds.",
        len(results),
        end_time - start_time,
    )
    return results


def write_training_data_batch(results: list[tuple]):
    with sqlite3.connect(
        f"{DATABASE_DIRECTORY}/{DATABASE_NAME}", timeout=10
    ) as connection:
        cursor = connection.cursor()
        cursor.executemany(
            "INSERT INTO training_data (integrand, integral, success) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT DO NOTHING",
            results,
        )
        connection.commit()
    logging.info("Wrote %d rows.", len(results))
