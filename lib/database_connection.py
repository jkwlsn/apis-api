"""Uses configuration values to connect to database via psycopg"""

from pathlib import Path

import psycopg
from psycopg.abc import Query
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from lib.database_configuration import DatabaseConfiguration


class DatabaseConnection:
    def __init__(self, **kwargs: str) -> None:
        self.connection: psycopg.Connection | None = None
        db: DatabaseConfiguration = DatabaseConfiguration()
        self.host: str | None = kwargs.get("host", db.host)
        self.port: str | None = kwargs.get("port", db.port)
        self.user: str | None = kwargs.get("user", db.user)
        self.password: str | None = kwargs.get("password", db.password)
        self.dbname: str | None = kwargs.get("dbname", db.dbname)

    def _build_connection_string(self) -> str:
        return make_conninfo(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
        )

    def connect(self) -> None:
        """
        Open a connection to the database

        Raises:
        ConnectionError:
        Raises ConnectionError if no connection can be made to the configured database

        """
        try:
            self.connection = psycopg.connect(
                self._build_connection_string(),
                row_factory=dict_row,
            )
        except psycopg.OperationalError as e:
            error_message = f"Couldn't connect to {self.dbname}: {e}"
            raise ConnectionError(error_message) from e

    def close(self) -> None:
        """Close the database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()

    def execute(self, query: Query, params: list | tuple = ()) -> list | None:
        if self.connection and not self.connection.closed:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall() if cursor.description else None
        return None

    def seed(self, sql_file_name: str) -> None:
        if not self.connection or self.connection.closed:
            error_message = f"Cannot connect to {self.host}:{self.port}/{self.dbname}"
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

        except psycopg.Error as e:
            error_message = f"Error executing SQL seed on {self.dbname}: {e}"
            raise RuntimeError(error_message) from e
