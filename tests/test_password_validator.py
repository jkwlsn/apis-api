"""Tests for PasswordValidator class"""

from utils.password_validator import PasswordValidator


class TestPasswordValidator:
    def test_password_valid(self) -> None:
        validator = PasswordValidator
        password = "passwordlongerthanten"

        assert validator.validate(password) is True

    def test_password_too_long(self) -> None:
        validator = PasswordValidator
        password = "passwordlongerthantheabsolutemaximumnumberofcharacterswhichisforty"

        assert validator.validate(password) is False

    def test_password_too_short(self) -> None:
        validator = PasswordValidator
        password = "tooshort"

        assert validator.validate(password) is False

    def test_password_empty(self) -> None:
        validator = PasswordValidator
        password = "        "
        assert validator.validate(password) is False
