"""Integration tests for PostgreSQL database connection."""

from collections.abc import Generator

import pytest

from db.database_configuration import DatabaseConfiguration
from db.database_connection import DatabaseConnection


@pytest.fixture(scope="module")
def db() -> Generator[DatabaseConnection, None, None]:
    """Provides a connected DatabaseConnection instance for tests."""
    config: DatabaseConfiguration = DatabaseConfiguration(".env")
    db: DatabaseConnection = DatabaseConnection(config)
    db.connect()
    yield db
    db.close()


def test_valid_connection_configuration(db: DatabaseConnection) -> None:
    assert db.connection is not None
    assert db.connection.closed is False


def test_valid_seed_data(db: DatabaseConnection) -> None:
    """Seed the database and verify data is inserted."""
    db.seed("seeds/valid_test_data.sql")
    results: list[dict] = db.execute("SELECT * FROM test_seed_data WHERE id = 1;", [])
    assert results == [{"id": 1, "name": "jake"}]
    db.execute("TRUNCATE TABLE test_seed_data RESTART IDENTITY CASCADE;", [])


def test_invalid_seed_filename(db: DatabaseConnection) -> None:
    """Seeding with a missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError) as excinfo:
        db.seed("seeds/nonexistent_seed.sql")
    assert "does not exist" in str(excinfo.value)


def test_close_connection(db: DatabaseConnection) -> None:
    """Closing the connection should set connection.closed to True."""
    assert db.connection.closed is False
    db.close()
    assert db.connection.closed is True


def test_invalid_connection_configuration() -> None:
    """Connecting with invalid credentials should raise ConnectionError."""
    config: DatabaseConfiguration = DatabaseConfiguration()
    config.host = "invalid_host"
    config.port = "5432"
    config.dbname = "nonexistent_db"
    config.user = "invalid_user"
    config.password = "invalid_password"
    config.url = (
        f"host={config.host} port={config.port} "
        f"user={config.user} password={config.password} dbname={config.dbname}"
    )

    db: DatabaseConnection = DatabaseConnection(config)
    with pytest.raises(ConnectionError) as excinfo:
        db.connect()
    assert "Couldn't connect" in str(excinfo.value)


def test_execute_without_connection() -> None:
    """Executing without connecting should raise ConnectionError."""
    config: DatabaseConfiguration = DatabaseConfiguration(".env")
    db: DatabaseConnection = DatabaseConnection(config)
    with pytest.raises(ConnectionError) as excinfo:
        db.execute("SELECT 1;", [])
    assert "No connection to" in str(excinfo.value)


def test_seed_without_connection() -> None:
    """Seeding without connecting should raise ConnectionError."""
    config: DatabaseConfiguration = DatabaseConfiguration(".env")
    db: DatabaseConnection = DatabaseConnection(config)
    with pytest.raises(ConnectionError) as excinfo:
        db.seed("seeds/valid_test_data.sql")
    assert "No connection to" in str(excinfo.value)
