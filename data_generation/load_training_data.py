from typing import Iterable

import psycopg
from datasets import Dataset

from settings import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASS,
    DATABASE_PORT,
    DATABASE_USER,
)


def get_data_generator(test=False):
    def generate() -> Iterable[tuple]:
        connection = psycopg.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASS,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT integrand, success FROM training_data")
                for i, row in enumerate(cursor.fetchall()):
                    if (i % 5 == 0 and test) or (i % 5 != 0 and not test):
                        # use 20% of the data for testing
                        yield {
                            "text": f"Is {row[0]} integrable?",
                            "label": row[1],
                        }
        finally:
            connection.close()

    return generate


success_fail_training_set = Dataset.from_generator(get_data_generator())
success_fail_test_set = Dataset.from_generator(get_data_generator(test=True))

success_fail_dataset = {
    "train": success_fail_training_set,
    "test": success_fail_test_set,
}
