"""Pytest module for testing the Inspection class"""

import datetime
import zoneinfo

import pytest

from lib.inspection import Inspection


@pytest.fixture
def test_inspection() -> Inspection:
    return Inspection(
        1,
        datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        ),
        1,
    )


@pytest.fixture
def test_inspection_2() -> Inspection:
    return Inspection(
        1,
        datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        ),
        1,
    )


class TestInspection:
    def test_inspection_instance_constructs(self, test_inspection: Inspection) -> None:
        """Test inspection constructs with inspection_id and colony_id."""
        assert test_inspection.inspection_id == 1
        assert test_inspection.inspection_timestamp == datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        )
        assert test_inspection.colony_id == 1

    def test_inspection_instance_pretty_prints(
        self, test_inspection: Inspection
    ) -> None:
        """Test __str__ dunder method pretty prints inspection instance."""
        assert str(test_inspection) == "Inspection(1, 2020-06-23 02:10:25+00:00, 1)"

    def test_inspection_instances_are_equal(
        self, test_inspection: Inspection, test_inspection_2: Inspection
    ) -> None:
        """Test __eq__ dunder method is true"""
        assert test_inspection == test_inspection_2


if __name__ == "__main__":
    pytest.main()
