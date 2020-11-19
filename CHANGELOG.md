
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.10.0] - 2020-11-11

# Added

- Update the license information to include Irish Public Sector Data license

# [0.9.0] - 2020-11-11

# Added

- Added format text/json to `luas address` command

# [0.8.0] - 2020-11-06

# Added

- Build / test / release badges in the README.md file
- Added codecov.io integration in the ci/cd pipelines

# [0.7.0] - 2020-11-06

# Added

- You can now calculate the fare of your journey with `luas fare begin_journey end_journey --adults N --children Y`

# [0.6.0] - 2020-11-01

# Added

- You can now get the timetable of a Luas stop using `luas time <stop>` in 2 formats: json and text

# [0.5.0] - 2020-10-30

# Added

- You can now get the address of a Luas stop using `luas address <stop>`
- Added better error handling
- Configuration is now stored in config.py

# Changed

- Complete refactor of cli to simplify code and parameter passing

## [0.4.0] - 2020-10-29

### Added

- Unit testing to all components with 100% coverage

## [0.3.0] - 2020-10-28

### Added

- CI/CD pipeline allow us to build and publish the tool with a new tag is generated
- CONTRIBUTING.md document with development information
- Added initial test setup
- Added bandit for static code security analysis
- Added black as our pep8 formatting tool

### Changed

- Fixed flake8 dependency missing in the pipenv configuration

## [0.2.0] - 2020-10-27

### Added

- luas <line> map <stop> - open the location of the luas stop in a browser
- lias <line> status - shows operational status for all lines
- luas <line> stops - display the list of all stops for a particular line