"""Routes for /hives"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.hive import HiveCreate, HiveRead, HiveUpdate
from services.dependencies import get_hive_service
from services.hive import HiveService

router = APIRouter()


@router.post("/apiaries/{apiary_id}/hives")
def create_hive(
    *,
    apiary_id: int,
    payload: HiveCreate,
    service: Annotated[HiveService, Depends(get_hive_service)],
) -> HiveRead:
    try:
        return service.create_hive(name=payload.name, apiary_id=apiary_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/apiaries/{apiary_id}/hives")
def list_apiary_hives(
    *,
    apiary_id: int,
    service: Annotated[HiveService, Depends(get_hive_service)],
) -> list[HiveRead]:
    hives = service.find_hives_by_apiary_id(apiary_id=apiary_id)
    if not hives:
        raise HTTPException(status_code=404, detail="No hives found for this apiary")
    return hives


@router.get("/apiaries/{apiary_id}/hives/{hive_id}")
def get_hive(
    *,
    hive_id: int,
    service: Annotated[HiveService, Depends(get_hive_service)],
) -> HiveRead:
    hives = service.find_hive_by_hive_id(hive_id=hive_id)
    if not hives:
        raise HTTPException(status_code=404, detail="Hive not found")
    return hives
