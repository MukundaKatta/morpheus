.PHONY: install test lint run clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

run:
	morpheus --help

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
