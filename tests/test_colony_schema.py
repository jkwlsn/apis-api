"""Test suite for colony schema"""

import pytest
from pydantic import ValidationError

from schemas.colony import ColonyCreate, ColonyRead


class TestColonySchema:
    def test_colony_create_valid(self) -> None:
        """Creates a valid colony"""
        test_data = {"hive_id": 1}
        colony = ColonyCreate(**test_data)
        assert colony.hive_id == 1

    def test_colony_create_missing_field(self) -> None:
        """Fail as no hive_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            ColonyCreate()
        assert "hive" in str(exc_info.value)

    def test_colony_read_valid(self) -> None:
        """Reads valid colony"""
        test_data = {
            "colony_id": 1,
            "hive_id": 1,
        }
        colony = ColonyRead(**test_data)
        assert colony.colony_id == 1
        assert colony.hive_id == 1

    def test_colony_read_invalid_id_type(self) -> None:
        """Fails as colony id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            ColonyRead(colony_id="not-an-int", hive_id=1)
        assert "colony_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
