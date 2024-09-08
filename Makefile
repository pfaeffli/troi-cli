.PHONY: test install complete

# Variables
CLI_EXEC=troi_billing.py
CLI_TOOL_NAME=troi-billing

# Default target to run all
all: install complete

# Running tests using pytest
test:
	@echo "Running tests..."
	@if command -v python >/dev/null 2>&1; then \
	    PYTHON=python; \
	else \
	    echo >&2 "python not found. Using python3 instead."; \
	    PYTHON=python3; \
	fi; \
	eval "$$PYTHON -m pytest --cov=./"
	@echo "Tests completed."

# Installing the CLI tool
install:
	@echo "Installing CLI tool..."
	pip install -e .
	@echo "Installation completed."

# Setting up click completion
complete:
	@echo "Configuring shell completion..."
	./$(CLI_EXEC) install-completion
	@echo 'eval "$$(_TROI_BILLING_COMPLETE=source $$(which $(CLI_TOOL_NAME)))"' >> ~/.bashrc
	@echo "Shell completion configured. Please reload your shell or run 'source ~/.bashrc'."