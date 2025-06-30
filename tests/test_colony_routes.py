"""Tests for Colony routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.colony import Colony
from services.colony import ColonyService
from services.dependencies import get_colony_service

client: TestClient = TestClient(app)


@pytest.fixture
def mock_colony_service() -> Generator[MagicMock, None, None]:
    mock: MagicMock = MagicMock()
    app.dependency_overrides[get_colony_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


class TestColonyRoutes:
    valid_colony: Colony = Colony(colony_id=1, hive_id=1)

    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {404, 200}

    def test_get_colony_service_direct(self) -> None:
        service: ColonyService = get_colony_service()
        assert service is not None
        assert isinstance(service, ColonyService)

    def test_create_colony_success(self, mock_colony_service: MagicMock) -> None:
        mock_colony_service.create_colony = MagicMock(return_value=self.valid_colony)

        response = client.post("/colony", json={"hive_id": "1"})

        assert response.status_code == 200
        assert response.json() == {
            "colony_id": self.valid_colony.colony_id,
            "hive_id": self.valid_colony.hive_id,
        }
        mock_colony_service.create_colony.assert_called_once_with(hive_id=1)

    def test_create_colony_failure(self, mock_colony_service: MagicMock) -> None:
        mock_colony_service.create_colony = MagicMock(return_value=self.valid_colony)

        response = client.post("/colony")

        assert response.status_code == 422
