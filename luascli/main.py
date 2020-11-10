# -*- coding: utf-8 -*-

import click
from luascli.luas import (
    get_stops,
    get_stop_detail,
    get_status,
    print_stops,
    get_address,
    find_line_by_stop,
    get_timetable,
    calculate_fare,
)
from luascli import config
from luascli.exceptions import (
    LuasStopNotFound,
    LuasLineNotFound,
    AddressLocationNotFound,
)
import sys
import pprint


@click.group()
@click.version_option()
def luas():
    pass


@luas.command()
@click.argument("line")
def stops(line):
    """List luas line stop names and its abbreviations (used in other commands)"""

    try:
        s = get_stops(line)
        click.echo("\n" + config.luas[line]["full_name"] + "\n")
        print_stops(s)
    except KeyError:
        click.echo("The line " + line + " doesn't exist")
        sys.exit(1)


@luas.command()
@click.argument("stop")
def status(stop):
    """Check if the Luas stop is operational"""
    try:
        click.echo(get_status(stop))
    except LuasStopNotFound:
        click.echo("The stop " + stop + " doesn't exist")
        sys.exit(1)
    except (ConnectionError, TimeoutError):
        click.echo("Can't connect to " + config.forecast_api["url"])
        sys.exit(2)


@luas.command()
@click.argument("stop")
def map(stop):
    """Launch Openstreet map URL with the stop location"""

    try:
        line_short_name = find_line_by_stop(stop)
    except LuasLineNotFound:
        click.echo("Couldn't find luas line for the stop " + stop)
        sys.exit(1)

    try:
        s = get_stop_detail(stop, line_short_name)
        click.launch(
            "https://www.openstreetmap.org/?mlat="
            + s["lat"]
            + "&mlon="
            + s["lon"]
            + "zoom=14#map=14"
        )
    except LuasStopNotFound:
        click.echo(
            "Couldn't find the location for the stop "
            + stop
            + " on the line "
            + line_short_name
        )
        sys.exit(1)


@luas.command()
@click.option(
    "--format",
    "-f",
    default="text",
    nargs=1,
    show_default=True,
    help="Output format (Valid options: json/text)",
)
@click.argument("stop")
def address(stop, format):
    """Display the address of the Luas stop"""

    try:
        address = get_address(stop)
        if format == "text":
            for key, value in address.items():
                click.echo(key.replace("_", " ").capitalize() + ": " + str(value))
        else:
            pprint.pprint(address)
    except (LuasStopNotFound, LuasLineNotFound):
        click.echo("The Luas stop " + stop + " doesn't exist.")
        sys.exit(1)
    except AddressLocationNotFound as alnf:
        click.echo(
            "Address location not found at lat=" + alnf.lat + "lon=" + alnf.lon + ""
        )
        sys.exit(2)


@luas.command()
@click.argument("stop")
@click.option(
    "--format",
    "-f",
    default="text",
    nargs=1,
    show_default=True,
    help="Output format (Valid options: json/text)",
)
def time(stop, format):
    """Display the the inbound/outbout timetable of a particualr luas stop"""

    try:
        timetable = get_timetable(stop)
        if format == "text":
            for dest in timetable.keys():
                click.echo(dest.capitalize())
                for tram in timetable[dest]:
                    click.echo(
                        "\tDestination: "
                        + tram["destination"]
                        + " - Due: "
                        + tram["dueMins"]
                    )
        elif format == "json":
            pprint.pprint(timetable)
        else:
            click.echo("Format " + format + " is not valid.")
            sys.exit(3)
    except LuasStopNotFound:
        click.echo("The Luas stop " + stop + " doesn't exist.")
        sys.exit(1)


@luas.command()
@click.argument("begin_journey")
@click.argument("end_journey")
@click.option(
    "--adults", "-a", nargs=1, default=0, show_default=True, help="Number of adults"
)
@click.option(
    "--children", "-c", nargs=1, default=0, show_default=True, help="Number of children"
)
@click.option(
    "--format",
    "-f",
    default="text",
    nargs=1,
    show_default=True,
    help="Output format (Valid options: json/text)",
)
def fare(begin_journey, end_journey, adults, children, format):
    """Calculate the fare price for adults and child between stops"""
    try:
        fare = calculate_fare(begin_journey, end_journey, adults, children)
        line = find_line_by_stop(begin_journey)
        s1 = get_stop_detail(begin_journey, line)
        s2 = get_stop_detail(end_journey, line)
        if format == "text":
            for key, value in fare.items():
                if key == "from":
                    click.echo(
                        key.replace("_", " ").capitalize() + ": " + str(s1["text"])
                    )
                elif key == "to":
                    click.echo(
                        key.replace("_", " ").capitalize() + ": " + str(s2["text"])
                    )
                else:
                    click.echo(key.replace("_", " ").capitalize() + ": " + str(value))
        elif format == "json":
            pprint.pprint(fare)
        else:
            click.echo("Format " + format + " is not valid.")
            sys.exit(3)
    except LuasStopNotFound as lsnf:
        click.echo("The Luas stop " + lsnf.stop + " doesn't exist.")
        sys.exit(1)


if __name__ == "__main__":
    luas()
