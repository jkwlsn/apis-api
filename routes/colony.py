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


@router.get("/hives/{hive_id}/colony")
def get_colony_by_hive_id(
    *,
    hive_id: int,
    service: Annotated[ColonyService, Depends(get_colony_service)],
) -> list[ColonyRead]:
    colony = service.find_colony_by_hive_id(hive_id=hive_id)
    if not colony:
        raise HTTPException(status_code=404, detail="No colonies found for this hive")
    return colony


@router.get("/colony/{colony_id}")
def get_colony_by_colony_id(
    *,
    colony_id: int,
    service: Annotated[ColonyService, Depends(get_colony_service)],
) -> ColonyRead:
    colony = service.find_colony_by_colony_id(colony_id=colony_id)
    if not colony:
        raise HTTPException(status_code=404, detail="No colonies found for this hive")
    return colony


@router.post("/colony/{colony_id}")
def update_colony(
    *,
    colony_id: int,
    payload: ColonyUpdate,
    service: Annotated[ColonyService, Depends(get_colony_service)],
) -> ColonyRead:
    try:
        return service.update_colony(
            colony_id=colony_id,
            hive_id=payload.hive_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/colony/{colony_id}")
def delete_colony(
    colony_id: int,
    service: Annotated[ColonyService, Depends(get_colony_service)],
) -> bool:
    try:
        return service.delete_colony(colony_id=colony_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
