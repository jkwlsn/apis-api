"""Creates an instance that can be shared across the codebase"""

from db.database_configuration import DatabaseConfiguration
from db.database_connection import DatabaseConnection

config = DatabaseConfiguration(".env")
db = DatabaseConnection(config=config)
db.connect()
