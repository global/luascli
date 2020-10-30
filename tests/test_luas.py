from luascli.luas import (
    get_status,
    get_stops,
    get_stop_detail,
    print_stops,
    find_line_by_stop,
    get_address,
)
import json
from mock import patch
from requests.exceptions import Timeout
import pytest
from luascli.exceptions import (
    LuasLineNotFound,
    AddressLocationNotFound,
    LuasStopNotFound,
)


@patch("luascli.luas.requests")
def test_get_status(mock_requests):
    """Test if get_status() returns a valid status based on mocked data."""
    mock_requests.get.return_value.text = """
        <stopInfo created="2020-10-28T21:51:58" stop="Ranelagh" stopAbv="RAN">
            <message>Green Line services operating normally</message>
            <direction name="Inbound"><tram dueMins="10" destination="Broombridge" /></direction>
            <direction name="Outbound"><tram dueMins="DUE" destination="Sandyford" /><tram dueMins="7" destination="Bride's Glen" /></direction>
        </stopInfo>
    """

    status = get_status("ran")
    mock_requests.get.assert_called_once()
    assert status == "Green Line services operating normally"

    mock_requests.get.return_value.text = "<error></error>"
    with pytest.raises(LuasStopNotFound):
        get_status("somethingelse")


@patch("luascli.luas.requests")
def test_get_status_timeout(mock_requests):
    """Test if get_status() raises a Timeout with a side effect."""
    mock_requests.get.side_effect = Timeout

    with pytest.raises(Timeout):
        get_status("ran")

    mock_requests.get.assert_called_once()


@patch("luascli.luas.requests")
def test_get_stops(mock_requests):
    """Test if get_stops() returns a valid list of stops based on mocked_data."""
    mock_requests.get.return_value.text = """
    <stops>
    <line name="Luas Red Line">
        <stop abrev="TPT" isParkRide="0" isCycleRide="0" lat="53.34835" long="-6.22925833333333" pronunciation="The Point">The Point</stop>
        <stop abrev="SDK" isParkRide="0" isCycleRide="0" lat="53.3488222222222" long="-6.23714722222222" pronunciation="Spencer Dock">Spencer Dock</stop>
    </line>
    <line name="Luas Green Line">
        <stop abrev="BRO" isParkRide="0" isCycleRide="0" lat="53.37223956" long="-6.29768465" pronunciation="Broombridge">Broombridge</stop>
    </line>
    </stops>
    """

    actual = get_stops("red")
    expected = [
        {
            "abrev": "TPT",
            "text": "The Point",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.34835",
            "lon": "-6.22925833333333",
        },
        {
            "abrev": "SDK",
            "text": "Spencer Dock",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.3488222222222",
            "lon": "-6.23714722222222",
        },
    ]

    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])


@patch("luascli.luas.get_stops")
def test_get_stop_detail(mock_get_stops):
    """Test if get_stop_detail returns a stop dictionary based on mocked data."""
    mock_get_stops.return_value = [
        {
            "abrev": "TPT",
            "text": "The Point",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.34835",
            "lon": "-6.22925833333333",
        },
        {
            "abrev": "SDK",
            "text": "Spencer Dock",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.3488222222222",
            "lon": "-6.23714722222222",
        },
    ]

    actual_dict = get_stop_detail("TPT", "Luas Red Line")
    expected_dict = {
        "abrev": "TPT",
        "text": "The Point",
        "park_ride": "0",
        "cycle_ride": "0",
        "lat": "53.34835",
        "lon": "-6.22925833333333",
    }

    expected_str = json.dumps(expected_dict, sort_keys=True)
    actual_str = json.dumps(actual_dict, sort_keys=True)

    assert expected_str == actual_str

    # Testing None case
    with pytest.raises(LuasStopNotFound):
        actual_dict = get_stop_detail("FAKE", "Luas Red Line")


@patch("luascli.luas.click")
def test_print_stops(mock_click):
    """Test if print_stops calls click.echo as expected."""

    mock_stops = [
        {
            "abrev": "TPT",
            "text": "The Point",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.34835",
            "lon": "-6.22925833333333",
        },
        {
            "abrev": "SDK",
            "text": "Spencer Dock",
            "park_ride": "0",
            "cycle_ride": "0",
            "lat": "53.3488222222222",
            "lon": "-6.23714722222222",
        },
    ]

    mock_click.echo.return_value = ""
    print_stops(mock_stops)

    assert mock_click.echo.call_count == 2


def test_get_address():
    """Test if get_address returns positive results"""

    address = get_address("ran")
    assert address["postcode"] == "D06 R9X5"


def test_find_line_by_stop():
    """Test if find_line_by_Stop returns can find which Luas line a stop belongs to"""

    line = find_line_by_stop("ran")
    assert line == "green"

    with pytest.raises(LuasLineNotFound):
        find_line_by_stop("somethingelse")
