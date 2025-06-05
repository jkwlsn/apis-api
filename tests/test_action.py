"""Pytest module for testing the Action class"""

import pytest

from models.action import Action


@pytest.fixture
def test_action() -> Action:
    return Action(1, "Example notes", 1)


@pytest.fixture
def test_action_2() -> Action:
    return Action(1, "Example notes", 1)


class TestAction:
    def test_action_instance_constructs(self, test_action: Action) -> None:
        """Test action constructs with action_id, notes, and inspection_id"""
        assert test_action.action_id == 1
        assert test_action.notes == "Example notes"
        assert test_action.inspection_id == 1

    def test_action_instance_pretty_prints(self, test_action: Action) -> None:
        """Test __str__ dunder method pretty prints action instance."""
        assert str(test_action) == "Action(1, Example notes, 1)"

    def test_action_instances_are_equal(
        self, test_action: Action, test_action_2: Action
    ) -> None:
        """Test __eq__ dunder method is true"""
        assert test_action == test_action_2


if __name__ == "__main__":
    pytest.main()
