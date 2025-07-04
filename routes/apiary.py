"""Routes for /apiaries"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.apiary import ApiaryCreate, ApiaryRead, ApiaryUpdate
from services.apiary import ApiaryService
from services.dependencies import get_apiary_service

router = APIRouter()


@router.post("/apiaries")
def create_apiary(
    payload: ApiaryCreate,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> ApiaryRead:
    try:
        return service.create_apiary(
            name=payload.name, location=payload.location, user_id=payload.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/users/{user_id}/apiaries")
def list_user_apiaries(
    user_id: int,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> list[ApiaryRead]:
    apiaries = service.find_apiaries_by_user_id(user_id=user_id)
    if not apiaries:
        raise HTTPException(status_code=404, detail="No apiaries found for this user")
    return apiaries


@router.get("/apiaries/{apiary_id}")
def get_apiary(
    apiary_id: int,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> ApiaryRead:
    apiaries = service.find_apiary_by_apiary_id(apiary_id=apiary_id)
    if not apiaries:
        raise HTTPException(status_code=404, detail="Apiary not found")
    return apiaries


@router.post("/apiaries/{apiary_id}")
def update_apiary(
    apiary_id: int,
    payload: ApiaryUpdate,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> ApiaryRead:
    try:
        return service.update_apiary(
            apiary_id=apiary_id,
            name=payload.name,
            location=payload.location,
            user_id=payload.user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/apiaries/{apiary_id}")
def delete_apiary(
    apiary_id: int,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> bool:
    try:
        return service.delete_apiary(apiary_id=apiary_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
