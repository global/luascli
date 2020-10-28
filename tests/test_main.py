from click.testing import CliRunner

from luascli.main import luas
import mock

runner = CliRunner()


def test_stops():
    """Test if running luas <line> stops returns 0"""
    response = runner.invoke(luas, ["red", "stops"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["green", "stops"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["somethingelse", "stops"])
    assert response.exit_code == 0


def test_status():
    """Test if running luas <line> status returns successfull with a valid result"""
    response = runner.invoke(luas, ["red", "status"])

    assert response.exit_code == 0
    assert response.output == "Red Line services operating normally\n"

    response = runner.invoke(luas, ["green", "status"])

    assert response.exit_code == 0
    assert response.output == "Green Line services operating normally\n"

    response = runner.invoke(luas, ["somethingelse", "status"])

    assert response.exit_code == 0
    assert response.output == "The line somethingelse doesn't exist\n"


@mock.patch("luascli.main.click")
def test_map(mock_click):
    """Test if running luas <line> map returns successfull or not,
    depending on the input
    """
    mock_click.launch.return_value = ""

    response = runner.invoke(luas, ["red", "map", "cit"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["green", "map", "ran"])
    assert response.exit_code == 0

    response = runner.invoke(luas, ["somethingelse", "map", "cit"])
    assert response.exit_code == 1

    response = runner.invoke(luas, ["green", "map", "cit"])
    assert response.exit_code == 0
