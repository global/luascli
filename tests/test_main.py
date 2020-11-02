from click.testing import CliRunner

from luascli.main import luas
from luascli.exceptions import (
    LuasStopNotFound,
    LuasLineNotFound,
    AddressLocationNotFound,
)
import mock


runner = CliRunner()


def test_stops():
    """Test if running luas <line> stops returns 0"""
    response = runner.invoke(luas, ["stops", "red"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["stops", "green"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["stops", "somethingelse"])
    assert response.exit_code == 1


def test_status():
    """Test if running luas <line> status returns successfull with a valid result"""
    response = runner.invoke(luas, ["status", "red"])
    assert response.exit_code == 0
    assert response.output == "Red Line services operating normally\n"

    response = runner.invoke(luas, ["status", "ran"])
    assert response.exit_code == 0
    assert response.output == "Green Line services operating normally\n"

    response = runner.invoke(luas, ["status", "somethingelse"])
    assert response.exit_code == 1
    assert response.output == "The stop somethingelse doesn't exist\n"

    with mock.patch("luascli.main.get_status", side_effect=TimeoutError):
        response = runner.invoke(luas, ["status", "somethingelse"])
        assert response.exit_code == 2


@mock.patch("luascli.main.click")
def test_map(mock_click):
    """Test if running luas <line> map returns successfull or not,
    depending on the input
    """
    mock_click.launch.return_value = ""

    response = runner.invoke(luas, ["map", "cit"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["map", "ran"])
    assert response.exit_code == 0

    with mock.patch("luascli.main.get_stop_detail", side_effect=LuasStopNotFound):
        response = runner.invoke(luas, ["map", "ran"])
        assert response.exit_code == 1

    with mock.patch("luascli.main.find_line_by_stop", side_effect=LuasLineNotFound):
        response = runner.invoke(luas, ["map", "somethingelse"])
        assert response.exit_code == 1


def test_address():
    """Test if running luas address <stop> returns the address of the Luas stop"""

    response = runner.invoke(luas, ["address", "cit"])
    assert response.exit_code == 0
    assert response.stdout.startswith("{'city") is True

    with mock.patch("luascli.main.get_address", side_effect=LuasStopNotFound):
        response = runner.invoke(luas, ["address", "cit"])
        assert response.exit_code == 1

    with mock.patch(
        "luascli.main.get_address", side_effect=AddressLocationNotFound("1", "2")
    ):
        response = runner.invoke(luas, ["address", "cit"])
        assert response.exit_code == 2


def test_timetable():
    """Test if luas time <stop> would return the timetable"""

    response = runner.invoke(luas, ["time", "cit", "--format", "json"])
    assert response.exit_code == 0
    assert response.stdout.startswith("{'inbound") is True

    response = runner.invoke(luas, ["time", "cit", "--format", "text"])
    assert response.exit_code == 0
    assert response.stdout.startswith("Inbound") is True

    response = runner.invoke(luas, ["time", "cit", "--format", "somethingelse"])
    assert response.exit_code == 3

    with mock.patch("luascli.main.get_timetable", side_effect=LuasStopNotFound):
        response = runner.invoke(luas, ["time", "cit", "--format", "text"])
        assert response.exit_code == 1


def test_fare_calculator():
    """Test if we can calculate fare between 2 stops, including children and adults"""

    response = runner.invoke(
        luas,
        ["fare", "cit", "jer", "--adults", "2", "--children", "1", "--format", "json"],
    )
    assert response.exit_code == 0
    assert response.stdout.startswith("{'adults': 2") is True

    # luas stop not found
    response = runner.invoke(
        luas,
        [
            "fare",
            "somethingelse",
            "jer",
            "--adults",
            "2",
            "--children",
            "1",
            "--format",
            "json",
        ],
    )
    assert response.exit_code == 1

    # invalid format
    response = runner.invoke(
        luas,
        [
            "fare",
            "cit",
            "jer",
            "--adults",
            "2",
            "--children",
            "1",
            "--format",
            "somethingelse",
        ],
    )
    assert response.exit_code == 3

    # invalid format and luas stop not found
    response = runner.invoke(
        luas,
        [
            "fare",
            "cit",
            "jer",
            "--adults",
            "2",
            "--children",
            "1",
            "--format",
            "somethingelse",
        ],
    )
    assert response.exit_code == 3
