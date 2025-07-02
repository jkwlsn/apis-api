"""APIS-API"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.instance import db
from routes.action import router as action_router
from routes.apiary import router as apiary_router
from routes.colony import router as colony_router
from routes.hive import router as hive_router
from routes.inspection import router as inspection_router
from routes.observation import router as observation_router
from routes.queen import router as queen_router
from routes.user import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    db.connect()
    yield
    db.close()


app = FastAPI()

app.router.lifespan_context = lifespan

app.include_router(user_router)
app.include_router(apiary_router)
app.include_router(hive_router)
app.include_router(colony_router)
app.include_router(queen_router)
app.include_router(inspection_router)
app.include_router(action_router)
app.include_router(observation_router)
