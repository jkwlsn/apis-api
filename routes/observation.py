"""Routes for /observations"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.observation import ObservationCreate, ObservationRead, ObservationUpdate
from services.dependencies import get_observation_service
from services.observation import ObservationService

router = APIRouter(tags=["Observations"])


@router.post("/observations")
def create_observation(
    payload: ObservationCreate,
    service: Annotated[ObservationService, Depends(get_observation_service)],
) -> ObservationRead:
    try:
        return service.create_observation(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/inspections/{inspection_id}/observations")
def get_observation_by_inspection_id(
    inspection_id: int,
    service: Annotated[ObservationService, Depends(get_observation_service)],
) -> ObservationRead:
    observation = service.find_observation_by_inspection_id(inspection_id=inspection_id)
    if not observation:
        raise HTTPException(
            status_code=404, detail="No observations found for this inspection"
        )
    return observation


@router.get("/observations/{observation_id}")
def get_observation_by_observation_id(
    observation_id: int,
    service: Annotated[ObservationService, Depends(get_observation_service)],
) -> ObservationRead:
    observation = service.find_observation_by_observation_id(
        observation_id=observation_id
    )
    if not observation:
        raise HTTPException(
            status_code=404, detail="No observations found for this inspection"
        )
    return observation
