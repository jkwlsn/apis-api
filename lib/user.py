"""User model class"""

from dataclasses import dataclass


@dataclass
class User:
    """Class models system users in the database"""

    user_id: int
    username: str
    password: str

    def __str__(self) -> str:
        return f"User({self.user_id}, {self.username}, {self.password})"
