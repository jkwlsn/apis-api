"""Test the configuration values are loaded from env files"""

import pytest

from db.database_configuration import DatabaseConfiguration


class TestDatabaseConfiguration:
    def test_configuration_file_exists(self) -> None:
        db_conf: DatabaseConfiguration = DatabaseConfiguration()
        assert db_conf is not None

    def test_default_configuration_values(self) -> None:
        db_conf: DatabaseConfiguration = DatabaseConfiguration()
        assert db_conf.host == "localhost"
        assert db_conf.port == "5432"
        assert db_conf.user == "admin"
        assert db_conf.dbname == "apis_database"
        assert db_conf.password == "password"

    def test_invalid_configuration_file(self) -> None:
        db_conf: DatabaseConfiguration = DatabaseConfiguration("invalid_filename.txt")
        assert db_conf.host is None
        assert db_conf.port is None
        assert db_conf.user is None
        assert db_conf.dbname is None
        assert db_conf.password is None


if __name__ == "__main__":
    pytest.main()
