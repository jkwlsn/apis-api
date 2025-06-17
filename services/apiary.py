"""Service class for handling Apiary operations"""

from models.apiary import Apiary
from repositories.apiary import ApiaryRepository
from repositories.user import UserRepository


class ApiaryService:
    def __init__(
        self, apiary_repo: ApiaryRepository, user_repo: UserRepository
    ) -> None:
        self.apiary_repo = apiary_repo
        self.user_repo = user_repo
        self.name_required = "Apiary name is required"
        self.location_required = "Location is required"
        self.invalid_user_id = "Invalid user_id"
        self.invalid_apiary = "Invalid apiary_id"

    def _validate_data(self, name: str, location: str, user_id: int) -> None:
        if not name:
            raise ValueError(self.name_required)
        if not location:
            raise ValueError(self.location_required)
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError(self.invalid_user_id)

    def create_apiary(self, name: str, location: str, user_id: int) -> Apiary | None:
        name = name.strip()
        location = location.strip()
        self._validate_data(name, location, user_id)
        if not self.user_repo.find_by_user_id(user_id):
            raise ValueError(self.invalid_user_id)
        return self.apiary_repo.create(name=name, location=location, user_id=user_id)

    def find_apiary_by_apiary_id(self, apiary_id: int) -> Apiary | None:
        return self.apiary_repo.find_by_apiary_id(apiary_id=apiary_id)

    def find_apiaries_by_user_id(self, user_id: int) -> list[Apiary] | None:
        return self.apiary_repo.find_by_user_id(user_id=user_id)
