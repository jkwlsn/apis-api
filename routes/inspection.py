"""Routes for /inspections"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.inspection import InspectionCreate, InspectionRead, InspectionUpdate
from services.dependencies import get_inspection_service
from services.inspection import InspectionService

router = APIRouter()
