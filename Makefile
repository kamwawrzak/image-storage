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

.PHONY: test-coverage-html
test-coverage-html: test-coverage
	coverage html

.PHONY: run-tests
run-tests:
	python -m unittest discover -v

.PHONY: start-localstack
start-localstack:
	 localstack start -d --network localstack_network

.PHONY: docker-build
docker-build:
	docker build -t image-storage:latest .

.PHONY: docker-run
docker-run:
	docker-compose up -d

.PHONY: docker-stop
docker-stop:
	docker-compose down

.PHONY: lint
lint:
	pylint app/
