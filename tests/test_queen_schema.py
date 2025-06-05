"""Test suite for queen schema"""

import pytest
from pydantic import ValidationError

from schemas.queen import QueenCreate, QueenRead


class TestQueenSchema:
    def test_queen_create_valid(self) -> None:
        """Creates a valid queen"""
        test_data: dict = {"colour": "Yellow", "clipped": True, "colony_id": 1}
        queen = QueenCreate(**test_data)
        assert queen.colour == "Yellow"
        assert queen.clipped is True
        assert queen.colony_id == 1

    def test_queen_create_missing_field(self) -> None:
        """Fail as no colony_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            QueenCreate()
        assert "colony" in str(exc_info.value)

    def test_queen_read_valid(self) -> None:
        """Reads valid queen"""
        test_data: dict = {
            "queen_id": 1,
            "colour": "Yellow",
            "clipped": True,
            "colony_id": 1,
        }
        queen = QueenRead(**test_data)
        assert queen.queen_id == 1
        assert queen.colour == "Yellow"
        assert queen.clipped is True
        assert queen.colony_id == 1

    def test_queen_read_invalid_id_type(self) -> None:
        """Fails as queen id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            QueenRead(queen_id="not-an-int", colour="Yellow", clipped=True, colony_id=1)
        assert "queen_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
