"""Routes for /actions"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.action import ActionCreate, ActionRead, ActionUpdate
from services.action import ActionService
from services.dependencies import get_action_service

router = APIRouter()
