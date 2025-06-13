"""UsernameValidator utility class"""


class UsernameValidator:
    MIN_LENGTH: int = 3
    MAX_LENGTH: int = 20

    @classmethod
    def validate(cls, username: str) -> bool:
        return username.isalnum() and cls.MIN_LENGTH <= len(username) <= cls.MAX_LENGTH
