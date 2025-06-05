"""Test suite for action schema"""

import pytest
from pydantic import ValidationError

from schemas.action import ActionCreate, ActionRead


class TestActionSchema:
    def test_action_create_valid(self) -> None:
        """Creates a valid action"""
        test_data: dict = {"notes": "Example notes", "inspection_id": 1}
        action = ActionCreate(**test_data)
        assert action.notes == "Example notes"
        assert action.inspection_id == 1

    def test_action_create_missing_field(self) -> None:
        """Fail as no inspection_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            ActionCreate(notes="Example notes")
        assert "inspection" in str(exc_info.value)

    def test_action_read_valid(self) -> None:
        """Reads valid action"""
        test_data: dict = {
            "action_id": 1,
            "notes": "Example notes",
            "inspection_id": 1,
        }
        action = ActionRead(**test_data)
        assert action.action_id == 1
        assert action.notes == "Example notes"
        assert action.inspection_id == 1

    def test_action_read_invalid_id_type(self) -> None:
        """Fails as action id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            ActionRead(
                action_id="not-an-int",
                notes="Example notes",
                inspection_id=1,
            )
        assert "action_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
