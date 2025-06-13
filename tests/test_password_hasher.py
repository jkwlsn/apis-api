"""Tests for PasswordHasher class"""

from utils.hashing import PasswordHasher


def test_password_is_hashed() -> None:
    hasher = PasswordHasher
    password = "password"

    hashed_password = hasher.hash(password)

    assert hasher.verify(password, hashed_password) is True
