# Overview

This page describes how to contribute and some guidelines used in the project, including technical details. 

## License

This project has been released under MIT License. Please check [LICENSE](https://github.com/global/luascli/blob/main/LICENSE) for more information.

## How to start

### Pre-requisites

- Install python and pip on your environment (windows/mac/linux)
- Install GNU Make

### Setup development environment

Download the source code and install dependencies
```
git clone https://github.com/global/luascli.git
cd luascli
make init
```

Get help
```
make help
```

Build the code
```
make build
```

Run tests
```
make test
```

Install locally
```
make install-local
```

Publish to pypitest and pypi (this requires .pypirc file to be configured)
```
make publish-test
make publish
```

## How to submit a new idea, code, question or bug report

If you have an idea how we can improve the code or the product, fix a bug or a simple question, please submit an [issue](https://github.com/global/luascli/issues).

## Technologies used

This is our tech stack:

Development
- Python 3
- Setuptools: configure the binary release information
- Pip, pipenv: install and manage dependencies
- GNU Make: directives to setup the environment, test, compile, install locally and publish the binaries
- black: pep8 formatting

Main Libraries
- requests: connect to downstream APIs
- xmltodict: xml parsing
- click: cmdline support 

Testing
- flake8: syntax check
- pytest: unit testing
- coverage: check test coverage
- bandit: static code analysis

CI/CD
- Github: source code, documentation and release information
- github actions: ci/cd pipeline to build/test/release the code
- Pypi and Pypytest: repository to store the python binaries

Documentation
- Markdown

## Pipeline

We have multiple workflows defined in github actions (.github/workflows). 

- build: on every push to feature/* branches, it will trigger the build pipeline that run tests and build the app
- release-rc: on every tags/*-rc* it will publish to pypi-test
- release: on every tags/** excluding tags/*-rc* it will publish to pypi

### Conventions

- Branching: every branch should start with *feature/* prefix to trigger the build pipeline
- Releasing and tagging: When ready to release, create a release in github with the version format x.y.z (semantic versioning). If it is a release candidate, add -rcNN to the end of the name.