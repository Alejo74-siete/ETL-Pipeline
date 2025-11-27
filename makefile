.PHONY: install test format lint run

install:
	pip install -r requirements.txt

test:
	pytest -q

format:
	black .

lint:
	flake8 .

run:
	python -c "from src.pipeline import production_etl_flow; production_etl_flow()"
