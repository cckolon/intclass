import logging
import os

import psycopg
import psycopg.sql

from settings import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASS,
    DATABASE_PORT,
    DATABASE_USER,
    MIGRATIONS_DIRECTORY,
)

logger = logging.getLogger(__name__)


class MigrationException(Exception):
    pass


def get_migrations():
    return os.listdir(MIGRATIONS_DIRECTORY)


def migrate_all():
    connection = psycopg.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                psycopg.sql.SQL(
                    "CREATE TABLE IF NOT EXISTS migrations ("
                    "id SERIAL PRIMARY KEY, "
                    "name TEXT NOT NULL"
                    ")"
                )
            )
            for migration in get_migrations():
                cursor.execute(
                    psycopg.sql.SQL(
                        "SELECT name FROM migrations WHERE name = %s"
                    ),
                    (migration,),
                )
                if cursor.fetchone() is None:
                    with open(
                        f"{MIGRATIONS_DIRECTORY}/{migration}",
                        "r",
                        encoding="utf-8",
                    ) as file:
                        cursor.execute(psycopg.sql.SQL(file.read()))
                    cursor.execute(
                        psycopg.sql.SQL(
                            "INSERT INTO migrations (name) VALUES (%s)"
                        ),
                        (migration,),
                    )
                    logger.info("Migration %s has been run.", migration)
            connection.commit()
    except psycopg.DatabaseError as e:
        logger.error("Error running migrations: %s", e)
    finally:
        connection.close()


def verify_migrations():
    connection = psycopg.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                psycopg.sql.SQL(
                    "CREATE TABLE IF NOT EXISTS migrations ("
                    "id SERIAL PRIMARY KEY, "
                    "name TEXT NOT NULL"
                    ")"
                )
            )
            for migration in get_migrations():
                cursor.execute(
                    psycopg.sql.SQL(
                        "SELECT name FROM migrations WHERE name = %s"
                    ),
                    (migration,),
                )
                if cursor.fetchone() is None:
                    raise MigrationException(
                        f"Migration {migration} has not been run."
                    )
    except psycopg.DatabaseError as e:
        logger.error("Error verifying migrations: %s", e)
    finally:
        connection.close()
    logger.info("All migrations have been run.")
