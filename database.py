import logging
import os
import sqlite3

from settings import (
    DATABASE_DIRECTORY,
    DATABASE_NAME,
    MIGRATIONS_DIRECTORY,
)

logger = logging.getLogger(__name__)


class MigrationException(Exception):
    pass


def get_migrations():
    return os.listdir(MIGRATIONS_DIRECTORY)


def create_database_directory():
    if not os.path.exists(DATABASE_DIRECTORY):
        os.makedirs(DATABASE_DIRECTORY)


def migrate_all():
    create_database_directory()
    with sqlite3.connect(
        f"{DATABASE_DIRECTORY}/{DATABASE_NAME}", timeout=10
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS migrations ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL"
            ")"
        )
        for migration in get_migrations():
            cursor.execute(
                "SELECT name FROM migrations WHERE name = ?",
                (migration,),
            )
            if cursor.fetchone() is None:
                with open(
                    f"{MIGRATIONS_DIRECTORY}/{migration}",
                    "r",
                    encoding="utf-8",
                ) as file:
                    cursor.executescript(file.read())
                cursor.execute(
                    "INSERT INTO migrations (name) VALUES (?)",
                    (migration,),
                )
        connection.commit()


def verify_migrations():
    with sqlite3.connect(
        f"{DATABASE_DIRECTORY}/{DATABASE_NAME}", timeout=10
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS migrations ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL"
            ")"
        )
        for migration in get_migrations():
            cursor.execute(
                "SELECT name FROM migrations WHERE name = ?",
                (migration,),
            )
            if cursor.fetchone() is None:
                raise MigrationException(
                    f"Migration {migration} has not been run."
                )
        connection.commit()
    logger.info("All migrations have been run.")
