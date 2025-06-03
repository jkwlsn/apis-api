"""Test connection to the postgres database"""

import pytest

from lib.database_connection import DatabaseConnection


def test_invalid_connection_configuration() -> None:
    db = DatabaseConnection(host="invalid")
    with pytest.raises(Exception, match="No address associated with hostname") as e:
        db.connect()
    assert (
        str(e.value)
        == "Couldn't connect to apis_database: [Errno -5] No address associated with hostname"
    )


def test_valid_connection_configuration() -> None:
    db = DatabaseConnection()
    db.connect()
    assert db.connection.closed is False


def test_close_connection() -> None:
    db = DatabaseConnection()
    db.connect()
    assert db.connection.closed is False
    db.close()
    assert db.connection.closed is True


def test_invalid_execute() -> None:
    db = DatabaseConnection()
    assert db.execute("SELECT * FROM users;") is None


def test_invalid_seed_filename() -> None:
    db = DatabaseConnection()
    db.connect()
    with pytest.raises(Exception, match="invalid_test_filename") as e:
        db.seed("invalid_test_filename")
    assert str(e.value) == "invalid_test_filename does not exist"


def test_valid_seed_data() -> None:
    db = DatabaseConnection()
    db.connect()
    db.seed("seeds/valid_test_data.sql")
    assert db.execute("SELECT * FROM test_seed_data;") == [{"id": 1, "name": "jake"}]
