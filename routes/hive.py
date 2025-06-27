"""Routes for /hives"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.hive import HiveCreate, HiveRead, HiveUpdate
from services.dependencies import get_hive_service
from services.hive import HiveService

router = APIRouter()
