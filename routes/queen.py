"""Routes for /queens"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.queen import QueenCreate, QueenRead, QueenUpdate
from services.dependencies import get_queen_service
from services.queen import QueenService

router = APIRouter()


@router.post("/queens")
def create_queen(
    payload: QueenCreate,
    service: Annotated[QueenService, Depends(get_queen_service)],
) -> QueenRead:
    try:
        return service.create_queen(
            colour=payload.colour, clipped=payload.clipped, colony_id=payload.colony_id
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/colonies/{colony_id}/queens")
def get_queen_by_colony_id(
    colony_id: int,
    service: Annotated[QueenService, Depends(get_queen_service)],
) -> list[QueenRead]:
    queen = service.find_queen_by_colony_id(colony_id=colony_id)
    if not queen:
        raise HTTPException(status_code=404, detail="No queens found for this colony")
    return queen


@router.get("/queens/{queen_id}")
def get_queen_by_queen_id(
    queen_id: int,
    service: Annotated[QueenService, Depends(get_queen_service)],
) -> QueenRead:
    queen = service.find_queen_by_queen_id(queen_id=queen_id)
    if not queen:
        raise HTTPException(status_code=404, detail="No queens found for this colony")
    return queen
