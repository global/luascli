# -*- coding: utf-8 -*-

import click
from luascli.luas import get_stops, get_stop_detail, get_status, print_stops
import sys


@click.group()
@click.version_option()
@click.argument("line")
@click.pass_context
def luas(ctx, line):
    ctx.ensure_object(dict)
    ctx.obj["line"] = line


@luas.command()
@click.pass_context
def stops(ctx):
    """List luas line stop names and its abbreviations to be used
    with others subcommands.
    """
    if ctx.obj["line"] == "red":
        line_name = "Luas Red Line"
        s = get_stops(line_name)
        click.echo("\n" + line_name + "\n")
        print_stops(s)
    elif ctx.obj["line"] == "green":
        line_name = "Luas Green Line"
        s = get_stops(line_name)
        click.echo("\n" + line_name + "\n")
        print_stops(s)
    else:
        click.echo("The line " + ctx.obj["line"] + " doesn't exist")


@luas.command()
@click.pass_context
def status(ctx):
    """Check if the line is operational"""
    if ctx.obj["line"] == "red":
        click.echo(get_status("red"))
    elif ctx.obj["line"] == "green":
        click.echo(get_status("ran"))
    else:
        click.echo("The line " + ctx.obj["line"] + " doesn't exist")


@luas.command()
@click.pass_context
@click.argument("stop")
def map(ctx, stop):
    """Launch Openstreet map URL with the stop location"""
    if ctx.obj["line"] == "red":
        line_name = "Luas Red Line"
    elif ctx.obj["line"] == "green":
        line_name = "Luas Green Line"
    else:
        click.echo("The line " + ctx.obj["line"] + " doesn't exist")
        sys.exit(1)

    s = get_stop_detail(stop, line_name)
    if s is not None:
        click.launch(
            "https://www.openstreetmap.org/?mlat="
            + s["lat"]
            + "&mlon="
            + s["long"]
            + "zoom=14#map=14"
        )
    else:
        click.echo(
            "Couldn't find the location for the stop "
            + stop
            + " on the line "
            + ctx.obj["line"]
        )


if __name__ == "__main__":
    luas(obj={})
