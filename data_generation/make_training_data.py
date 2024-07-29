import logging

import psycopg

from settings import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASS,
    DATABASE_PORT,
    DATABASE_USER,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL)


def write_training_data_batch(results: list[tuple]):
    connection = psycopg.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    try:
        with connection.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO training_data (integrand, integral, success) "
                "VALUES (%s, %s, %s) "
                "ON CONFLICT DO NOTHING",
                results,
            )
            connection.commit()
            logging.info("Wrote %d rows.", len(results))
    except psycopg.DatabaseError as e:
        logger.error("Error writing training data: %s", e)
    finally:
        connection.close()
