"""Tests for ObservationRepository"""

from unittest.mock import MagicMock

import pytest

from models.observation import Observation
from repositories.observation import ObservationRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestObservationRepository:
    test_observation: Observation = Observation(
        observation_id=1,
        queenright=True,
        queen_cells=3,
        bias=True,
        brood_frames=5,
        store_frames=4,
        chalk_brood=False,
        foul_brood=False,
        varroa_count=10,
        temper=5,
        notes="Example note",
        inspection_id=1,
    )
    test_observation_2: Observation = Observation(
        observation_id=2,
        queenright=True,
        queen_cells=3,
        bias=True,
        brood_frames=5,
        store_frames=4,
        chalk_brood=False,
        foul_brood=False,
        varroa_count=10,
        temper=5,
        notes="Example note",
        inspection_id=2,
    )
    test_observation_3: Observation = Observation(
        observation_id=3,
        queenright=True,
        queen_cells=3,
        bias=True,
        brood_frames=5,
        store_frames=4,
        chalk_brood=False,
        foul_brood=False,
        varroa_count=10,
        temper=5,
        notes="Example note",
        inspection_id=3,
    )

    def test_create_observation(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {"observation_id": self.test_observation.observation_id}
        ]
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        result: Observation | None = repo.create(
            queenright=self.test_observation.queenright,
            queen_cells=self.test_observation.queen_cells,
            bias=self.test_observation.bias,
            brood_frames=self.test_observation.brood_frames,
            store_frames=self.test_observation.store_frames,
            chalk_brood=self.test_observation.chalk_brood,
            foul_brood=self.test_observation.foul_brood,
            varroa_count=self.test_observation.varroa_count,
            temper=self.test_observation.temper,
            notes=self.test_observation.notes,
            inspection_id=self.test_observation.inspection_id,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO observations (queenright, queen_cells, bias, brood_frames, store_frames, chalk_brood, foul_brood, varroa_count, temper, notes, inspection_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING observation_id;",
            [
                self.test_observation.queenright,
                self.test_observation.queen_cells,
                self.test_observation.bias,
                self.test_observation.brood_frames,
                self.test_observation.store_frames,
                self.test_observation.chalk_brood,
                self.test_observation.foul_brood,
                self.test_observation.varroa_count,
                self.test_observation.temper,
                self.test_observation.notes,
                self.test_observation.inspection_id,
            ],
        )
        assert isinstance(result, Observation)
        assert result.observation_id == self.test_observation.observation_id
        assert result.queenright is True
        assert result.queen_cells == self.test_observation.queen_cells
        assert result.bias is True
        assert result.brood_frames == self.test_observation.brood_frames
        assert result.store_frames == self.test_observation.store_frames
        assert result.chalk_brood is False
        assert result.foul_brood is False
        assert result.varroa_count == self.test_observation.varroa_count
        assert result.temper == self.test_observation.temper
        assert result.notes == self.test_observation.notes
        assert result.inspection_id == self.test_observation.inspection_id

    def test_create_invalid_observation(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        result: Observation | None = repo.create(
            queenright=self.test_observation.queenright,
            queen_cells=self.test_observation.queen_cells,
            bias=self.test_observation.bias,
            brood_frames=self.test_observation.brood_frames,
            store_frames=self.test_observation.store_frames,
            chalk_brood=self.test_observation.chalk_brood,
            foul_brood=self.test_observation.foul_brood,
            varroa_count=self.test_observation.varroa_count,
            temper=self.test_observation.temper,
            notes=self.test_observation.notes,
            inspection_id=999,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO observations (queenright, queen_cells, bias, brood_frames, store_frames, chalk_brood, foul_brood, varroa_count, temper, notes, inspection_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING observation_id;",
            [
                self.test_observation.queenright,
                self.test_observation.queen_cells,
                self.test_observation.bias,
                self.test_observation.brood_frames,
                self.test_observation.store_frames,
                self.test_observation.chalk_brood,
                self.test_observation.foul_brood,
                self.test_observation.varroa_count,
                self.test_observation.temper,
                self.test_observation.notes,
                999,
            ],
        )
        assert result is None

    def test_can_find_observation_by_valid_observation_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = [
            {
                "observation_id": self.test_observation.observation_id,
                "queenright": self.test_observation.queenright,
                "queen_cells": self.test_observation.queen_cells,
                "bias": self.test_observation.bias,
                "brood_frames": self.test_observation.brood_frames,
                "store_frames": self.test_observation.store_frames,
                "chalk_brood": self.test_observation.chalk_brood,
                "foul_brood": self.test_observation.foul_brood,
                "varroa_count": self.test_observation.varroa_count,
                "temper": self.test_observation.temper,
                "notes": self.test_observation.notes,
                "inspection_id": self.test_observation.inspection_id,
            }
        ]
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        result: Observation | None = repo.find_by_observation_id(
            self.test_observation.observation_id
        )

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM observations WHERE observation_id = %s LIMIT 1;",
            [self.test_observation.observation_id],
        )
        assert isinstance(result, Observation)
        assert result.observation_id == self.test_observation.observation_id
        assert result.queenright is True
        assert result.queen_cells == self.test_observation.queen_cells
        assert result.bias is True
        assert result.brood_frames == self.test_observation.brood_frames
        assert result.store_frames == self.test_observation.store_frames
        assert result.chalk_brood is False
        assert result.foul_brood is False
        assert result.varroa_count == self.test_observation.varroa_count
        assert result.temper == self.test_observation.temper
        assert result.notes == self.test_observation.notes
        assert result.inspection_id == self.test_observation.inspection_id

    def test_can_not_find_observation_by_invalid_observation_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        result: Observation | None = repo.find_by_observation_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM observations WHERE observation_id = %s LIMIT 1;", [999]
        )
        assert result is None
