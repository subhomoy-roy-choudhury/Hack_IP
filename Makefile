.PHONY: all clean venv deps

VENV := venv
ACTIVATE_VENV := . $(VENV)/bin/activate

all: clean venv deps

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@echo "Removed virtual environment."

venv:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Virtual environment created."

pre-commit:
	@echo "Installling pre-commit hooks"
	@pre-commit install --install-hooks

deps:
	@echo "Installing dependencies..."
	@$(ACTIVATE_VENV) && pip install --upgrade pip wheel
	@$(ACTIVATE_VENV) && pip install --upgrade poetry
	@$(ACTIVATE_VENV) && poetry install --no-cache
	@echo "Dependencies installed."

test:
	@echo "Running Test Cases..."
	@$(ACTIVATE_VENV) && pytest -v
