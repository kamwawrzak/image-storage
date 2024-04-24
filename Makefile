.PHONY: run-server
run-server:
	python3 main.py

.PHONY: install-deps
install-deps:
	pip install -r requirements.txt

.PHONY: update-deps
update-deps:
	pip freeze > requirements.txt

.PHONY: setup-venv
setup-venv:
	python3 -m venv venv
	venv/bin/activate

.PHONY: test-coverage
test-coverage:
	coverage run -m unittest discover

.PHONY: run-tests
run-tests:
	python -m unittest discover -v