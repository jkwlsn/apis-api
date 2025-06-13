"""Utility class to hash passwords"""

import bcrypt


class PasswordHasher:
    """Hashes and verifies passwords using Bcrypt"""

    @classmethod
    def hash(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @classmethod
    def verify(cls, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
