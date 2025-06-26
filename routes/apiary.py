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
