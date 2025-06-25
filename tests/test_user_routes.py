"""Tests for User API Routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas.user import UserRead
from services.dependencies import get_user_service
from services.user import UserService

client: TestClient = TestClient(app)
