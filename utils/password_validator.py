"""Password Validator utility class"""


class PasswordValidator:
    MIN_LENGTH: int = 10
    MAX_LENGTH: int = 40

    @classmethod
    def validate(cls, password: str) -> bool:
        return cls.MIN_LENGTH <= len(password) <= cls.MAX_LENGTH
