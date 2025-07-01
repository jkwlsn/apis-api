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


@router.get("/colonies/{colony_id}/inspections")
def get_inspection_by_colony_id(
    colony_id: int,
    service: Annotated[InspectionService, Depends(get_inspection_service)],
) -> list[InspectionRead]:
    inspections: list[InspectionRead] | None = service.find_inspections_by_colony_id(
        colony_id=colony_id
    )
    if not inspections:
        raise HTTPException(
            status_code=404, detail="No inspections found for this colony"
        )
    return inspections


@router.get("/inspections/{inspection_id}")
def get_inspection_by_inspection_id(
    inspection_id: int,
    service: Annotated[InspectionService, Depends(get_inspection_service)],
) -> InspectionRead:
    inspection = service.find_inspection_by_inspection_id(inspection_id=inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=404, detail="No inspections found for this colony"
        )
    return inspection


@router.post("/inspections/{inspection_id}")
def update_inspection(
    inspection_id: int,
    payload: InspectionUpdate,
    service: Annotated[InspectionService, Depends(get_inspection_service)],
) -> InspectionRead:
    try:
        return service.update_inspection(
            inspection_id=inspection_id,
            inspection_timestamp=payload.inspection_timestamp,
            colony_id=payload.colony_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/inspections/{inspection_id}")
def delete_inspection(
    inspection_id: int,
    service: Annotated[InspectionService, Depends(get_inspection_service)],
) -> bool:
    try:
        return service.delete_inspection(inspection_id=inspection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
