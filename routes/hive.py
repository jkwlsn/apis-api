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
