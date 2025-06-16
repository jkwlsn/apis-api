"""User service"""

from models.user import User
from repositories.user import UserRepository
from utils.hashing import PasswordHasher
from utils.password_validator import PasswordValidator
from utils.username_validator import UsernameValidator


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo: UserRepository = repo
        self.username_invalid = "Username invalid"
        self.password_invalid = "Password invalid"  # noqa: S105
        self.username_taken = "Username already taken"
        self.user_does_not_exist = "User does not exist"

    def create_user(self, username: str, password: str) -> User | None:
        """Creates a new user in the database if the user doesn't already exist"""
        password_validator = PasswordValidator()
        username_validator = UsernameValidator()
        password_hasher = PasswordHasher()
        normalised_username = username.strip().lower()

        if password_validator.validate(password) is False:
            raise ValueError(self.password_invalid)

        if username_validator.validate(username) is False:
            raise ValueError(self.username_invalid)

        if self.find_user_by_username(normalised_username):
            raise ValueError(self.username_taken)

        hashed_password = password_hasher.hash(password)

        return self.repo.create(normalised_username, hashed_password)

    def find_user_by_user_id(self, user_id: int) -> User | None:
        return self.repo.find_by_user_id(user_id=user_id)

    def find_user_by_username(self, username: str) -> User | None:
        return self.repo.find_by_username(username=username)

    def update_user(self, user_id: int, username: str, password: str) -> User | None:
        password_validator = PasswordValidator()
        username_validator = UsernameValidator()
        password_hasher = PasswordHasher()
        normalised_username = username.strip().lower()
        hashed_password = password_hasher.hash(password)

        if username_validator.validate(username) is False:
            raise ValueError(self.username_invalid)

        if password_validator.validate(password) is False:
            raise ValueError(self.password_invalid)

        user_exists = self.find_user_by_user_id(user_id)

        if user_exists is None:
            raise ValueError(self.user_does_not_exist)

        username_exists = self.find_user_by_username(normalised_username)

        if username_exists and (username_exists.user_id != user_exists.user_id):
            raise ValueError(self.username_taken)

        return self.repo.update(
            user_id=user_id, username=normalised_username, password=hashed_password
        )

    def delete_user(self, user_id: int) -> bool:
        return bool(self.repo.delete(user_id=user_id))
