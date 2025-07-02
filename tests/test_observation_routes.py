"""Tests for Observation routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.observation import Observation
from schemas.observation import ObservationRead
from services.dependencies import get_observation_service
from services.observation import ObservationService

client = TestClient(app)


@pytest.fixture
def mock_observation_service() -> Generator[MagicMock, None, None]:
    mock = MagicMock()
    app.dependency_overrides[get_observation_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def valid_observation_read() -> ObservationRead:
    return ObservationRead(
        observation_id=1,
        queenright=True,
        queen_cells=5,
        bias=True,
        brood_frames=5,
        store_frames=6,
        chalk_brood=False,
        foul_brood=False,
        varroa_count=10,
        temper=5,
        notes="Example notes",
        inspection_id=1,
    )


class TestObservationRoutes:
    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {200, 404}

    def test_get_observation_service_direct(self) -> None:
        service: ObservationService = get_observation_service()
        assert isinstance(service, ObservationService)
