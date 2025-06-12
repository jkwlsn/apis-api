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

    def test_can_find_observation_by_valid_inspection_id(
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

        result: Observation | None = repo.find_by_inspection_id(
            self.test_observation.inspection_id
        )

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM observations WHERE inspection_id = %s LIMIT 1;",
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

    def test_can_not_find_observation_by_invalid_inspection_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        result: Observation | None = repo.find_by_inspection_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM observations WHERE inspection_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
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
            },
            {
                "observation_id": self.test_observation_2.observation_id,
                "queenright": self.test_observation_2.queenright,
                "queen_cells": self.test_observation_2.queen_cells,
                "bias": self.test_observation_2.bias,
                "brood_frames": self.test_observation_2.brood_frames,
                "store_frames": self.test_observation_2.store_frames,
                "chalk_brood": self.test_observation_2.chalk_brood,
                "foul_brood": self.test_observation_2.foul_brood,
                "varroa_count": self.test_observation_2.varroa_count,
                "temper": self.test_observation_2.temper,
                "notes": self.test_observation_2.notes,
                "inspection_id": self.test_observation_2.inspection_id,
            },
            {
                "observation_id": self.test_observation_3.observation_id,
                "queenright": self.test_observation_3.queenright,
                "queen_cells": self.test_observation_3.queen_cells,
                "bias": self.test_observation_3.bias,
                "brood_frames": self.test_observation_3.brood_frames,
                "store_frames": self.test_observation_3.store_frames,
                "chalk_brood": self.test_observation_3.chalk_brood,
                "foul_brood": self.test_observation_3.foul_brood,
                "varroa_count": self.test_observation_3.varroa_count,
                "temper": self.test_observation_3.temper,
                "notes": self.test_observation_3.notes,
                "inspection_id": self.test_observation_3.inspection_id,
            },
        ]
        repo: ObservationRepository = ObservationRepository(db=mock_db)

        results: list[Observation] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM observations;", [])
        assert isinstance(results, (list, Observation))
        assert results[0].observation_id == 1
        assert results[1].observation_id == 2
        assert results[2].observation_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(mock_db)

        result: list[Observation] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM observations;", [])
        assert result is None

    def test_can_update_valid_observation(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "observation_id": self.test_observation.observation_id,
            }
        ]
        repo: ObservationRepository = ObservationRepository(mock_db)

        result: Observation | None = repo.update(
            observation_id=self.test_observation.observation_id,
            queenright=self.test_observation.queenright,
            queen_cells=self.test_observation.queen_cells,
            bias=self.test_observation.bias,
            brood_frames=self.test_observation.brood_frames,
            store_frames=self.test_observation.store_frames,
            chalk_brood=self.test_observation.chalk_brood,
            foul_brood=self.test_observation.foul_brood,
            varroa_count=self.test_observation.varroa_count,
            temper=self.test_observation.temper,
            notes="UPDATED NOTES",
            inspection_id=self.test_observation.inspection_id,
        )

        mock_db.execute.assert_called_once_with(
            "UPDATE observations SET queenright = %s, queen-cells = %s, bias = %s, brood_frames = %s, store_frames = %s, chalk_brood = %s, foul_brood = %s, varroa_count = %s, temper = %s, notes = %s, inspection_id = %s RETURNING observation_id;",
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
                "UPDATED NOTES",
                self.test_observation.inspection_id,
                self.test_observation.observation_id,
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
        assert result.notes == "UPDATED NOTES"
        assert result.inspection_id == self.test_observation.inspection_id

    def test_can_not_update_invalid_observation(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE an invalid observation in the database"""
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(mock_db)

        result: Observation | None = repo.update(
            observation_id=self.test_observation.observation_id,
            queenright=self.test_observation.queenright,
            queen_cells=self.test_observation.queen_cells,
            bias=self.test_observation.bias,
            brood_frames=self.test_observation.brood_frames,
            store_frames=self.test_observation.store_frames,
            chalk_brood=self.test_observation.chalk_brood,
            foul_brood=self.test_observation.foul_brood,
            varroa_count=self.test_observation.varroa_count,
            temper=self.test_observation.temper,
            notes="BAD UPDATE",
            inspection_id=self.test_observation.inspection_id,
        )

        mock_db.execute.assert_called_once_with(
            "UPDATE observations SET queenright = %s, queen-cells = %s, bias = %s, brood_frames = %s, store_frames = %s, chalk_brood = %s, foul_brood = %s, varroa_count = %s, temper = %s, notes = %s, inspection_id = %s RETURNING observation_id;",
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
                "BAD UPDATE",
                self.test_observation.inspection_id,
                self.test_observation.observation_id,
            ],
        )
        assert result is None

    def test_can_delete_valid_observation(self, mock_db: MagicMock) -> None:
        """Respository CAN DELETE a single valid observation in the database"""
        mock_db.execute.return_value = [1]
        repo: ObservationRepository = ObservationRepository(mock_db)
        result: list[int] = repo.delete(1)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM observations WHERE observation_id = %s RETURNING observation_id;",
            [1],
        )
        assert result is True

    def test_can_not_delete_invalid_observation(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT DELETE an invalid observation in the database"""
        mock_db.execute.return_value = []
        repo: ObservationRepository = ObservationRepository(mock_db)
        result: list = repo.delete(999)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM observations WHERE observation_id = %s RETURNING observation_id;",
            [999],
        )
        assert result is False
