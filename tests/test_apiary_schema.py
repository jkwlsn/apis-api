"""Test suite for apiary schema"""

import pytest
from pydantic import ValidationError

from schemas.apiary import ApiaryCreate, ApiaryRead


class TestApiarySchema:
    def test_apiary_create_valid(self) -> None:
        """Creates a valid apiary"""
        test_data = {"name": "Happy Bee Co.", "location": "Kent", "user_id": "1"}
        apiary = ApiaryCreate(**test_data)
        assert apiary.name == "Happy Bee Co."
        assert apiary.location == "Kent"

    def test_apiary_create_missing_field(self) -> None:
        """Fail as no password provided"""
        with pytest.raises(ValidationError) as exc_info:
            ApiaryCreate(apiaryname="test_apiary")
        assert "validation" in str(exc_info.value)

    def test_apiary_read_valid(self) -> None:
        """Reads valid apiary"""
        test_data = {
            "apiary_id": 1,
            "name": "Happy Bee Co.",
            "location": "Kent",
            "user_id": 1,
        }
        apiary = ApiaryRead(**test_data)
        assert apiary.apiary_id == 1
        assert apiary.name == "Happy Bee Co."
        assert apiary.location == "Kent"
        assert apiary.user_id == 1

    def test_apiary_read_invalid_id_type(self) -> None:
        """Fails as apiary id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            ApiaryRead(
                apiary_id="not-an-int", name="Happy Bee Co.", location="Kent", user_id=1
            )
        assert "id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
