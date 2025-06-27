"""Tests for hive routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.hive import Hive
from services.dependencies import get_hive_service
from services.hive import HiveService

client: TestClient = TestClient(app)


@pytest.fixture
def mock_hive_service() -> Generator[MagicMock, None, None]:
    mock: MagicMock = MagicMock()
    app.dependency_overrides[get_hive_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


class TestHiveRoutes:
    valid_hive: Hive = Hive(hive_id=1, name="Test Hive", apiary_id=1)

    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {404, 200}

    def test_get_hive_service_direct(self) -> None:
        service: HiveService = get_hive_service()
        assert service is not None
        assert isinstance(service, HiveService)
