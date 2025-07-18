"""Tests for QueenService"""

from unittest.mock import MagicMock

import pytest

from models.colony import Colony
from models.queen import Queen
from services.queen import QueenService


@pytest.fixture
def queen_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def colony_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Queen:
    return Queen(queen_id=1, colour="Yellow", clipped=True, colony_id=1)


@pytest.fixture
def test_data_2() -> Queen:
    return Queen(queen_id=2, colour="Blue", clipped=True, colony_id=2)


def test_create_queen(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    colour = "Yellow"
    clipped = True
    colony_id = 1
    queen_repo.create.return_value = test_data
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: Queen | None = queen_service.create_queen(
        colour=colour, clipped=clipped, colony_id=colony_id
    )

    assert isinstance(results, Queen)
    assert results.queen_id == test_data.queen_id
    assert results.colour == test_data.colour
    assert results.clipped is True
    assert results.colony_id == colony_id


def test_can_not_create_queen_invalid_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    colour = "Yellow"
    clipped = True
    colony_id = -1
    queen_repo.create.return_value = test_data
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        queen_service.create_queen(colour=colour, clipped=clipped, colony_id=colony_id)


def test_can_not_create_queen_missing_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    colour = "Yellow"
    clipped = True
    colony_id = 999
    queen_repo.create.return_value = test_data
    colony_repo.find_by_colony_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        queen_service.create_queen(colour=colour, clipped=clipped, colony_id=colony_id)


def test_find_queen_by_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    queen_repo.find_by_queen_id.return_value = test_data
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: Queen | None = queen_service.find_queen_by_queen_id(1)

    assert isinstance(results, Queen)
    assert results.queen_id == test_data.queen_id
    assert results.colour == test_data.colour
    assert results.clipped is True
    assert results.colony_id == test_data.colony_id


def test_can_not_find_queen_by_missing_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    queen_id = 999
    queen_repo.find_by_queen_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    result = queen_service.find_queen_by_queen_id(queen_id)

    assert result is None


def test_can_not_find_queen_by_invalid_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    queen_id = -1
    queen_repo.find_by_queen_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid queen_id"):
        queen_service.find_queen_by_queen_id(queen_id)


def test_find_queen_by_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen, test_data_2: Queen
) -> None:
    colony_id = 1
    queen_repo.find_by_colony_id.return_value = [test_data, test_data_2]
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: list[Queen] | None = queen_service.find_queen_by_colony_id(colony_id)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Queen)
    assert results[0].colour == test_data.colour
    assert results[0].clipped is True
    assert results[0].colony_id == test_data.colony_id
    assert isinstance(results[1], Queen)
    assert results[1].colour == test_data_2.colour
    assert results[1].clipped is True
    assert results[1].colony_id == test_data_2.colony_id


def test_can_not_find_queen_by_missing_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    colony_id = 999
    queen_repo.find_by_colony_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: list[Queen] | None = queen_service.find_queen_by_colony_id(colony_id)

    assert results is None


def test_can_not_find_queen_by_invalid_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    colony_id = -1
    queen_repo.find_by_colony_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        queen_service.find_queen_by_colony_id(colony_id)


def test_update_queen(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    queen_id = 1
    colour = "Yellow"
    clipped = True
    colony_id = 1
    queen_repo.find_by_queen_id.return_value = test_data
    colony_repo.find_by_colony_id.return_value = Colony(1, 1)
    queen_repo.update.return_value = test_data
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: Queen | None = queen_service.update_queen(
        queen_id=queen_id, colour=colour, clipped=clipped, colony_id=colony_id
    )

    assert results.queen_id == test_data.queen_id
    assert results.colour == test_data.colour
    assert results.clipped is True
    assert results.colony_id == test_data.colony_id


def test_can_not_update_queen_invalid_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    queen_repo.update.return_value = test_data
    queen_id = -1
    colour = "Yellow"
    clipped = True
    colony_id = 1
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid queen_id"):
        queen_service.update_queen(
            queen_id=queen_id, colour=colour, clipped=clipped, colony_id=colony_id
        )


def test_can_not_update_queen_missing_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    queen_repo.find_by_queen_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)
    queen_id = 999
    colour = "Yellow"
    clipped = True
    colony_id = 1

    with pytest.raises(ValueError, match="Invalid queen_id"):
        queen_service.update_queen(
            queen_id=queen_id, colour=colour, clipped=clipped, colony_id=colony_id
        )


def test_can_not_update_queen_invalid_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    queen_repo.update.return_value = test_data
    queen_id = 1
    colour = "Yellow"
    clipped = True
    colony_id = -1
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        queen_service.update_queen(
            queen_id=queen_id, colour=colour, clipped=clipped, colony_id=colony_id
        )


def test_can_not_update_queen_missing_colony_id(
    queen_repo: MagicMock, colony_repo: MagicMock, test_data: Queen
) -> None:
    queen_repo.update.return_value = test_data
    colony_repo.find_by_colony_id.return_value = None
    queen_id = 1
    colour = "Yellow"
    clipped = True
    colony_id = 999
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        queen_service.update_queen(
            queen_id=queen_id, colour=colour, clipped=clipped, colony_id=colony_id
        )


def test_delete_queen(queen_repo: MagicMock, colony_repo: MagicMock) -> None:
    queen_id = 1
    queen_repo.delete.return_value = True
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    result: bool = queen_service.delete_queen(queen_id)

    assert result is True


def test_can_not_delete_queen_missing_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    queen_id = 999
    queen_repo.find_by_queen_id.return_value = None
    queen_repo.delete.return_value = False
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    results: bool = queen_service.delete_queen(queen_id)

    assert results is False


def test_can_not_delete_queen_invalid_queen_id(
    queen_repo: MagicMock, colony_repo: MagicMock
) -> None:
    queen_id = -1
    queen_repo.delete.return_value = False
    queen_repo.find_by_queen_id.return_value = None
    queen_service: QueenService = QueenService(queen_repo, colony_repo)

    with pytest.raises(ValueError, match="Invalid queen_id"):
        queen_service.delete_queen(queen_id)
