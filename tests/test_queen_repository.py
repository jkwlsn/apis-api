"""Tests for the Queen Repository"""

from unittest.mock import MagicMock

import pytest

from models.queen import Queen
from repositories.queen import QueenRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestQueenRepository:
    test_queen: Queen = Queen(queen_id=1, colour="Yellow", clipped=True, colony_id=1)
    test_queen_2: Queen = Queen(queen_id=2, colour="Blue", clipped=True, colony_id=2)
    test_queen_3: Queen = Queen(queen_id=3, colour="Red", clipped=True, colony_id=3)

    def test_create_queen(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [{"queen_id": self.test_queen.queen_id}]
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.create(
            colour=self.test_queen.colour,
            clipped=self.test_queen.clipped,
            colony_id=self.test_queen.colony_id,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO queens (colour, clipped, colony_id) VALUES (%s, %s, %s) RETURNING queen_id;",
            [
                self.test_queen.colour,
                self.test_queen.clipped,
                self.test_queen.colony_id,
            ],
        )
        assert isinstance(result, Queen)
        assert result.queen_id == self.test_queen.queen_id
        assert result.colour == self.test_queen.colour
        assert result.clipped == self.test_queen.clipped
        assert result.colony_id == self.test_queen.colony_id

    def test_create_invalid_queen(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.create(
            colour=self.test_queen.colour,
            clipped=self.test_queen.clipped,
            colony_id=self.test_queen.colony_id,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO queens (colour, clipped, colony_id) VALUES (%s, %s, %s) RETURNING queen_id;",
            [
                self.test_queen.colour,
                self.test_queen.clipped,
                self.test_queen.colony_id,
            ],
        )
        assert result is None
