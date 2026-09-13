.PHONY: help install install-dev test lint format clean run setup

# Variables
PYTHON := python3
PIP := pip3
VENV := venv

help:
	@echo "ClipFree Development Tasks"
	@echo ""
	@echo "Installation:"
	@echo "  make install       - Install dependencies in virtual environment"
	@echo "  make install-dev   - Install dev dependencies (testing, linting)"
	@echo ""
	@echo "Development:"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters (flake8, pylint)"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up temp files"
	@echo ""
	@echo "Usage:"
	@echo "  make run URL=\"https://youtube.com/watch?v=...\" - Run ClipFree"
	@echo ""

install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	@echo ""
	@echo "✅ Installed! Next steps:"
	@echo "  1. Activate venv: source $(VENV)/bin/activate"
	@echo "  2. Set API key: export GEMINI_API_KEY=\"your_key\""
	@echo "  3. Run: python clipfree.py <youtube_url>"

install-dev:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt pytest black flake8 pylint

test:
	. $(VENV)/bin/activate && pytest -v

lint:
	. $(VENV)/bin/activate && flake8 clipfree.py && pylint clipfree.py

format:
	. $(VENV)/bin/activate && black clipfree.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage
	rm -rf *.pyc *.pyo
	rm -rf build/ dist/ *.egg-info/

run:
	. $(VENV)/bin/activate && python clipfree.py $(URL)

.DEFAULT_GOAL := help
