"""Pytest module for testing the Hive class"""

import pytest

from models.hive import Hive


class TestHive:
    def test_hive_instance_constructs(self) -> None:
        """Test hive constructs with hive_id, hive name, and apiary_id."""
        hive_1: type[Hive] = Hive(1, "Hive 1", 1)
        assert hive_1.hive_id == 1
        assert hive_1.name == "Hive 1"
        assert hive_1.apiary_id == 1

    def test_hive_instance_pretty_prints(self) -> None:
        """Test __str__ dunder method pretty prints hive instance."""
        hive_1: type[Hive] = Hive(1, "Hive 1", 1)
        assert str(hive_1) == "Hive(1, Hive 1, 1)"

    def test_hive_instances_are_equal(self) -> None:
        """Test __eq__ dunder method is true"""
        hive_1: type[Hive] = Hive(1, "Hive 1", 1)
        hive_2: type[Hive] = Hive(1, "Hive 1", 1)
        assert hive_1 == hive_2


if __name__ == "__main__":
    pytest.main()
