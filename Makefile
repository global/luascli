.PHONY: init check test build publish clean

init:
	pip install pipenv --upgrade
	PIPENV_VERBOSITY=-1 pipenv install --dev

check:
	PIPENV_VERBOSITY=-1 pipenv run flake8 --ignore=E501,W503 luascli
	PIPENV_VERBOSITY=-1 pipenv run bandit -r luascli
	PIPENV_VERBOSITY=-1 pipenv run black . --check

test:
	PIPENV_VERBOSITY=-1 pipenv run coverage run --source=luascli -m pytest tests
	PIPENV_VERBOSITY=-1 pipenv run coverage report --fail-under=10

build: init check clean test
	PIPENV_VERBOSITY=-1 pipenv run python setup.py sdist bdist_wheel

publish-test: build
	PIPENV_VERBOSITY=-1 pipenv run python -m twine check dist/*
	PIPENV_VERBOSITY=-1 pipenv run python -m twine upload --repository testpypi dist/*
	make clean

publish: build
	PIPENV_VERBOSITY=-1 pipenv run python -m twine check dist/*
	PIPENV_VERBOSITY=-1 pipenv run python -m twine upload dist/*
	make clean

local-install: build
	python install --editable .

clean:
	rm -rf build dist .egg luascli.egg-info .coverage

help:
	@echo "This project assumes that you have python and pip installed."
	@echo "The following make targets are available:"
	@echo " init 	 		install all dependencies for dev env"
	@echo " check	 		check for flake8 syntax issues"
	@echo " test			run tests"
	@echo " build   		build your code and generate binaries to be published"
	@echo " publish-test		submit your code to pypi-test repository"
	@echo " publish 		submit your code to pypi repository"
	@echo " local-install 		Install luascli in editable mode (i.e. setuptools 'develop mode')"
	@echo " clean			cleanup your build"
	@echo " help			display this information"
