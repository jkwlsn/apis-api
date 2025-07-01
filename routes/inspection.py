"""Routes for /inspections"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.inspection import InspectionCreate, InspectionRead, InspectionUpdate
from services.dependencies import get_inspection_service
from services.inspection import InspectionService

router = APIRouter()


@router.post("/inspections")
def create_inspection(
    payload: InspectionCreate,
    service: Annotated[InspectionService, Depends(get_inspection_service)],
) -> InspectionRead:
    try:
        return service.create_inspection(
            inspection_timestamp=payload.inspection_timestamp,
            colony_id=payload.colony_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
