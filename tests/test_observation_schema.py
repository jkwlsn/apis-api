"""Observation schema"""

import pytest
from pydantic import ValidationError

from schemas.observation import ObservationCreate, ObservationRead


class TestObservationSchema:
    def test_observation_create_valid(self) -> None:
        """Creates a valid observation"""
        test_data: dict = {
            "queenright": True,
            "queen_cells": 4,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 3,
            "notes": "Example notes",
            "inspection_id": 1,
        }
        observation = ObservationCreate(**test_data)
        assert observation.queenright is True
        assert observation.queen_cells == 4
        assert observation.bias is True
        assert observation.brood_frames == 5
        assert observation.store_frames == 6
        assert observation.chalk_brood is False
        assert observation.foul_brood is False
        assert observation.varroa_count == 10
        assert observation.temper == 3
        assert observation.notes == "Example notes"
        assert observation.inspection_id == 1

    def test_observation_create_missing_field(self) -> None:
        """Fail as no inspection_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            ObservationCreate(
                queenright=True,
                queen_cells=4,
                bias=True,
                brood_frames=5,
                store_frames=6,
                chalk_brood=False,
                foul_brood=False,
                varroa_count=10,
                temper=3,
                notes="Example notes",
            )
        assert "inspection" in str(exc_info.value)

    def test_observation_read_valid(self) -> None:
        """Reads valid observation"""
        test_data: dict = {
            "queenright": True,
            "queen_cells": 4,
            "bias": True,
            "brood_frames": 5,
            "store_frames": 6,
            "chalk_brood": False,
            "foul_brood": False,
            "varroa_count": 10,
            "temper": 3,
            "notes": "Example notes",
            "inspection_id": 1,
            "observation_id": 1,
        }
        observation = ObservationRead(**test_data)
        assert observation.observation_id == 1
        assert observation.queenright is True
        assert observation.queen_cells == 4
        assert observation.bias is True
        assert observation.brood_frames == 5
        assert observation.store_frames == 6
        assert observation.chalk_brood is False
        assert observation.foul_brood is False
        assert observation.varroa_count == 10
        assert observation.temper == 3
        assert observation.notes == "Example notes"
        assert observation.inspection_id == 1

    def test_observation_read_invalid_id_type(self) -> None:
        """Fails as observation_id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            ObservationRead(
                observation_id="not-an-int",
                queenright=True,
                queen_cells=4,
                bias=True,
                brood_frames=5,
                store_frames=6,
                chalk_brood=False,
                foul_brood=False,
                varroa_count=10,
                temper=3,
                notes="Example notes",
                inspection_id=1,
            )
        assert "observation_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
