.PHONY: build docker-build docker-run run test

build:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

docker-build:
	docker build -t docd-ai:latest .

docker-run:
	docker run --rm -p 8000:8000 docd-ai:latest

run:
	uvicorn src.app:app --reload --host 127.0.0.1 --port 8000

test:
	python -m pytest -q
