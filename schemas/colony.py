"""Colony schema"""

from pydantic import BaseModel


class ColonyCreate(BaseModel):
    hive_id: int


class ColonyRead(BaseModel):
    colony_id: int
    hive_id: int
