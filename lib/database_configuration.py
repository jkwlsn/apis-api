"""Read configuration values from .env.db file"""

from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values


@dataclass
class DatabaseConfiguration:
    def __init__(self, filename: str = ".env.db") -> None:
        file_path = Path(filename)
        if Path.exists(file_path):
            config: dict[str, str | None] = dotenv_values(file_path)
            self.host: str | None = config.get("POSTGRES_HOST")
            self.port: str | None = config.get("POSTGRES_PORT")
            self.dbname: str | None = config.get("POSTGRES_DB")
            self.user: str | None = config.get("POSTGRES_USER")
            self.password: str | None = config.get("POSTGRES_PASSWORD")
        else:
            self.host = self.port = self.user = self.password = self.dbname = None
