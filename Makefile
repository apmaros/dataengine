.PHONY: test

# must use TABS instead of spaces
# otherwise fails with makefile:X: *** missing separator.  Stop.
freeze:
	pip-compile -r --no-emit-index-url --output-file=requirements-test.txt requirements/requirements-test.in
	pip-compile -r --no-emit-index-url --output-file=requirements.txt requirements/requirements.in
install:
	PIP_CONFIG_FILE=pip.conf pip install -r requirements.txt
install-test: install
	PIP_CONFIG_FILE=pip.conf pip install -r requirements-test.txt
run:
	python dataengine/main.py
test:
	python -m pytest
coverage:
	coverage run --source=dataengine --branch -m pytest test/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml
