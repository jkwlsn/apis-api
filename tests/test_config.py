"""Test the configuration values are loaded from env files"""

from lib.config import DatabaseConfiguration


def test_configuration_file_exists() -> None:
    db_conf = DatabaseConfiguration()
    print(db_conf)
    assert db_conf is not None


def test_default_configuration_values() -> None:
    db_conf = DatabaseConfiguration()
    print(db_conf.__dict__)
    assert db_conf.host == "psql"
    assert db_conf.port == "5432"
    assert db_conf.user == "admin"
    assert db_conf.dbname == "apis_database"
    assert db_conf.password == "password"


def test_invalid_configuration_file() -> None:
    db_conf = DatabaseConfiguration("invalid_filename")
    print(db_conf.__dict__)
    assert db_conf.host is None
    assert db_conf.port is None
    assert db_conf.user is None
    assert db_conf.dbname is None
    assert db_conf.password is None
