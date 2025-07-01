"""Tests for Queen routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.queen import Queen
from services.dependencies import get_queen_service
from services.queen import QueenService

client: TestClient = TestClient(app)


@pytest.fixture
def mock_queen_service() -> Generator[MagicMock, None, None]:
    mock: MagicMock = MagicMock()
    app.dependency_overrides[get_queen_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


class TestQueenRoutes:
    valid_queen: Queen = Queen(queen_id=1, colour="Yellow", clipped=True, colony_id=1)

    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as temp_client:
            response = temp_client.get("/")
            assert response.status_code in {404, 200}

    def test_get_queen_service_direct(self) -> None:
        service: QueenService = get_queen_service()
        assert service is not None
        assert isinstance(service, QueenService)

    def test_create_queen_success(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.create_queen = MagicMock(return_value=self.valid_queen)

        response = client.post(
            "/queens", json={"colour": "Yellow", "clipped": True, "colony_id": 1}
        )

        assert response.status_code == 200
        assert response.json() == {
            "queen_id": self.valid_queen.queen_id,
            "colour": self.valid_queen.colour,
            "clipped": self.valid_queen.clipped,
            "colony_id": self.valid_queen.colony_id,
        }
        mock_queen_service.create_queen.assert_called_once_with(
            colour="Yellow", clipped=True, colony_id=1
        )

    def test_create_queen_failure(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.create_queen.side_effect = ValueError()

        response = client.post(
            "/queens", json={"colour": "Yellow", "clipped": True, "colony_id": -999}
        )

        assert response.status_code == 422

    def test_get_queen_by_colony_id_success(
        self, mock_queen_service: MagicMock
    ) -> None:
        mock_queen_service.find_queen_by_colony_id = MagicMock(
            return_value=[self.valid_queen]
        )

        response = client.get("/colonies/1/queens")

        assert response.status_code == 200
        assert response.json() == [
            {
                "queen_id": self.valid_queen.queen_id,
                "colour": self.valid_queen.colour,
                "clipped": self.valid_queen.clipped,
                "colony_id": self.valid_queen.colony_id,
            }
        ]

        mock_queen_service.find_queen_by_colony_id.assert_called_once_with(colony_id=1)

    def test_get_queen_by_colony_id_not_found(
        self, mock_queen_service: MagicMock
    ) -> None:
        mock_queen_service.find_queen_by_colony_id.return_value = []

        response = client.get("/colonies/999/queens")

        assert response.status_code == 404
        assert response.json()["detail"] == "No queens found for this colony"

    def test_get_queen_by_queen_id_success(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.find_queen_by_queen_id = MagicMock(
            return_value=self.valid_queen
        )

        response = client.get("/queens/1")

        assert response.status_code == 200
        assert response.json() == {
            "queen_id": self.valid_queen.queen_id,
            "colour": self.valid_queen.colour,
            "clipped": self.valid_queen.clipped,
            "colony_id": self.valid_queen.colony_id,
        }
        mock_queen_service.find_queen_by_queen_id.assert_called_once_with(queen_id=1)

    def test_get_queen_by_queen_id_not_found(
        self, mock_queen_service: MagicMock
    ) -> None:
        mock_queen_service.find_queen_by_queen_id.return_value = None

        response = client.get("/queens/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "No queens found for this colony"

    def test_update_queen_success(self, mock_queen_service: MagicMock) -> None:
        updated_queen = Queen(queen_id=1, colour="Yellow", clipped=True, colony_id=2)
        mock_queen_service.update_queen.return_value = updated_queen

        response = client.post(
            "/queens/1", json={"colour": "Yellow", "clipped": True, "colony_id": "2"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "queen_id": updated_queen.queen_id,
            "colour": self.valid_queen.colour,
            "clipped": self.valid_queen.clipped,
            "colony_id": updated_queen.colony_id,
        }
        mock_queen_service.update_queen.assert_called_once_with(
            queen_id=1, colour="Yellow", clipped=True, colony_id=2
        )

    def test_update_queen_failure(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.update_queen.side_effect = ValueError()

        response = client.post(
            "/queens/1", json={"colour": "Yellow", "clipped": True, "colony_id": "-999"}
        )

        assert response.status_code == 400

    def test_delete_queen_success(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.delete_queen.return_value = True

        response = client.delete("/queens/1")

        assert response.status_code == 200
        assert response.json() is True
        mock_queen_service.delete_queen.assert_called_once_with(queen_id=1)

    def test_delete_queen_not_found(self, mock_queen_service: MagicMock) -> None:
        mock_queen_service.delete_queen.side_effect = ValueError("Invalid queen_id")

        response = client.delete("/queens/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Invalid queen_id"
