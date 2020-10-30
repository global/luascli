# -*- coding: utf-8 -*-

import requests
from luascli.exceptions import AddressLocationNotFound


def xml_to_dict(xmldata):
    """Converts XML data into python dictionary

    Args:
        xmldata: xml string

    Returns:
        dictionary with all xml elements
    """
    import xmltodict

    doc = xmltodict.parse(xmldata)
    return doc


def get_address_by_coordinates(lat, lon):
    """Get the address by coordinate - lat/logn

    Args:
        lat: latitude coordinate
        lon: itude coordinate

    Returns:
        A dictionary container the address based on lat/ coordinates or {} otherwise
    """

    output = {}
    resp = requests.get(
        "https://nominatim.openstreetmap.org/reverse?format=xml&lat="
        + lat
        + "&lon="
        + lon
        + "&zoom=18&addressdetails=1"
    )

    parsed_address = xml_to_dict(resp.text)

    if "error" in parsed_address["reversegeocode"].keys():
        raise AddressLocationNotFound(lat, lon)

    output["full_address"] = parsed_address["reversegeocode"]["result"].get("#text", "")
    output["house_number"] = parsed_address["reversegeocode"]["addressparts"].get(
        "house_number", ""
    )
    output["road"] = parsed_address["reversegeocode"]["addressparts"].get("road", "")
    output["town"] = parsed_address["reversegeocode"]["addressparts"].get("town", "")
    output["city"] = parsed_address["reversegeocode"]["addressparts"].get("city", "")
    output["county"] = parsed_address["reversegeocode"]["addressparts"].get(
        "county", ""
    )
    output["state"] = parsed_address["reversegeocode"]["addressparts"].get("state", "")
    output["postcode"] = parsed_address["reversegeocode"]["addressparts"].get(
        "postcode", ""
    )
    output["country"] = parsed_address["reversegeocode"]["addressparts"].get(
        "country", ""
    )
    output["country_code"] = parsed_address["reversegeocode"]["addressparts"].get(
        "country_code", ""
    )

    return output
