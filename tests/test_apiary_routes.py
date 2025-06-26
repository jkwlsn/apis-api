"""Tests for Apiary API Routes (with all keyword arguments)"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas.apiary import ApiaryRead
from services.apiary import ApiaryService
from services.dependencies import get_apiary_service

client: TestClient = TestClient(app)


@pytest.fixture
def mock_apiary_service() -> Generator[MagicMock, None, None]:
    mock: MagicMock = MagicMock()
    app.dependency_overrides[get_apiary_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


class TestApiaryRoutes:
    valid_apiary: ApiaryRead = ApiaryRead(
        apiary_id=1, name="Happy Bees", location="Kent", user_id=1
    )

    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {404, 200}

    def test_get_apiary_service_direct(self) -> None:
        service: ApiaryService = get_apiary_service()

        assert service is not None
        assert isinstance(service, ApiaryService)
