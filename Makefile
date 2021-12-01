# must use TABS instead of spaces
# otherwise fails with makefile:X: *** missing separator.  Stop.

freeze:
	python -m pip freeze > requirements.txt
install:
	PIP_CONFIG_FILE=pip.conf pip install -r requirements.txt
run:
	python dataengine/main.py
test:
	JWT_SECRET=secret python -m pytest
