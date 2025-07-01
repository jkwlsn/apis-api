"""Routes for /actions"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.action import ActionCreate, ActionRead, ActionUpdate
from services.action import ActionService
from services.dependencies import get_action_service

router = APIRouter()


@router.post("/actions")
def create_action(
    payload: ActionCreate,
    service: Annotated[ActionService, Depends(get_action_service)],
) -> ActionRead:
    try:
        return service.create_action(
            notes=payload.notes,
            inspection_id=payload.inspection_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
