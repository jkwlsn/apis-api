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

    def test_create_hive_success(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.create_hive = MagicMock(return_value=self.valid_hive)

        response = client.post("/apiaries/1/hives", json={"name": "Test Hive"})

        assert response.status_code == 200
        assert response.json() == {
            "hive_id": self.valid_hive.hive_id,
            "name": self.valid_hive.name,
            "apiary_id": self.valid_hive.apiary_id,
        }
        mock_hive_service.create_hive.assert_called_once_with(
            name="Test Hive", apiary_id=1
        )

    def test_create_hive_validation_error(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.create_hive.side_effect = ValueError("Hive name is required")

        response = client.post("/apiaries/1/hives", json={"name": ""})

        assert response.status_code in {400, 422}
        assert response.json()["detail"] == "Hive name is required"

    def test_list_hives_success(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.find_hives_by_apiary_id = MagicMock(
            return_value=[self.valid_hive]
        )

        response = client.get("/apiaries/1/hives")

        assert response.status_code == 200
        assert response.json() == [
            {
                "hive_id": self.valid_hive.hive_id,
                "name": self.valid_hive.name,
                "apiary_id": self.valid_hive.apiary_id,
            }
        ]
        mock_hive_service.find_hives_by_apiary_id.assert_called_once_with(apiary_id=1)

    def test_list_hives_not_found(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.find_hives_by_apiary_id.return_value = []

        response = client.get("/apiaries/1/hives")

        assert response.status_code == 404
        assert response.json()["detail"] == "No hives found for this apiary"

    def test_get_hive_success(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.find_hive_by_hive_id = MagicMock(return_value=self.valid_hive)

        response = client.get("/apiaries/1/hives/1")

        assert response.status_code == 200
        assert response.json() == {
            "hive_id": self.valid_hive.hive_id,
            "name": self.valid_hive.name,
            "apiary_id": self.valid_hive.apiary_id,
        }
        mock_hive_service.find_hive_by_hive_id.assert_called_once_with(hive_id=1)

    def test_get_hive_not_found(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.find_hive_by_hive_id.return_value = None

        response = client.get("/apiaries/1/hives/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Hive not found"

    def test_update_hive_success(self, mock_hive_service: MagicMock) -> None:
        updated_hive = Hive(hive_id=1, name="Updated Hive", apiary_id=1)
        mock_hive_service.update_hive.return_value = updated_hive

        response = client.post("/apiaries/1/hives/1", json={"name": "Updated Hive"})

        assert response.status_code == 200
        assert response.json() == {
            "hive_id": updated_hive.hive_id,
            "name": updated_hive.name,
            "apiary_id": updated_hive.apiary_id,
        }
        mock_hive_service.update_hive.assert_called_once_with(
            hive_id=1, name="Updated Hive", apiary_id=1
        )

    def test_update_hive_validation_error(self, mock_hive_service: MagicMock) -> None:
        mock_hive_service.update_hive.side_effect = ValueError("Hive name is required")

        response = client.post("/apiaries/1/hives/1", json={"name": ""})

        assert response.status_code == 400
        assert response.json()["detail"] == "Hive name is required"
