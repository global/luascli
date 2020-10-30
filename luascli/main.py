# -*- coding: utf-8 -*-

import click
from luascli.luas import (
    get_stops,
    get_stop_detail,
    get_status,
    print_stops,
    get_address,
    find_line_by_stop,
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
    """List luas line stop names and its abbreviations to be used
    with others subcommands.
    """

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
@click.argument("stop")
def address(stop):
    """Display the address of the Luas stop"""

    try:
        address = get_address(stop)
        pprint.pprint(address)
    except (LuasStopNotFound, LuasLineNotFound):
        click.echo("The Luas stop " + stop + " doesn't exist.")
        sys.exit(1)
    except AddressLocationNotFound as alnf:
        click.echo(
            "Address location not found at lat=" + alnf.lat + "lon=" + alnf.lon + ""
        )
        sys.exit(2)


if __name__ == "__main__":
    luas()
