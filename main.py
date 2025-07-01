"""APIS-API"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.instance import db
from routes.apiary import router as apiary_router
from routes.colony import router as colony_router
from routes.hive import router as hive_router
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
