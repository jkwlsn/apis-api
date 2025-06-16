"""User service"""

from models.user import User
from repositories.user import UserRepository
from utils.hashing import PasswordHasher
from utils.password_validator import PasswordValidator
from utils.username_validator import UsernameValidator


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo: UserRepository = repo

    def create_user(self, username: str, password: str) -> User | None:
        """Creates a new user in the database if the user doesn't already exist"""
        password_validator = PasswordValidator()
        username_validator = UsernameValidator()
        password_hasher = PasswordHasher()
        normalised_username = username.strip().lower()

        if password_validator.validate(password) is False:
            raise ValueError("Password invalid")

        if username_validator.validate(username) is False:
            raise ValueError("Username invalid")

        if self.find_user_by_username(normalised_username):
            raise ValueError("Username taken")

        hashed_password = password_hasher.hash(password)

        return self.repo.create(normalised_username, hashed_password)

    def find_user_by_user_id(self, user_id: int) -> User | None:
        return self.repo.find_by_user_id(user_id=user_id)

    def find_user_by_username(self, username: str) -> User | None:
        return self.repo.find_by_username(username=username)
