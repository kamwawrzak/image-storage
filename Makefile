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