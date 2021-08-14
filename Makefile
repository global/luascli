.PHONY: init check test build publish clean

ifdef OS
  # windows version
  SHELL=cmd
  PYTHON=$(shell where.exe python)
else
  UNAME_S := $(shell uname -s)
  ifeq ($(UNAME_S), Linux)
    PYTHON=$(shell which python3 || which python)
    PIP=$(shell which pip3 || which pip)
    PIPENV=$(HOME)/.local/bin/pipenv
  endif
  ifeq ($(UNAME_S),Darwin)
    PYTHON=$(shell which python3 || which python)
    PIP=$(shell which pip3 || which pip)
    PIPENV=$(HOME)/.local/bin/pipenv
  endif
endif


init:
	$(PIP) install pipenv --upgrade
	PIPENV_VERBOSITY=-1 $(PIPENV) install --dev --pre

check:
	PIPENV_VERBOSITY=-1 $(PIPENV) run flake8 --ignore=E501,W503 luascli
	PIPENV_VERBOSITY=-1 $(PIPENV) run bandit -r luascli
	PIPENV_VERBOSITY=-1 $(PIPENV) run black . --check

test:
	PIPENV_VERBOSITY=-1 $(PIPENV) run coverage run --source=luascli --omit=luascli/__version__.py -m pytest tests
	PIPENV_VERBOSITY=-1 $(PIPENV) run coverage report --fail-under=100 -m
	PIPENV_VERBOSITY=-1 $(PIPENV) run coverage xml

build: init check clean test
	PIPENV_VERBOSITY=-1 $(PIPENV) run python setup.py sdist bdist_wheel

publish-test: build
	PIPENV_VERBOSITY=-1 $(PIPENV) run python -m twine check dist/*
	PIPENV_VERBOSITY=-1 $(PIPENV) run python -m twine upload --repository testpypi dist/*
	make clean

publish: build
	PIPENV_VERBOSITY=-1 $(PIPENV) run python -m twine check dist/*
	PIPENV_VERBOSITY=-1 $(PIPENV) run python -m twine upload dist/*
	make clean

local-install: build
	$(PIP) install --editable .

clean:
	rm -rf build dist .egg luascli.egg-info .coverage coverage.xml

help:
	@echo "This project assumes that you have python and pip installed."
	@echo "The following make targets are available:"
	@echo " init 	 		install all dependencies for dev env"
	@echo " check	 		check for flake8 syntax issues"
	@echo " test			run tests"
	@echo " build   		build your code and generate binaries to be published"
	@echo " publish-test		submit your code to pypi-test repository (requires .pypirc)"
	@echo " publish 		submit your code to pypi repository (requires .pypirc)"
	@echo " local-install 		Install luascli in editable mode (i.e. setuptools 'develop mode')"
	@echo " clean			cleanup your build"
	@echo " help			display this information"
