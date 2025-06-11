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

    def test_can_find_queen_by_valid_queen_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "queen_id": self.test_queen.queen_id,
                "colour": self.test_queen.colour,
                "clipped": self.test_queen.clipped,
                "colony_id": self.test_queen.colony_id,
            }
        ]
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.find_by_queen_id(self.test_queen.queen_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM queens WHERE queen_id = %s LIMIT 1;",
            [self.test_queen.queen_id],
        )
        assert isinstance(result, Queen)
        assert result.queen_id == self.test_queen.queen_id
        assert result.colour == self.test_queen.colour
        assert result.clipped == self.test_queen.clipped
        assert result.colony_id == self.test_queen.colony_id

    def test_can_not_find_queen_by_invalid_queen_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.find_by_queen_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM queens WHERE queen_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_queens_by_valid_colony_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "queen_id": self.test_queen.queen_id,
                "colour": self.test_queen.colour,
                "clipped": self.test_queen.clipped,
                "colony_id": self.test_queen.colony_id,
            }
        ]
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.find_by_colony_id(self.test_queen.colony_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM queens WHERE colony_id = %s LIMIT 1;",
            [self.test_queen.colony_id],
        )
        assert isinstance(result, Queen)
        assert result.queen_id == self.test_queen.queen_id
        assert result.colour == self.test_queen.colour
        assert result.clipped == self.test_queen.clipped
        assert result.colony_id == self.test_queen.colony_id

    def test_can_not_find_queen_by_invalid_colony_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: QueenRepository = QueenRepository(db=mock_db)

        result: Queen | None = repo.find_by_colony_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM queens WHERE colony_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "queen_id": self.test_queen.queen_id,
                "colour": self.test_queen.colour,
                "clipped": self.test_queen.clipped,
                "colony_id": self.test_queen.colony_id,
            },
            {
                "queen_id": self.test_queen_2.queen_id,
                "colour": self.test_queen_2.colour,
                "clipped": self.test_queen_2.clipped,
                "colony_id": self.test_queen_2.colony_id,
            },
            {
                "queen_id": self.test_queen_3.queen_id,
                "colour": self.test_queen_3.colour,
                "clipped": self.test_queen_3.clipped,
                "colony_id": self.test_queen_3.colony_id,
            },
        ]
        repo: QueenRepository = QueenRepository(db=mock_db)

        results: list[Queen] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM queens;", [])
        assert isinstance(results, (list, Queen))
        assert results[0].queen_id == 1
        assert results[1].queen_id == 2
        assert results[2].queen_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: QueenRepository = QueenRepository(mock_db)

        result: list[Queen] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM queens;", [])
        assert result is None

    def test_can_update_valid_queen(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "queen_id": self.test_queen.queen_id,
            }
        ]
        repo: QueenRepository = QueenRepository(mock_db)

        result: list[Queen] = repo.update(
            queen_id=1, colour="Yellow", clipped=True, colony_id=999
        )

        mock_db.execute.assert_called_once_with(
            "UPDATE queens SET colony_id = %s, colour = %s, clipped = %s WHERE queen_id = %s RETURNING queen_id;",
            [999, "Yellow", True, 1],
        )
        assert isinstance(result, Queen)
        assert result.queen_id == self.test_queen.queen_id
        assert result.colony_id == 999

    def test_can_not_update_invalid_queen(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE an invalid queen in the database"""
        mock_db.execute.return_value = []
        repo = QueenRepository(mock_db)

        result: list[Queen] = repo.update(
            queen_id=999, colour="Yellow", clipped=True, colony_id=1
        )
        assert result is None

    def test_can_delete_valid_queen(self, mock_db: MagicMock) -> None:
        """Respository CAN DELETE a single valid queen in the database"""
        mock_db.execute.return_value = [1]
        repo: QueenRepository = QueenRepository(mock_db)
        result: list[int] = repo.delete(1)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM queens WHERE queen_id = %s RETURNING queen_id;",
            [1],
        )
        assert result is True

    def test_can_not_delete_invalid_queen(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT DELETE an invalid queen in the database"""
        mock_db.execute.return_value = []
        repo: QueenRepository = QueenRepository(mock_db)
        result: list = repo.delete(999)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM queens WHERE queen_id = %s RETURNING queen_id;", [999]
        )
        assert result is False
