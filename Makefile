# Makefile for Empuje

# Define variables
ENV := env
PYTHON := $(ENV)/bin/python
ENTRYPOINT := empuje.py 

.PHONY: all run all clean


# Run unit tests
test:
	@echo "🚀 Running unit tests..."
	@$(PYTHON) -m pytest tests
	@echo "✅ Tests completed!"

# Check the version of Empuje
version:
	@echo "🔍 Checking Empuje version..."
	@$(PYTHON) -m empuje -v
	@echo "✨ Version check complete!"

# Run linters to ensure code quality
lint:
	@echo "🧹 Running linters..."
	@./scripts/run-linters.sh
	@echo "🌟 Code is clean and lint-free!"

# Clean up temporary files and caches
clean:
	@echo "🧼 Cleaning up temporary files and caches..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✨ Workspace is squeaky clean!"

# Display help message
help:
	@echo "📖 Available commands:"
	@echo "  test      🚀 Run unit tests"
	@echo "  lint      🧹 Check code style, formatting, and linting"
	@echo "  clean     🧼 Remove temporary files and caches"
	@echo "  help      📖 Show this help message"
	@echo "  version   🔍 Check the version of Empuje"
	@echo "🌟 Happy coding!"
