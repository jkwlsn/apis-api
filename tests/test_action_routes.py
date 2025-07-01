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

    def test_create_action_success(
        self, mock_action_service: MagicMock, valid_action_read: ActionRead
    ) -> None:
        mock_action_service.create_action.return_value = valid_action_read

        response = client.post(
            "/actions",
            json={
                "notes": valid_action_read.notes,
                "inspection_id": valid_action_read.inspection_id,
            },
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "action_id": 1,
            "notes": "Example notes",
            "inspection_id": 1,
        }
        mock_action_service.create_action.assert_called_once()

    def test_create_action_failure(
        self, mock_action_service: MagicMock, invalid_action_read: ActionRead
    ) -> None:
        mock_action_service.create_action.side_effect = ValueError()

        response = client.post(
            "/actions",
            json={
                "notes": invalid_action_read.notes,
                "inspection_id": invalid_action_read.inspection_id,
            },
        )

        assert response.status_code == 422

    def test_get_actions_by_inspection_id_success(
        self, mock_action_service: MagicMock, valid_action_read: ActionRead
    ) -> None:
        mock_action_service.find_actions_by_inspection_id.return_value = [
            valid_action_read
        ]

        response = client.get(f"/inspections/{valid_action_read.inspection_id}/actions")

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == [
            {
                "action_id": 1,
                "notes": "Example notes",
                "inspection_id": 1,
            }
        ]
        mock_action_service.find_actions_by_inspection_id.assert_called_once_with(
            inspection_id=1
        )

    def test_get_actions_by_inspection_id_not_found(
        self, mock_action_service: MagicMock
    ) -> None:
        mock_action_service.find_actions_by_inspection_id.return_value = []

        response = client.get("/inspections/999/actions")

        assert response.status_code == 404
        assert response.json()["detail"] == "No actions found for this inspection"
