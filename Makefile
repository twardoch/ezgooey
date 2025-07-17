# this_file: Makefile
# Makefile for ezgooey development

.PHONY: help install test lint type-check build clean release dev-setup

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev-setup:  ## Set up development environment
	@echo "🔧 Setting up development environment..."
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r requirements-dev.txt
	@echo "✅ Development environment ready!"
	@echo "💡 Activate with: source venv/bin/activate"

install:  ## Install the package in development mode
	pip install -e .

test:  ## Run the test suite
	@echo "🧪 Running tests..."
	./scripts/test.sh

lint:  ## Run linting checks
	@echo "🔍 Running linting..."
	python -m flake8 ezgooey/ --max-line-length=88 --ignore=E203,W503

type-check:  ## Run type checking
	@echo "🔍 Running type checking..."
	python -m mypy ezgooey/ --ignore-missing-imports

build:  ## Build the package
	@echo "🏗️  Building package..."
	./scripts/build.sh

clean:  ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

release-patch:  ## Create a patch release (x.x.X)
	@read -p "Enter release message: " message; \
	./scripts/release.sh patch "$$message"

release-minor:  ## Create a minor release (x.X.x)
	@read -p "Enter release message: " message; \
	./scripts/release.sh minor "$$message"

release-major:  ## Create a major release (X.x.x)
	@read -p "Enter release message: " message; \
	./scripts/release.sh major "$$message"

version:  ## Show current version
	@python3 version.py get

# Development shortcuts
dev: dev-setup  ## Alias for dev-setup
check: test lint type-check  ## Run all checks
all: clean build test  ## Clean, build, and test