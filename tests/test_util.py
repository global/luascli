from luascli.util import xml_to_dict, get_address_by_coordinates
from luascli.exceptions import AddressLocationNotFound
import json
import pytest


def test_xml_to_dict():
    """Test if xml_to_dict returns a valid dictionary with the
    correct contents.
    """

    sample_xml = """
    <stops>
    <line name="Luas Red Line">
        <stop pronunciation="The Point">The Point</stop>
        <stop pronunciation="Spencer Dock">Spencer Dock</stop>
    </line>
    </stops>
    """
    sample_dict = {
        "stops": {
            "line": {
                "@name": "Luas Red Line",
                "stop": [
                    {"#text": "The Point", "@pronunciation": "The Point"},
                    {"#text": "Spencer Dock", "@pronunciation": "Spencer Dock"},
                ],
            }
        }
    }

    expected_str = json.dumps(sample_dict, sort_keys=True)
    actual_str = json.dumps(xml_to_dict(sample_xml), sort_keys=True)

    assert expected_str == actual_str


def test_get_address_by_coordinates():
    """Test if _xml_to_dict returns a valid dictionary with the
    correct contents.
    """

    address = get_address_by_coordinates("53.28783255", "-6.418914583333")
    assert address["postcode"] == "D24 YX53"

    with pytest.raises(AddressLocationNotFound):
        get_address_by_coordinates("1234", "5678")
