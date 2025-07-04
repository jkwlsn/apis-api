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


@router.get("/inspections/{inspection_id}/actions")
def get_actions_by_inspection_id(
    inspection_id: int,
    service: Annotated[ActionService, Depends(get_action_service)],
) -> list[ActionRead]:
    actions: list[ActionRead] | None = service.find_actions_by_inspection_id(
        inspection_id=inspection_id
    )
    if not actions:
        raise HTTPException(
            status_code=404, detail="No actions found for this inspection"
        )
    return actions


@router.get("/actions/{action_id}")
def get_action_by_action_id(
    action_id: int,
    service: Annotated[ActionService, Depends(get_action_service)],
) -> ActionRead:
    action = service.find_action_by_action_id(action_id=action_id)
    if not action:
        raise HTTPException(
            status_code=404, detail="No actions found for this inspection"
        )
    return action


@router.post("/actions/{action_id}")
def update_action(
    action_id: int,
    payload: ActionUpdate,
    service: Annotated[ActionService, Depends(get_action_service)],
) -> ActionRead:
    try:
        return service.update_action(
            action_id=action_id,
            notes=payload.notes,
            inspection_id=payload.inspection_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/actions/{action_id}")
def delete_action(
    action_id: int,
    service: Annotated[ActionService, Depends(get_action_service)],
) -> bool:
    try:
        return service.delete_action(action_id=action_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
