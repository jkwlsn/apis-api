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


@router.get("/id/{user_id}")
def get_user_by_id(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    user = service.find_user_by_user_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/id/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        updated_user = service.update_user(
            user_id=user_id, username=user.username, password=user.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Update failed: does user exist?")
    return updated_user


@router.delete("/id/{user_id}")
def delete_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> bool:
    deleted = service.delete_user(user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
