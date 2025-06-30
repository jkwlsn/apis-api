"""Routes for /colonies"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.colony import ColonyCreate, ColonyRead, ColonyUpdate
from services.colony import ColonyService
from services.dependencies import get_colony_service

router = APIRouter()


@router.post("/colony")
def create_colony(
    *,
    payload: ColonyCreate,
    service: Annotated[ColonyService, Depends(get_colony_service)],
) -> ColonyRead:
    try:
        return service.create_colony(hive_id=payload.hive_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
