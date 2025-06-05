"""Pytest module for testing the Queen class"""

import pytest

from lib.queen import Queen


@pytest.fixture
def test_queen() -> Queen:
    clipped = True
    return Queen(1, "Yellow", clipped, 1)


@pytest.fixture
def test_queen_2() -> Queen:
    clipped = True
    return Queen(1, "Yellow", clipped, 1)


class TestQueen:
    def test_queen_instance_constructs(self, test_queen: Queen) -> None:
        """Test queen constructs with queen_id and colony_id."""
        assert test_queen.queen_id == 1
        assert test_queen.colour == "Yellow"
        assert test_queen.clipped is True
        assert test_queen.colony_id == 1

    def test_queen_instance_pretty_prints(self, test_queen: Queen) -> None:
        """Test __str__ dunder method pretty prints queen instance."""
        assert str(test_queen) == "Queen(1, Yellow, True, 1)"

    def test_queen_instances_are_equal(
        self, test_queen: Queen, test_queen_2: Queen
    ) -> None:
        """Test __eq__ dunder method is true"""
        assert test_queen == test_queen_2


if __name__ == "__main__":
    pytest.main()
