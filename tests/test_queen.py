"""Pytest module for testing the Queen class"""

import pytest

from lib.queen import Queen


class TestQueen:
    def test_queen_instance_constructs(self) -> None:
        """Test queen constructs with queen_id and colony_id."""
        queen_1: type[Queen] = Queen(1, "Yellow", True, 1)
        assert queen_1.queen_id == 1
        assert queen_1.colour == "Yellow"
        assert queen_1.clipped is True
        assert queen_1.colony_id == 1

    def test_queen_instance_pretty_prints(self) -> None:
        """Test __str__ dunder method pretty prints queen instance."""
        queen_1: type[Queen] = Queen(1, "Yellow", True, 1)
        assert str(queen_1) == "Queen(1, Yellow, True, 1)"

    def test_queen_instances_are_equal(self) -> None:
        """Test __eq__ dunder method is true"""
        queen_1: type[Queen] = Queen(1, "Yellow", True, 1)
        queen_2: type[Queen] = Queen(1, "Yellow", True, 1)
        assert queen_1 == queen_2


if __name__ == "__main__":
    pytest.main()
