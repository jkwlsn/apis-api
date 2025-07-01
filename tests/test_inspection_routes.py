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

    def test_create_inspection_success(
        self, mock_inspection_service: MagicMock, valid_inspection_read: InspectionRead
    ) -> None:
        mock_inspection_service.create_inspection.return_value = valid_inspection_read

        response = client.post(
            "/inspections",
            json={
                "inspection_timestamp": valid_inspection_read.inspection_timestamp.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "colony_id": valid_inspection_read.colony_id,
            },
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        expected = {
            "inspection_id": valid_inspection_read.inspection_id,
            "inspection_timestamp": valid_inspection_read.inspection_timestamp.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "colony_id": valid_inspection_read.colony_id,
        }
        assert response.json() == expected
        mock_inspection_service.create_inspection.assert_called_once()

    def test_create_inspection_failure(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.create_inspection.side_effect = ValueError()

        response = client.post(
            "/inspections",
            json={
                "inspection_timestamp": "2025-06-23T02:10:25Z",
                "colony_id": -999,
            },
        )

        assert response.status_code == 422

    def test_get_inspections_by_colony_id_success(
        self, mock_inspection_service: MagicMock, valid_inspection_read: InspectionRead
    ) -> None:
        mock_inspection_service.find_inspections_by_colony_id.return_value = [
            valid_inspection_read
        ]

        response = client.get(
            f"/colonies/{valid_inspection_read.colony_id}/inspections"
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == [
            {
                "inspection_id": valid_inspection_read.inspection_id,
                "inspection_timestamp": valid_inspection_read.inspection_timestamp.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "colony_id": valid_inspection_read.colony_id,
            }
        ]
        mock_inspection_service.find_inspections_by_colony_id.assert_called_once_with(
            colony_id=valid_inspection_read.colony_id
        )

    def test_get_inspection_by_colony_id_not_found(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.find_inspections_by_colony_id.return_value = []

        response = client.get("/colonies/999/inspections")

        assert response.status_code == 404
        assert response.json()["detail"] == "No inspections found for this colony"

    def test_get_inspection_by_inspection_id_success(
        self, mock_inspection_service: MagicMock, valid_inspection_read: InspectionRead
    ) -> None:
        mock_inspection_service.find_inspection_by_inspection_id.return_value = (
            valid_inspection_read
        )

        response = client.get(f"/inspections/{valid_inspection_read.inspection_id}")

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "inspection_id": valid_inspection_read.inspection_id,
            "inspection_timestamp": valid_inspection_read.inspection_timestamp.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "colony_id": valid_inspection_read.colony_id,
        }
        mock_inspection_service.find_inspection_by_inspection_id.assert_called_once_with(
            inspection_id=valid_inspection_read.inspection_id,
        )

    def test_get_inspection_by_inspection_id_not_found(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.find_inspection_by_inspection_id.return_value = None

        response = client.get("/inspections/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "No inspections found for this colony"

    def test_update_inspection_success(
        self, mock_inspection_service: MagicMock
    ) -> None:
        updated_inspection = Inspection(
            inspection_id=1,
            inspection_timestamp=datetime(2025, 6, 23, 2, 10, 25, tzinfo=UTC),
            colony_id=2,
        )
        mock_inspection_service.update_inspection.return_value = updated_inspection

        response = client.post(
            "/inspections/1",
            json={
                "inspection_timestamp": updated_inspection.inspection_timestamp.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "colony_id": updated_inspection.colony_id,
            },
        )

        assert response.status_code == 200, f"Unexpected status: {response.text}"
        assert response.json() == {
            "inspection_id": updated_inspection.inspection_id,
            "inspection_timestamp": updated_inspection.inspection_timestamp.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "colony_id": updated_inspection.colony_id,
        }
        mock_inspection_service.update_inspection.assert_called_once_with(
            inspection_id=1,
            inspection_timestamp=updated_inspection.inspection_timestamp,
            colony_id=updated_inspection.colony_id,
        )

    def test_update_inspection_failure(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.update_inspection.side_effect = ValueError()

        response = client.post(
            "/inspections/1",
            json={
                "inspection_timestamp": "2025-06-23T02:10:25Z",
                "colony_id": -999,
            },
        )

        assert response.status_code == 400

    def test_delete_inspection_success(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.delete_inspection.return_value = True

        response = client.delete("/inspections/1")

        assert response.status_code == 200
        assert response.json() is True
        mock_inspection_service.delete_inspection.assert_called_once_with(
            inspection_id=1
        )

    def test_delete_inspection_not_found(
        self, mock_inspection_service: MagicMock
    ) -> None:
        mock_inspection_service.delete_inspection.side_effect = ValueError(
            "Invalid inspection_id"
        )

        response = client.delete("/inspections/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Invalid inspection_id"
