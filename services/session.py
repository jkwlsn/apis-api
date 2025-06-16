"""SessionService"""

from datetime import UTC, datetime

from models.session import Session
from repositories.session import SessionRepository
from repositories.user import UserRepository


class SessionService:
    def __init__(
        self, session_repo: SessionRepository, user_repo: UserRepository
    ) -> None:
        self.session_repo = session_repo
        self.user_id_invalid = "User does not exist"
        self.user_repo = user_repo

    def create_session(self, user_id: int) -> Session | None:
        if not self.user_repo.find_by_user_id(user_id):
            raise ValueError(self.user_id_invalid)
        session_start = datetime.now(tz=UTC)
        return self.session_repo.create(session_start=session_start, user_id=user_id)

    def find_session_by_session_id(self, session_id: int) -> Session | None:
        return self.session_repo.find_by_session_id(session_id)
