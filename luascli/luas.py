# -*- coding: utf-8 -*-

import click
import requests
from luascli.util import xml_to_dict, get_address_by_coordinates
from luascli.exceptions import (
    LuasStopNotFound,
    LuasLineNotFound,
    LuasStopsNotOnSameLine,
)
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


def get_timetable(stop):
    """Get the operational timetable of a particular Luas stop

    Args:
        stop: LUAS abbreviated stop name

    Returns:
        List of inbound/outbound timetable of a particular luas stopp
    """

    timetable = {}

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
        for direction in doc["stopInfo"]["direction"]:
            d = direction["@name"].lower()
            timetable[d] = []
            if isinstance(direction["tram"], list):
                for tram in direction["tram"]:
                    timetable[d].append(
                        {
                            "dueMins": tram.get("@dueMins", ""),
                            "destination": tram.get("@destination", ""),
                        }
                    )
            else:
                tram = direction["tram"]
                timetable[d].append(
                    {
                        "dueMins": tram.get("@dueMins", ""),
                        "destination": tram.get("@destination", ""),
                    }
                )
        return timetable
    except KeyError:
        raise LuasStopNotFound


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
        stop: LUAS stop abbreviated name

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


def is_not_valid_stop(stop):
    """Validate if stop name exists in the luas line

    Args:
        stop: LUAS stop abbreviated name

    Returns:
        True if stop is not valid and False otherwise
    """

    try:
        find_line_by_stop(stop)
        return False
    except LuasLineNotFound:
        return True


def are_stops_on_same_line(first_stop, second_stop):
    """Validate if stop name exists in the luas line

    Args:
        first_stop: LUAS stop abbreviated name
        second_stop: LUAS stop abbreviated name

    Returns:
        True if both stops belongs to the same line, False otherwise
    """

    try:
        line1 = find_line_by_stop(first_stop)
        line2 = find_line_by_stop(second_stop)
        if line1 == line2:
            return True
    except (LuasStopNotFound, LuasLineNotFound):
        return False

    return False


def calculate_fare(begin_journey, end_journey, num_adults=0, num_children=0):
    """Calculates the fare between two stops

    Args:
        stop: stop: LUAS stop abbreviated name

    Returns:
        True if stops exists or False otherwise
    """

    if (
        num_adults < 0
        or not isinstance(num_adults, int)
        or num_children < 0
        or not isinstance(num_children, int)
    ):
        raise ValueError

    if is_not_valid_stop(begin_journey):
        raise LuasStopNotFound(begin_journey)
    elif is_not_valid_stop(end_journey):
        raise LuasStopNotFound(end_journey)

    if are_stops_on_same_line(begin_journey, end_journey):

        response = requests.get(
            "https://luasforecasts.rpa.ie/xml/get.ashx?action=farecalc&from="
            + begin_journey
            + "&to="
            + end_journey
            + "&adults="
            + str(num_adults)
            + "&children="
            + str(num_children)
            + "&encrypt=false"
        )

        output = {}
        fare_dict = xml_to_dict(response.text)
        output["from"] = begin_journey
        output["to"] = end_journey
        output["adults"] = num_adults
        output["children"] = num_children
        output["fare_peak"] = fare_dict["farecalc"]["result"].get("@peak", "")
        output["fare_offpeak"] = fare_dict["farecalc"]["result"].get("@offpeak", "")
        output["zones_travelled"] = fare_dict["farecalc"]["result"].get(
            "@zonesTravelled", ""
        )

        return output

    else:
        raise LuasStopsNotOnSameLine(begin_journey, end_journey)
