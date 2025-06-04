"""Pytest module for testing the Observation class"""

import pytest

from lib.observation import Observation


@pytest.fixture
def test_observation() -> Observation:
    return Observation(1, True, 5, True, 4, 6, False, False, 10, 3, "Example notes", 1)


@pytest.fixture
def test_observation_2() -> Observation:
    return Observation(1, True, 5, True, 4, 6, False, False, 10, 3, "Example notes", 1)


class TestObservation:
    def test_observation_instance_constructs(
        self, test_observation: Observation
    ) -> None:
        """Test observation constructs with observation_id, queenright, queen_cells, bias, brood_frames, store_frames, chalk_brood, foul_brood, varroa_count, temper, notes, and inspection_id"""
        assert test_observation.observation_id == 1
        assert test_observation.queenright is True
        assert test_observation.queen_cells == 5
        assert test_observation.bias is True
        assert test_observation.brood_frames == 4
        assert test_observation.store_frames == 6
        assert test_observation.chalk_brood is False
        assert test_observation.foul_brood is False
        assert test_observation.varroa_count == 10
        assert test_observation.temper == 3
        assert test_observation.notes == "Example notes"
        assert test_observation.inspection_id == 1

    def test_observation_instance_pretty_prints(
        self, test_observation: Observation
    ) -> None:
        """Test __str__ dunder method pretty prints observation instance."""
        assert (
            str(test_observation)
            == "Observation(1, True, 5, True, 4, 6, False, False, 10, 3, Example notes, 1)"
        )

    def test_observation_instances_are_equal(
        self, test_observation: Observation, test_observation_2: Observation
    ) -> None:
        """Test __eq__ dunder method is true"""
        assert test_observation == test_observation_2


if __name__ == "__main__":
    pytest.main()
