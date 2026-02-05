# ============================================================================
# Project Chimera: Makefile
# ============================================================================
# Standardized commands for development, testing, and deployment
#
# Usage:
#   make help          - Show all available commands
#   make setup         - Install dependencies
#   make test          - Run tests
#   make docker-up     - Start all services
# ============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# ============================================================================
# Variables
# ============================================================================

PYTHON := python3
UV := uv
DOCKER := docker
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := project-chimera

# Colors for output
COLOR_RESET := \033[0m
COLOR_BOLD := \033[1m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m

# ============================================================================
# Help Command
# ============================================================================

help: ## Show this help message
	@echo "$(COLOR_BOLD)Project Chimera - Available Commands$(COLOR_RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BOLD)Quick Start:$(COLOR_RESET)"
	@echo "  1. make setup              # Install dependencies"
	@echo "  2. make env                # Copy .env.example to .env (edit afterwards)"
	@echo "  3. make docker-up          # Start all services"
	@echo "  4. make test               # Run tests"
	@echo ""

# ============================================================================
# Setup & Installation
# ============================================================================

setup: ## Install all dependencies using uv
	@echo "$(COLOR_BLUE)Installing dependencies with uv...$(COLOR_RESET)"
	$(UV) pip install -e ".[dev]"
	@echo "$(COLOR_GREEN)✓ Dependencies installed$(COLOR_RESET)"

setup-pip: ## Install dependencies using pip (alternative to uv)
	@echo "$(COLOR_BLUE)Installing dependencies with pip...$(COLOR_RESET)"
	$(PYTHON) -m pip install -e ".[dev]"
	@echo "$(COLOR_GREEN)✓ Dependencies installed$(COLOR_RESET)"

env: ## Copy .env.example to .env
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(COLOR_GREEN)✓ Created .env file from template$(COLOR_RESET)"; \
		echo "$(COLOR_YELLOW)⚠ Edit .env and add your API keys$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ .env already exists, skipping$(COLOR_RESET)"; \
	fi

install-uv: ## Install uv package manager
	@echo "$(COLOR_BLUE)Installing uv...$(COLOR_RESET)"
	curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "$(COLOR_GREEN)✓ uv installed$(COLOR_RESET)"

# ============================================================================
# Testing
# ============================================================================

test: ## Run all tests with pytest
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	pytest tests/ -v

test-unit: ## Run only unit tests
	@echo "$(COLOR_BLUE)Running unit tests...$(COLOR_RESET)"
	pytest tests/ -v -m unit

test-integration: ## Run only integration tests
	@echo "$(COLOR_BLUE)Running integration tests...$(COLOR_RESET)"
	pytest tests/ -v -m integration

test-cov: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "$(COLOR_GREEN)✓ Coverage report generated in htmlcov/$(COLOR_RESET)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(COLOR_BLUE)Running tests in watch mode...$(COLOR_RESET)"
	ptw tests/ -- -v

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run all linters (black, ruff, mypy)
	@echo "$(COLOR_BLUE)Running linters...$(COLOR_RESET)"
	@$(MAKE) lint-black
	@$(MAKE) lint-ruff
	@$(MAKE) lint-mypy
	@echo "$(COLOR_GREEN)✓ All linters passed$(COLOR_RESET)"

lint-black: ## Check code formatting with black
	@echo "$(COLOR_BLUE)Checking code formatting...$(COLOR_RESET)"
	black --check src/ tests/

lint-ruff: ## Check code with ruff
	@echo "$(COLOR_BLUE)Running ruff...$(COLOR_RESET)"
	ruff check src/ tests/

lint-mypy: ## Run type checking with mypy
	@echo "$(COLOR_BLUE)Running type checker...$(COLOR_RESET)"
	mypy src/

format: ## Auto-format code with black
	@echo "$(COLOR_BLUE)Formatting code...$(COLOR_RESET)"
	black src/ tests/
	@echo "$(COLOR_GREEN)✓ Code formatted$(COLOR_RESET)"

format-fix: ## Auto-fix linting issues with ruff
	@echo "$(COLOR_BLUE)Auto-fixing linting issues...$(COLOR_RESET)"
	ruff check --fix src/ tests/
	@echo "$(COLOR_GREEN)✓ Linting issues fixed$(COLOR_RESET)"

# ============================================================================
# Docker Commands
# ============================================================================

docker-build: ## Build Docker images
	@echo "$(COLOR_BLUE)Building Docker images...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) build
	@echo "$(COLOR_GREEN)✓ Docker images built$(COLOR_RESET)"

docker-up: ## Start all services with Docker Compose
	@echo "$(COLOR_BLUE)Starting services...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(COLOR_GREEN)✓ Services started$(COLOR_RESET)"
	@$(MAKE) docker-ps

docker-up-logs: ## Start services and show logs
	@echo "$(COLOR_BLUE)Starting services with logs...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) up

docker-down: ## Stop all services
	@echo "$(COLOR_BLUE)Stopping services...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) down
	@echo "$(COLOR_GREEN)✓ Services stopped$(COLOR_RESET)"

docker-down-volumes: ## Stop services and remove volumes (clean slate)
	@echo "$(COLOR_YELLOW)⚠ This will delete all data in volumes!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Stopping services and removing volumes...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(COLOR_GREEN)✓ Services stopped and volumes removed$(COLOR_RESET)"

docker-restart: ## Restart all services
	@echo "$(COLOR_BLUE)Restarting services...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) restart
	@echo "$(COLOR_GREEN)✓ Services restarted$(COLOR_RESET)"

docker-ps: ## Show running containers
	@echo "$(COLOR_BLUE)Running containers:$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) ps

docker-logs: ## Show logs from all services
	$(DOCKER_COMPOSE) logs -f

docker-logs-orchestrator: ## Show orchestrator logs
	$(DOCKER_COMPOSE) logs -f orchestrator

docker-logs-worker: ## Show worker logs
	$(DOCKER_COMPOSE) logs -f worker

docker-test: ## Run tests in Docker
	@echo "$(COLOR_BLUE)Running tests in Docker...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) --profile test up test
	@echo "$(COLOR_GREEN)✓ Tests completed$(COLOR_RESET)"

docker-shell: ## Open shell in orchestrator container
	$(DOCKER_COMPOSE) exec orchestrator /bin/bash

docker-shell-redis: ## Open Redis CLI
	$(DOCKER_COMPOSE) exec redis redis-cli

docker-shell-postgres: ## Open PostgreSQL shell
	$(DOCKER_COMPOSE) exec postgres psql -U chimera -d chimera

docker-scale-workers: ## Scale workers (usage: make docker-scale-workers N=5)
	@echo "$(COLOR_BLUE)Scaling workers to $(N)...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) up --scale worker=$(N) -d
	@echo "$(COLOR_GREEN)✓ Workers scaled to $(N)$(COLOR_RESET)"

# ============================================================================
# Database Commands
# ============================================================================

db-migrate: ## Run database migrations (if implemented)
	@echo "$(COLOR_BLUE)Running database migrations...$(COLOR_RESET)"
	$(PYTHON) -m src.database.migrate
	@echo "$(COLOR_GREEN)✓ Migrations complete$(COLOR_RESET)"

db-seed: ## Seed database with test data
	@echo "$(COLOR_BLUE)Seeding database...$(COLOR_RESET)"
	$(PYTHON) -m src.database.seed
	@echo "$(COLOR_GREEN)✓ Database seeded$(COLOR_RESET)"

db-reset: ## Reset database (drop all tables and recreate)
	@echo "$(COLOR_YELLOW)⚠ This will delete all data!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Resetting database...$(COLOR_RESET)"
	$(DOCKER_COMPOSE) exec postgres psql -U chimera -d chimera -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@$(MAKE) db-migrate
	@echo "$(COLOR_GREEN)✓ Database reset$(COLOR_RESET)"

# ============================================================================
# Spec Checking (Custom for Chimera)
# ============================================================================

spec-check: ## Verify code aligns with specifications
	@echo "$(COLOR_BLUE)Checking spec alignment...$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)⚠ This is a placeholder - implement custom spec checker$(COLOR_RESET)"
	@# TODO: Implement script that checks if:
	@#   - All FR-* user stories have corresponding tests
	@#   - All tests reference their spec requirements
	@#   - Code implements the schemas defined in technical.md
	@echo "$(COLOR_GREEN)✓ Spec check complete$(COLOR_RESET)"

spec-list: ## List all functional requirements from specs
	@echo "$(COLOR_BOLD)Functional Requirements:$(COLOR_RESET)"
	@grep -rh "^### FR-" specs/functional.md | sed 's/### /  /' || echo "  No FR-* requirements found"

# ============================================================================
# Skills Management
# ============================================================================

skills-validate: ## Validate all skill.yaml files
	@echo "$(COLOR_BLUE)Validating skill manifests...$(COLOR_RESET)"
	@$(PYTHON) -m src.orchestrator.validate_skills
	@echo "$(COLOR_GREEN)✓ All skills validated$(COLOR_RESET)"

skills-list: ## List all available skills
	@echo "$(COLOR_BOLD)Available Skills:$(COLOR_RESET)"
	@find skills/ -name "skill.yaml" -exec echo "  - {}" \;

# ============================================================================
# Cleanup
# ============================================================================

clean: ## Remove Python cache files
	@echo "$(COLOR_BLUE)Cleaning Python cache...$(COLOR_RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(COLOR_GREEN)✓ Cache cleaned$(COLOR_RESET)"

clean-test: ## Remove test artifacts
	@echo "$(COLOR_BLUE)Cleaning test artifacts...$(COLOR_RESET)"
	rm -rf .pytest_cache htmlcov .coverage
	@echo "$(COLOR_GREEN)✓ Test artifacts cleaned$(COLOR_RESET)"

clean-all: clean clean-test docker-down-volumes ## Remove all generated files and Docker volumes
	@echo "$(COLOR_GREEN)✓ All cleaned$(COLOR_RESET)"

# ============================================================================
# Git Helpers
# ============================================================================

git-status: ## Show git status
	@git status

git-commit-specs: ## Commit specs changes with standard message
	@git add specs/
	@git commit -m "docs(specs): update specifications"
	@echo "$(COLOR_GREEN)✓ Specs committed$(COLOR_RESET)"

git-commit-tests: ## Commit test changes with standard message
	@git add tests/
	@git commit -m "test: add/update test suite"
	@echo "$(COLOR_GREEN)✓ Tests committed$(COLOR_RESET)"

# ============================================================================
# Project Info
# ============================================================================

info: ## Show project information
	@echo "$(COLOR_BOLD)Project Chimera$(COLOR_RESET)"
	@echo "  Version: 0.1.0"
	@echo "  Python: $$($(PYTHON) --version)"
	@echo "  Docker: $$($(DOCKER) --version)"
	@echo "  UV: $$($(UV) --version 2>/dev/null || echo 'Not installed')"
	@echo ""
	@echo "$(COLOR_BOLD)Directory Structure:$(COLOR_RESET)"
	@echo "  specs/          - Specifications"
	@echo "  src/            - Source code"
	@echo "  tests/          - Test suite"
	@echo "  skills/         - Agent skills"
	@echo "  agents/         - Agent personas"
	@echo ""

verify: ## Verify environment is set up correctly
	@echo "$(COLOR_BLUE)Verifying environment...$(COLOR_RESET)"
	@echo -n "  Python 3.11+: "
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 11), 'Need Python 3.11+'; print('✓')"
	@echo -n "  Docker: "
	@command -v $(DOCKER) >/dev/null 2>&1 && echo "✓" || echo "✗ (not installed)"
	@echo -n "  Docker Compose: "
	@command -v $(DOCKER_COMPOSE) >/dev/null 2>&1 && echo "✓" || echo "✗ (not installed)"
	@echo -n "  uv: "
	@command -v $(UV) >/dev/null 2>&1 && echo "✓" || echo "✗ (not installed - run 'make install-uv')"
	@echo -n "  .env file: "
	@test -f .env && echo "✓" || echo "✗ (run 'make env')"
	@echo -n "  specs/ directory: "
	@test -d specs && echo "✓" || echo "✗"
	@echo -n "  tests/ directory: "
	@test -d tests && echo "✓" || echo "✗"
	@echo "$(COLOR_GREEN)Verification complete$(COLOR_RESET)"

# ============================================================================
# CI/CD Simulation
# ============================================================================

ci: ## Run CI pipeline locally (lint + test)
	@echo "$(COLOR_BOLD)Running CI Pipeline$(COLOR_RESET)"
	@$(MAKE) lint
	@$(MAKE) test-cov
	@echo "$(COLOR_GREEN)✓ CI pipeline passed$(COLOR_RESET)"

ci-docker: ## Run CI pipeline in Docker
	@echo "$(COLOR_BOLD)Running CI Pipeline in Docker$(COLOR_RESET)"
	@$(MAKE) docker-build
	@$(MAKE) docker-test
	@echo "$(COLOR_GREEN)✓ CI pipeline passed$(COLOR_RESET)"

# ============================================================================
# Development Workflow
# ============================================================================

dev-setup: ## Complete development setup (first time)
	@echo "$(COLOR_BOLD)Setting up development environment$(COLOR_RESET)"
	@$(MAKE) install-uv
	@$(MAKE) setup
	@$(MAKE) env
	@$(MAKE) docker-build
	@echo ""
	@echo "$(COLOR_GREEN)✓ Development environment ready!$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)Next steps:$(COLOR_RESET)"
	@echo "  1. Edit .env and add your API keys"
	@echo "  2. Run: make docker-up"
	@echo "  3. Run: make test"
	@echo ""

dev-start: docker-up ## Start development environment

dev-stop: docker-down ## Stop development environment

dev-restart: docker-restart ## Restart development environment

dev-logs: docker-logs ## View development logs

# ============================================================================
# Quick Actions (Most Common Commands)
# ============================================================================

.PHONY: all
all: lint test ## Run linting and tests (quick check)

.PHONY: watch
watch: test-watch ## Watch for file changes and run tests

# ============================================================================
# Notes
# ============================================================================
#
# Makefile Conventions:
#   - Commands are lowercase with hyphens (e.g., docker-up)
#   - All commands have help text (##)
#   - Colors make output readable
#   - .PHONY prevents conflicts with files
#
# Common Workflows:
#   
#   First Time Setup:
#     make dev-setup
#     (edit .env)
#     make docker-up
#     make test
#
#   Daily Development:
#     make dev-start
#     (make code changes)
#     make test
#     make lint
#     make dev-stop
#
#   Before Committing:
#     make ci
#     git add .
#     git commit -m "feat: your change"
#
# ============================================================================
