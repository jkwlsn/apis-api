"""Session model class"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    """Models Sessions in the database"""

    session_id: int
    session_start: datetime
    user_id: int

    def __str__(self) -> str:
        return f"Session({self.session_id}, {self.session_start}, {self.user_id})"
