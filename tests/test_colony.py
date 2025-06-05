"""Pytest module for testing the Colony class"""

import pytest

from models.colony import Colony


class TestColony:
    def test_colony_instance_constructs(self) -> None:
        """Test colony constructs with colony_id and hive_id."""
        colony_1: type[Colony] = Colony(1, 1)
        assert colony_1.colony_id == 1
        assert colony_1.hive_id == 1

    def test_colony_instance_pretty_prints(self) -> None:
        """Test __str__ dunder method pretty prints colony instance."""
        colony_1: type[Colony] = Colony(1, 1)
        assert str(colony_1) == "Colony(1, 1)"

    def test_colony_instances_are_equal(self) -> None:
        """Test __eq__ dunder method is true"""
        colony_1: type[Colony] = Colony(1, 1)
        colony_2: type[Colony] = Colony(1, 1)
        assert colony_1 == colony_2


if __name__ == "__main__":
    pytest.main()
