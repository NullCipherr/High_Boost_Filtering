.PHONY: install install-dev run run-streamlit test lint docker-build docker-run

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python main.py

run-streamlit:
	streamlit run app_streamlit.py

test:
	pytest -q

lint:
	ruff check src tests

docker-build:
	docker build -t high-boost-filtering:latest .

docker-run:
	docker compose up --build
