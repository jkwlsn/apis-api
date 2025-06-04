"""Session model class"""

import datetime
from dataclasses import dataclass


@dataclass
class Session:
    """Models Sessions in the database"""

    session_id: int
    session_start: type[datetime.datetime]
    user_id: int

    def __str__(self) -> str:
        return f"Session({self.session_id}, {self.session_start}, {self.user_id})"
