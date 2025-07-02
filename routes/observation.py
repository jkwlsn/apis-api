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
