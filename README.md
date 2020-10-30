# Overview

This is a CLI tool that helps you to get LUAS Irish Transport information. This tool is based on the [Luas Forecasting API](https://data.gov.ie/dataset/luas-forecasting-api/resource/078346e0-fe7f-4e71-9c51-21c78520dc3d) integrated with the [Open Street Map API](https://www.openstreetmap.org/)

`luascli` is licensed under the MIT license.

## Basic information

This CLI uses the following format:

```
luas command <arguments> [parameters]
```

where 

`<argument>` : commands can have arguments and/or optional parameters. The most comonn is the `<stop>` which means the abbreviated stop name. You can get it from `stops` command. Another one is `<line>` which could be red/green.

## How to install

```
pip install luascli
```

## How to use

```
luas <command> <arguments> [parameters]
luas --help
```
### Commands

- stops: list all stops for a particular line
- status: show the operational status of the line
- map: display the location of the luas stop on the map (default browser)
- address: display the address of a particular luas stop

Examples:

```
# Show all red luas stops and their abbreviations (to be used with other commands)
luas stops red

# Show the operational status of Citywest stop
luas status cit

# Show in your browser, the location of Citywest Luas Stop
luas map cit

# Display the address of a luas stop
luas address cit
```