default:
	@make run

run:
	python main.py

web:
	pygbag main.py

web-build:
	pygbag --build main.py

init:
	@pip install -U pip; \
	pip install -e ".[dev]"; \
	pre-commit install; \

pre-commit:
	pre-commit install

pre-commit-all:
	pre-commit run --all-files

format:
	black .

lint:
	flake8 --config=../.flake8 --output-file=./coverage/flake8-report --format=default
