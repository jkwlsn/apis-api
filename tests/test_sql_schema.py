"""Test seeding the database with schema.sql"""

import datetime
import zoneinfo

import pytest

from db.database_configuration import DatabaseConfiguration
from db.database_connection import DatabaseConnection


@pytest.fixture
def db() -> DatabaseConnection:
    config: DatabaseConfiguration = DatabaseConfiguration()

    db = DatabaseConnection(config=config)
    db.connect()
    db.seed("./sql/schema.sql")
    db.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s);", ["jake", "password"]
    )
    db.execute(
        "INSERT INTO apiaries (name, location, user_id) VALUES (%s, %s, %s);",
        ["Flowery Field", "123 Example Road, Kent", 1],
    )
    db.execute("INSERT INTO hives (name, apiary_id) VALUES (%s, %s);", ["Hive 1", 1])
    db.execute("INSERT INTO colonies (hive_id) VALUES (%s);", [1])
    db.execute(
        "INSERT INTO queens (colour, clipped, colony_id) VALUES (%s, %s, %s);",
        ["Yellow", True, 1],
    )
    db.execute(
        "INSERT INTO inspections (inspection_timestamp, colony_id) VALUES (%s, %s);",
        ["2020-06-22 19:10:25-07", 1],
    )
    db.execute(
        "INSERT INTO actions (notes, inspection_id) VALUES (%s, %s);",
        ["Added some feed", 1],
    )
    db.execute(
        "INSERT INTO observations (queenright, queen_cells, bias, brood_frames, store_frames, chalk_brood, foul_brood, varroa_count, temper, notes, inspection_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        [True, 0, True, 6, 5, False, False, 10, 5, "Happy bees!", 1],
    )
    return db


class TestSqlSchema:
    def test_users_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM users;", [])
        assert results == [{"user_id": 1, "username": "jake", "password": "password"}]

    def test_sessions_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        db.execute(
            "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s);",
            ["2020-06-22 19:10:25-07", 1],
        )
        results = db.execute("SELECT * FROM sessions;", [])
        assert results == [
            {
                "session_id": 1,
                "session_start": datetime.datetime(
                    2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
                ),
                "user_id": 1,
            }
        ]

    def test_apiaries_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM apiaries;", [])
        assert results == [
            {
                "apiary_id": 1,
                "name": "Flowery Field",
                "location": "123 Example Road, Kent",
                "user_id": 1,
            }
        ]

    def test_hives_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM hives;", [])
        assert results == [
            {
                "hive_id": 1,
                "name": "Hive 1",
                "apiary_id": 1,
            }
        ]

    def test_colonies_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM colonies;", [])
        assert results == [
            {
                "colony_id": 1,
                "hive_id": 1,
            }
        ]

    def test_queens_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM queens;", [])
        assert results == [
            {
                "queen_id": 1,
                "colour": "Yellow",
                "clipped": True,
                "colony_id": 1,
            }
        ]

    def test_inspections_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM inspections;", [])
        assert results == [
            {
                "inspection_id": 1,
                "inspection_timestamp": datetime.datetime(
                    2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
                ),
                "colony_id": 1,
            }
        ]

    def test_observations_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM observations;", [])
        assert results == [
            {
                "observation_id": 1,
                "queenright": True,
                "queen_cells": 0,
                "bias": True,
                "brood_frames": 6,
                "store_frames": 5,
                "chalk_brood": False,
                "foul_brood": False,
                "varroa_count": 10,
                "temper": 5,
                "notes": "Happy bees!",
                "inspection_id": 1,
            }
        ]

    def test_actions_table_seeded_correctly(self, db: DatabaseConnection) -> None:
        results = db.execute("SELECT * FROM actions;", [])
        assert results == [
            {"action_id": 1, "notes": "Added some feed", "inspection_id": 1}
        ]
