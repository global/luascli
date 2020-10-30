# -*- coding: utf-8 -*-

import click
import requests
from luascli.util import xml_to_dict, get_address_by_coordinates
from luascli.exceptions import LuasStopNotFound, LuasLineNotFound
from xml.parsers.expat import ExpatError
from luascli import config


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

    try:
        doc = xml_to_dict(ops.text)
    except ExpatError:
        raise LuasStopNotFound

    try:
        stop_status = doc["stopInfo"]["message"]
    except KeyError:
        raise LuasStopNotFound

    return stop_status


def get_stops(line_name):
    """Get the list of stops and their details

    Args:
        line_name: LUAS line (red/green)

    Returns:
        A list of LUAS stops of a particular line with their details:
        abbreviated name, full name, park and ride support, cycle and ride support, location (lat/lon).
    """
    res = requests.get(
        "https://luasforecasts.rpa.ie/xml/get.ashx?action=stops&encrypt=false"
    )
    output = []
    stops = xml_to_dict(res.text)
    lines = stops["stops"]["line"]
    for line in lines:
        if line["@name"] == config.luas[line_name]["full_name"]:
            for stop in line["stop"]:
                output.append(
                    {
                        "abrev": stop["@abrev"],
                        "text": stop["@pronunciation"],
                        "park_ride": stop["@isParkRide"],
                        "cycle_ride": stop["@isCycleRide"],
                        "lat": stop["@lat"],
                        "lon": stop["@long"],
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

    raise LuasStopNotFound


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


def get_address(stop):
    """Get the address of a LUAS stop, according to its lat/lon information
    Args:
        stop: stop: LUAS stop abbreviated name

    Returns:
        The address of a Luas stop, in dict format
    """

    line_name = find_line_by_stop(stop)
    stop = get_stop_detail(stop, line_name)
    address = get_address_by_coordinates(stop["lat"], stop["lon"])

    return address


def find_line_by_stop(stop):
    """Return the abbreviated name (e.g. gree/red) of the Luas Line

    Args:
        stop: stop: LUAS stop abbreviated name
        line_name: LUAS line (red/green)

    Returns:
        The address of a Luas stop, in dict format
    """

    stops = get_stops

    for line in config.luas.keys():
        stops = get_stops(line)
        for s in stops:
            if s["abrev"].lower() == stop.lower():
                return line

    raise LuasLineNotFound
