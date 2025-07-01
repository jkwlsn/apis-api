"""Tests for Inspection routes"""

from collections.abc import Generator
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.inspection import Inspection
from schemas.inspection import InspectionRead
from services.dependencies import get_inspection_service
from services.inspection import InspectionService

client = TestClient(app)


@pytest.fixture
def mock_inspection_service() -> Generator[MagicMock, None, None]:
    mock = MagicMock()
    app.dependency_overrides[get_inspection_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def valid_inspection_read() -> InspectionRead:
    return InspectionRead(
        inspection_id=1,
        inspection_timestamp=datetime(2025, 6, 30, 13, 0, 0, tzinfo=UTC),
        colony_id=1,
    )


class TestInspectionRoutes:
    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {200, 404}

    def test_get_inspection_service_direct(self) -> None:
        service: InspectionService = get_inspection_service()
        assert isinstance(service, InspectionService)
