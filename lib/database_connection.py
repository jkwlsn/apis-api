"""Uses configuration values to connect to database via psycopg"""

import psycopg
import os
from psycopg.rows import dict_row

from lib.database_configuration import DatabaseConfiguration


class DatabaseConnection:
    def __init__(self, **kwargs) -> None:
        self.connection = None
        self.db = DatabaseConfiguration()
        self.host = kwargs.get("host", self.db.host)
        self.port = kwargs.get("port", self.db.port)
        self.user = kwargs.get("user", self.db.user)
        self.password = kwargs.get("password", self.db.password)
        self.dbname = kwargs.get("dbname", self.db.dbname)

    def _build_conn_string(self) -> str:
        return f"host={self.host} port={self.port} user={self.user} password={self.password} dbname={self.dbname}"

    def connect(self) -> None:
        """Open a connection to the database"""
        try:
            self.connection = psycopg.connect(
                self._build_conn_string(),
                row_factory=dict_row,
            )
        except psycopg.OperationalError as e:
            raise Exception(f"Couldn't connect to {self.dbname}: {e}")

    def close(self) -> None:
        """Close the database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()

    def execute(self, query, params: list | tuple = ()) -> list | None:
        if self.connection and not self.connection.closed:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall() if cursor.description else None
        return None

    def seed(self, sql_filename: str) -> None:
        if not os.path.isfile(sql_filename):
            raise Exception(f"{sql_filename} does not exist")
        with open(sql_filename, "r") as file:
            sql = file.read()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
