"""Routes for /observations"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.observation import ObservationCreate, ObservationRead, ObservationUpdate
from services.dependencies import get_observation_service
from services.observation import ObservationService

router = APIRouter(tags=["Observations"])
