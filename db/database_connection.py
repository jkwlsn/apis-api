"""Uses configuration values to connect to database via psycopg"""

from pathlib import Path

import psycopg
from psycopg.abc import Query
from psycopg.rows import dict_row

from db.database_configuration import DatabaseConfiguration


class DatabaseConnection:
    def __init__(self, config: DatabaseConfiguration) -> None:
        self.db: DatabaseConfiguration = config
        self.connection = None

    def connect(self) -> None:
        """
        Open a connection to the database

        Raises:
            ConnectionError: if no connection can be made to the configured database.

        """
        try:
            self.connection = psycopg.connect(
                conninfo=self.db.url,
                row_factory=dict_row,
            )
            self.connection.autocommit = True
        except psycopg.OperationalError as e:
            error_message: str = f"Couldn't connect to {self.db.host}:{self.db.port}/{self.db.dbname}: {e}"
            raise ConnectionError(error_message) from e

    def close(self) -> None:
        """Close the database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()

    def execute(self, query: Query, params: list) -> list | None:
        """
        Execute queries on the database

        Args:
            query: SQL query formatted as a psycopg Query object
            params: a list of parameters for the query

        Returns:
            A list of results

        Raises:
            ConnectionError: if no connection can be made to the configured database.

        """
        if self.connection and not self.connection.closed:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall() if cursor.description else None
        error_message = (
            f"No connection to {self.db.host}:{self.db.port}/{self.db.dbname}"
        )
        raise ConnectionError(error_message)

    def seed(self, sql_file_name: str) -> None:
        """
        Seeds the database

        Args:
            sql_file_name: string pointing to sql seed file.

        Raises:
            ConnectionError: if no connection can be made to the configured database.
            FileNotFoundError: if sql seed file cannot be found.

        """
        if not self.connection or self.connection.closed:
            error_message = (
                f"No connection to {self.db.host}:{self.db.port}/{self.db.dbname}"
            )
            raise ConnectionError(error_message)
        sql_file_path = Path(sql_file_name)
        try:
            with sql_file_path.open() as file:
                sql: str = file.read()

            with self.connection.cursor() as cursor:
                cursor.execute(sql)

        except FileNotFoundError as e:
            error_message = f"{sql_file_name} does not exist: {e}"
            raise FileNotFoundError(error_message) from e
