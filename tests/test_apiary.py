"""Pytest module for testing the Apiary class"""

import pytest
from models.apiary import Apiary


class TestApiary:
    def test_apiary_instance_constructs(self) -> None:
        """Test apiary constructs with apiary_id, apiary name, location, and user_id."""
        apiary_1 = Apiary(1, "Happy Bee Co.", "Kent", 1)
        assert apiary_1.apiary_id == 1
        assert apiary_1.name == "Happy Bee Co."
        assert apiary_1.location == "Kent"
        assert apiary_1.user_id == 1

    def test_apiary_instance_pretty_prints(self) -> None:
        """Test __str__ dunder method pretty prints apiary instance."""
        apiary_1 = Apiary(1, "Happy Bee Co.", "Kent", 1)
        assert str(apiary_1) == "Apiary(1, Happy Bee Co., Kent, 1)"

    def test_apiary_instances_are_equal(self) -> None:
        """Test __eq__ dunder method is true"""
        apiary_1 = Apiary(1, "Happy Bee Co.", "Kent", 1)
        apiary_2 = Apiary(1, "Happy Bee Co.", "Kent", 1)
        assert apiary_1 == apiary_2


if __name__ == "__main__":
    pytest.main()
