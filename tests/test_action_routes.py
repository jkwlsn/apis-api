"""Tests for Action routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.action import Action
from schemas.action import ActionRead
from services.action import ActionService
from services.dependencies import get_action_service

client = TestClient(app)


@pytest.fixture
def mock_action_service() -> Generator[MagicMock, None, None]:
    mock = MagicMock()
    app.dependency_overrides[get_action_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def valid_action_read() -> ActionRead:
    return ActionRead(
        action_id=1,
        notes="Example notes",
        inspection_id=1,
    )


@pytest.fixture
def invalid_action_read() -> ActionRead:
    return ActionRead(
        action_id=1,
        notes="Example notes",
        inspection_id=-999,
    )


class TestActionRoutes:
    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {200, 404}

    def test_get_action_service_direct(self) -> None:
        service: ActionService = get_action_service()
        assert isinstance(service, ActionService)
