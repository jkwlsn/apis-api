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

    def test_create_observation_success(
        self,
        mock_observation_service: MagicMock,
        valid_observation_read: ObservationRead,
    ) -> None:
        mock_observation_service.create_observation.return_value = (
            valid_observation_read
        )

        response = client.post(
            "/observations",
            json={
                "queenright": True,
                "queen_cells": 5,
                "bias": True,
                "brood_frames": 5,
                "store_frames": 6,
                "chalk_brood": False,
                "foul_brood": False,
                "varroa_count": 10,
                "temper": 5,
                "notes": "Example notes",
                "inspection_id": 1,
            },
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "observation_id": 1,
            "queenright": True,
            "queen_cells": 5,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 5,
            "notes": "Example notes",
            "inspection_id": 1,
        }
        mock_observation_service.create_observation.assert_called_once_with(
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

    def test_create_observation_failure(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.create_observation.side_effect = ValueError()

        response = client.post(
            "/observations",
            json={
                "queenright": True,
                "queen_cells": 5,
                "bias": True,
                "brood_frames": 5,
                "store_frames": 6,
                "chalk_brood": False,
                "foul_brood": False,
                "varroa_count": 10,
                "temper": 5,
                "notes": "Example notes",
                "inspection_id": -999,
            },
        )
        assert response.status_code == 422
        mock_observation_service.create_observation.assert_called_once_with(
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
            inspection_id=-999,
        )

    def test_get_observations_by_inspection_id_success(
        self,
        mock_observation_service: MagicMock,
        valid_observation_read: ObservationRead,
    ) -> None:
        mock_observation_service.find_observation_by_inspection_id.return_value = (
            valid_observation_read
        )
        response = client.get("/inspections/1/observations")

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "observation_id": 1,
            "queenright": True,
            "queen_cells": 5,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 5,
            "notes": "Example notes",
            "inspection_id": 1,
        }

        mock_observation_service.find_observation_by_inspection_id.assert_called_once_with(
            inspection_id=valid_observation_read.inspection_id
        )

    def test_get_observation_by_inspection_id_not_found(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.find_observation_by_inspection_id.return_value = None

        response = client.get("/inspections/999/observations")

        assert response.status_code == 404
        assert response.json()["detail"] == "No observations found for this inspection"
        mock_observation_service.find_observation_by_inspection_id.assert_called_once_with(
            inspection_id=999
        )

    def test_get_observation_by_observation_id_success(
        self,
        mock_observation_service: MagicMock,
        valid_observation_read: ObservationRead,
    ) -> None:
        mock_observation_service.find_observation_by_observation_id.return_value = (
            valid_observation_read
        )

        response = client.get(f"/observations/{valid_observation_read.observation_id}")

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "observation_id": 1,
            "queenright": True,
            "queen_cells": 5,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 5,
            "notes": "Example notes",
            "inspection_id": 1,
        }
        mock_observation_service.find_observation_by_observation_id.assert_called_once_with(
            observation_id=valid_observation_read.observation_id,
        )

    def test_get_observation_by_observation_id_not_found(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.find_observation_by_observation_id.return_value = None

        response = client.get("/observations/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "No observations found for this inspection"

    def test_update_observation_success(
        self, mock_observation_service: MagicMock
    ) -> None:
        updated_observation = Observation(
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
            inspection_id=2,
        )
        mock_observation_service.update_observation.return_value = updated_observation

        response = client.post(
            "/observations/1",
            json={
                "queenright": True,
                "queen_cells": 5,
                "bias": True,
                "brood_frames": 5,
                "store_frames": 6,
                "chalk_brood": False,
                "foul_brood": False,
                "varroa_count": 10,
                "temper": 5,
                "notes": "Example notes",
                "inspection_id": 2,
            },
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "observation_id": 1,
            "queenright": True,
            "queen_cells": 5,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 5,
            "notes": "Example notes",
            "inspection_id": 2,
        }
        mock_observation_service.update_observation.assert_called_once_with(
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
            inspection_id=2,
        )

    def test_update_observation_failure(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.update_observation.side_effect = ValueError()

        response = client.post(
            "/observations/1",
            json={
                "queenright": True,
                "queen_cells": 5,
                "bias": True,
                "brood_frames": 5,
                "store_frames": 6,
                "chalk_brood": False,
                "foul_brood": False,
                "varroa_count": 10,
                "temper": 5,
                "notes": "Example notes",
                "inspection_id": -999,
            },
        )

        assert response.status_code == 400
        mock_observation_service.update_observation.assert_called_once_with(
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
            inspection_id=-999,
        )

    def test_delete_observation_success(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.delete_observation.return_value = True

        response = client.delete("/observations/1")

        assert response.status_code == 200
        assert response.json() is True
        mock_observation_service.delete_observation.assert_called_once_with(
            observation_id=1
        )

    def test_delete_observation_not_found(
        self, mock_observation_service: MagicMock
    ) -> None:
        mock_observation_service.delete_observation.side_effect = ValueError(
            "Invalid observation_id"
        )

        response = client.delete("/observations/-999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Invalid observation_id"
