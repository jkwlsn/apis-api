"""Test connection to the postgres database"""

import pytest

from db.database_connection import DatabaseConnection


class TestDatabaseConnection:
    def test_invalid_connection_configuration(self) -> None:
        db = DatabaseConnection(host="invalid")
        with pytest.raises(ConnectionError) as e:
            db.connect()
        assert (
            str(e.value)
            == """Couldn't connect to invalid:5432/apis_database: [Errno -2] Name or service not known"""
        )

    def test_valid_connection_configuration(self) -> None:
        db = DatabaseConnection()
        db.connect()
        assert db.connection.closed is False

    def test_close_connection(self) -> None:
        db = DatabaseConnection()
        db.connect()
        assert db.connection.closed is False
        db.close()
        assert db.connection.closed is True

    def test_invalid_execute(self) -> None:
        db = DatabaseConnection()
        with pytest.raises(ConnectionError) as e:
            db.execute("SELECT * FROM users;", [])
        assert str(e.value) == "No connection to localhost:5432/apis_database"

    def test_invalid_seed_filename(self) -> None:
        db = DatabaseConnection()
        db.connect()
        with pytest.raises(FileNotFoundError, match="invalid_test_filename") as e:
            db.seed("invalid_test_filename")
        assert (
            str(e.value)
            == "invalid_test_filename does not exist: [Errno 2] No such file or directory: 'invalid_test_filename'"
        )

    def test_invalid_connection_seed(self) -> None:
        db = DatabaseConnection()
        with pytest.raises(ConnectionError) as e:
            db.seed("seeds/valid_test_data.sql")
        assert str(e.value) == "No connection to localhost:5432/apis_database"

    def test_valid_seed_data(self) -> None:
        db = DatabaseConnection()
        db.connect()
        db.seed("seeds/valid_test_data.sql")
        results = db.execute("SELECT * FROM test_seed_data;", [])
        assert results == [{"id": 1, "name": "jake"}]


if __name__ == "__main__":
    pytest.main()
