VENV ?= .venv
PY := $(VENV)/bin/python
IMAGE ?= flask-hello:local

.PHONY: install lint format test run docker-build docker-run tf-check

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PY) -m pip install -r requirements-dev.txt

lint:
	$(VENV)/bin/ruff check .
	$(VENV)/bin/ruff format --check .

format:
	$(VENV)/bin/ruff format .
	$(VENV)/bin/ruff check --fix .

test:
	$(PY) -m pytest --cov --cov-report=term-missing

run:
	STORAGE_BACKEND=sqlite $(PY) wsgi.py

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -p 8000:8000 -e STORAGE_BACKEND=sqlite -e SQLITE_PATH=/tmp/users.db $(IMAGE)

tf-check:
	terraform fmt -check -recursive terraform
	terraform -chdir=terraform init -backend=false -input=false >/dev/null
	terraform -chdir=terraform validate
	terraform -chdir=terraform test
	terraform -chdir=terraform/bootstrap init -backend=false -input=false >/dev/null
	terraform -chdir=terraform/bootstrap validate
