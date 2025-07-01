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
