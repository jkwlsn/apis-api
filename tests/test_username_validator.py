"""Tests for UsernameValidator class"""

from utils.username_validator import UsernameValidator


class TestUsernameValidator:
    def test_username_valid(self) -> None:
        validator = UsernameValidator
        username = "correctusername"

        assert validator.validate(username) is True

    def test_username_too_long(self) -> None:
        validator = UsernameValidator
        username = "usernamelongerthantheabsolutemaximumnumberofcharacterswhichisforty"

        assert validator.validate(username) is False

    def test_username_too_short(self) -> None:
        validator = UsernameValidator
        username = "x"

        assert validator.validate(username) is False

    def test_username_empty(self) -> None:
        validator = UsernameValidator
        username = "        "
        assert validator.validate(username) is False

    def test_username_invalid_chars(self) -> None:
        validator = UsernameValidator
        username = "jakes!^*&($&$username"
        assert validator.validate(username) is False
