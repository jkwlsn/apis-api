"""Read configuration values from .env file"""

import os
from pathlib import Path

from dotenv import dotenv_values


class DatabaseConfiguration:
    def __init__(self, filename: str = ".env") -> None:
        file_path: Path = Path(filename)

        if file_path.exists():
            config: dict[str, str | None] = dotenv_values(file_path)
        else:
            config: dict[str, str | None] = dict(os.environ)

        self.host: str | None = config.get("POSTGRES_HOST")
        self.port: str | None = config.get("POSTGRES_PORT")
        self.dbname: str | None = config.get("POSTGRES_DB")
        self.user: str | None = config.get("POSTGRES_USER")
        self.password: str | None = config.get("POSTGRES_PASSWORD")
