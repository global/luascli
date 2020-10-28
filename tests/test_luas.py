from luascli.luas import _xml_to_dict
import json


def test_xml_to_dict():

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

    dictA_str = json.dumps(sample_dict, sort_keys=True)
    dictB_str = json.dumps(_xml_to_dict(sample_xml), sort_keys=True)

    assert dictA_str == dictB_str
