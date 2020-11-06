![release](https://github.com/global/luascli/workflows/release/badge.svg)
![release candidates](https://github.com/global/luascli/workflows/release%20candidates/badge.svg)
![build and test](https://github.com/global/luascli/workflows/build%20and%20test/badge.svg)
![coverage](https://img.shields.io/codecov/c/github/global/luascli?flag=unittests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## Usage

```
Usage: luas [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  address  Display the address of the Luas stop
  fare     Calculate the fare price for adults and child between stops
  map      Launch Openstreet map URL with the stop location
  status   Check if the Luas stop is operational
  stops    List luas line stop names and its abbreviations (used in other commands)
  time     Display the the inbound/outbout timetable of a particualr luas stop
```

### Examples:

```
# Show all red luas stops and their abbreviations (to be used with other commands)
luas stops red

# Show the operational status of Citywest stop
luas status cit

# Show in your browser, the location of Citywest Luas Stop
luas map cit

# Display the address of a luas stop
luas address cit

# Display the inbound/outbound time table on Citiwest luas stop in json format
luas time cit --format json

# Calculate Luas Fare
luas fare cit jer --adults 2 --children 1
```