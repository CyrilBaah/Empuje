# Makefile for Empuje

# Define variables
ENV := env
PYTHON := $(ENV)/bin/python
ENTRYPOINT := empuje.py 

.PHONY: all run all clean


test:
	@echo "Unit tests"
	@$(PYTHON) -m pytest tests

version:
	@$(PYTHON) -m empuje -v

lint:
	./scripts/run-linters.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "  test      Run unit tests"
	@echo "  lint      Check code style, formating and linting"
	@echo "  clean     Remove temporary files and the virtual environment"
	@echo "  help      Show this help message"
