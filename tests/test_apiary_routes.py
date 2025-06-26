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

    def test_create_apiary_success(self, mock_apiary_service: MagicMock) -> None:
        mock_apiary_service.create_apiary = MagicMock(return_value=self.valid_apiary)

        response = client.post(
            "/users/1/apiaries",
            json={"name": "Happy Bees", "location": "Kent"},
        )

        assert response.status_code == 200
        assert response.json() == self.valid_apiary.model_dump()
        mock_apiary_service.create_apiary.assert_called_once_with(
            name="Happy Bees", location="Kent", user_id=1
        )

    def test_create_apiary_missing_name(self, mock_apiary_service: MagicMock) -> None:
        mock_apiary_service.create_apiary.side_effect = ValueError(
            "Apiary name is required"
        )

        response = client.post(
            "/users/1/apiaries",
            json={"name": "   ", "location": "Kent"},
        )

        assert response.status_code in {400, 422}
        assert "Apiary name is required" in response.json()["detail"]

    def test_create_apiary_invalid_user(self, mock_apiary_service: MagicMock) -> None:
        mock_apiary_service.create_apiary.side_effect = ValueError("Invalid user_id")

        response = client.post(
            "/users/999/apiaries",
            json={"name": "Happy Bees", "location": "Kent"},
        )

        assert response.status_code in {400, 422}
        assert response.json()["detail"] == "Invalid user_id"
