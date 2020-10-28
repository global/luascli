# -*- coding: utf-8 -*-

import click
import requests


def _xml_to_dict(xmldata):
    """Converts XML data into python dictionary

    Args:
        xmldata: xml string

    Returns:
        dictionary with all xml elements
    """
    import xmltodict

    doc = xmltodict.parse(xmldata)
    return doc


def get_status(stop):
    """Get the operational status information of a LUAS stop

    Args:
        stop: LUAS abbreviated stop name

    Returns:
        Operational status information
    """
    ops = requests.get(
        "https://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop="
        + stop
        + "&encrypt=false"
    )
    doc = _xml_to_dict(ops.text)
    return doc["stopInfo"]["message"]


def get_stops(line_name):
    """Get the list of stops and their details

    Args:
        line_name: LUAS line (red/green)

    Returns:
        A list of LUAS stops of a particular line with their details:
        abbreviated name, full name, park and ride support, cycle and ride support, location (lat/long).
    """
    res = requests.get(
        "https://luasforecasts.rpa.ie/xml/get.ashx?action=stops&encrypt=false"
    )
    output = []
    stops = _xml_to_dict(res.text)
    lines = stops["stops"]["line"]
    for line in lines:
        if line["@name"] == line_name:
            for stop in line["stop"]:
                output.append(
                    {
                        "abrev": stop["@abrev"],
                        "text": stop["@pronunciation"],
                        "park_ride": stop["@isParkRide"],
                        "cycle_ride": stop["@isCycleRide"],
                        "lat": stop["@lat"],
                        "long": stop["@long"],
                    }
                )
    return output


def get_stop_detail(stop, line_name):
    """Get the details of one

    Args:
        stop: LUAS stop abbreviated name
        line_name: LUAS line (red/green)

    Returns:
        A dictionary with the stop details or None otherwise
    """
    all_stops = get_stops(line_name)
    for s in all_stops:
        if s["abrev"].lower() == stop.lower():
            return s

    return None


def print_stops(stops):
    """Print the list of all stops

    Args:
        stops: list container all stops with their details - from get_stops()

    Returns:
        None
    """
    for stop in stops:
        abrev = stop["abrev"]
        text = stop["text"]
        park = "Park and Ride" if stop["park_ride"] == "1" else "No park"
        cycle = "Cycle and Ride" if stop["cycle_ride"] == "1" else "No cycle"
        click.echo(f"{abrev:<6}{text:<20}{park:^20}{cycle:^30}")

    return None
