"""Test suite for hive schema"""

import pytest
from pydantic import ValidationError

from schemas.hive import HiveCreate, HiveRead


class TestHiveSchema:
    def test_hive_create_valid(self) -> None:
        """Creates a valid hive"""
        test_data = {"name": "Hive 1", "apiary_id": 1}
        hive = HiveCreate(**test_data)
        assert hive.name == "Hive 1"

    def test_hive_create_missing_field(self) -> None:
        """Fail as no name provided"""
        with pytest.raises(ValidationError) as exc_info:
            HiveCreate()  # No 'name' provided
        assert "name" in str(exc_info.value)

    def test_hive_read_valid(self) -> None:
        """Reads valid hive"""
        test_data = {
            "hive_id": 1,
            "name": "Hive 1",
            "apiary_id": 1,
        }
        hive = HiveRead(**test_data)
        assert hive.hive_id == 1
        assert hive.name == "Hive 1"
        assert hive.apiary_id == 1

    def test_hive_read_invalid_id_type(self) -> None:
        """Fails as hive id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            HiveRead(hive_id="not-an-int", name="Hive 1", apiary_id=1)
        assert "id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
