.PHONY: test install complete

# Variables
CLI_EXEC=troi-billing.py
CLI_TOOL_NAME=troi-billing

# Default target to run all
all: test install complete

# Running tests using pytest
test:
	@echo "Running tests..."
	python -m pytest --cov=./tests
	@echo "Tests completed."

# Installing the CLI tool
install:
	@echo "Installing CLI tool..."
	pip install -e .
	@echo "Installation completed."

# Setting up click completion
complete:
	@echo "Configuring shell completion..."
	-@$(CLI_EXEC) --install-completion
	-echo 'eval "$(_TROI_BILLING_COMPLETE=source_bash $(which $(CLI_TOOL_NAME)))"' >> ~/.bashrc
	@echo "Shell completion configured."