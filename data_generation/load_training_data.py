import sqlite3
from typing import Iterable

from datasets import Dataset

from settings import DATABASE_DIRECTORY, DATABASE_NAME


def get_data_generator(test=False):
    def generate() -> Iterable[tuple]:
        with sqlite3.connect(
            f"{DATABASE_DIRECTORY}/{DATABASE_NAME}", timeout=10
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT integrand, success FROM training_data"
            )
            for i, row in enumerate(cursor.fetchall()):
                if (i % 5 == 0 and test) or (i % 5 != 0 and not test):
                    # use 20% of the data for testing
                    yield {
                        "text": f"Is {row[0]} integrable?",
                        "label": row[1],
                    }

    return generate


success_fail_training_set = Dataset.from_generator(get_data_generator())
success_fail_test_set = Dataset.from_generator(
    get_data_generator(test=True)
)

success_fail_dataset = {
    "train": success_fail_training_set,
    "test": success_fail_test_set,
}
