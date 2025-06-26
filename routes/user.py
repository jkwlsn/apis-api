"""user routes"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.user import UserCreate, UserRead
from services.dependencies import get_user_service
from services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        created_user = service.create_user(
            username=user.username, password=user.password
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    if created_user is None:
        raise HTTPException(status_code=400, detail="Failed to create user") from None
    return created_user


@router.get("/username/{username}")
def get_user_by_username(
    username: str, service: Annotated[UserService, Depends(get_user_service)]
) -> UserRead:
    user = service.find_user_by_username(username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
