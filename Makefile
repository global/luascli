.PHONY: init check test build publish clean

init:
	pip install pipenv --upgrade
	PIPENV_VERBOSITY=-1 pipenv install --dev

check:
	PIPENV_VERBOSITY=-1 pipenv run flake8 --ignore=E501 luascli

build: init check clean
	python setup.py sdist bdist_wheel

publish-test: build
	python -m twine check dist/*
	python -m twine upload --repository testpypi dist/*
	make clean

publish: build
	python -m twine check dist/*
	python -m twine upload dist/*
	make clean

clean:
	rm -rf build dist .egg luascli.egg-info

help:
	@echo "This project assumes that you have python and pip installed."
	@echo "The following make targets are available:"
	@echo " init 	 		install all dependencies for dev env"
	@echo " check	 		check for flake8 syntax issues"
	@echo " build   		build your code and generate binaries to be published"
	@echo " publish-test		submit your code to pypi-test repository"
	@echo " publish 		submit your code to pypi repository"
	@echo " clean			cleanup your build"
	@echo " help			display this information"
