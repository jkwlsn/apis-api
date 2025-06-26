"""Routes for /apiaries"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.apiary import ApiaryCreate, ApiaryRead, ApiaryUpdate
from services.apiary import ApiaryService
from services.dependencies import get_apiary_service

router = APIRouter()


@router.post("/users/{user_id}/apiaries")
def create_apiary(
    *,
    user_id: int,
    payload: ApiaryCreate,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> ApiaryRead:
    try:
        return service.create_apiary(
            name=payload.name, location=payload.location, user_id=user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/users/{user_id}/apiaries")
def list_user_apiaries(
    *,
    user_id: int,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> list[ApiaryRead]:
    apiaries = service.find_apiaries_by_user_id(user_id=user_id)
    if not apiaries:
        raise HTTPException(status_code=404, detail="No apiaries found for this user")
    return apiaries


@router.get("/apiaries/{apiary_id}")
def get_apiary(
    *,
    apiary_id: int,
    service: Annotated[ApiaryService, Depends(get_apiary_service)],
) -> ApiaryRead:
    apiaries = service.find_apiary_by_apiary_id(apiary_id=apiary_id)
    if not apiaries:
        raise HTTPException(status_code=404, detail="Apiary not found")
    return apiaries
