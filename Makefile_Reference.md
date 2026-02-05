# Makefile Quick Reference

**Complete list of standardized commands for Project Chimera**

---

## 🚀 Quick Start

```bash
# First time setup
make dev-setup         # Install everything
nano .env              # Add your API keys
make docker-up         # Start all services
make test              # Verify it works
```

---

## 📋 All Available Commands

Run `make help` to see this list anytime.

### 🔧 Setup & Installation

| Command | Description |
|---------|-------------|
| `make setup` | Install all dependencies using uv |
| `make setup-pip` | Install dependencies using pip (alternative) |
| `make env` | Copy .env.example to .env |
| `make install-uv` | Install uv package manager |
| `make dev-setup` | Complete first-time development setup |

### 🧪 Testing

| Command | Description |
|---------|-------------|
| `make test` | Run all tests with pytest |
| `make test-unit` | Run only unit tests |
| `make test-integration` | Run only integration tests |
| `make test-cov` | Run tests with coverage report (HTML + terminal) |
| `make test-watch` | Run tests in watch mode (auto-rerun on changes) |

### ✨ Code Quality

| Command | Description |
|---------|-------------|
| `make lint` | Run all linters (black, ruff, mypy) |
| `make lint-black` | Check code formatting with black |
| `make lint-ruff` | Check code with ruff |
| `make lint-mypy` | Run type checking with mypy |
| `make format` | Auto-format code with black |
| `make format-fix` | Auto-fix linting issues with ruff |

### 🐳 Docker Commands

| Command | Description |
|---------|-------------|
| `make docker-build` | Build Docker images |
| `make docker-up` | Start all services in background |
| `make docker-up-logs` | Start services and show logs (foreground) |
| `make docker-down` | Stop all services |
| `make docker-down-volumes` | Stop services and delete volumes (clean slate) |
| `make docker-restart` | Restart all services |
| `make docker-ps` | Show running containers |
| `make docker-logs` | Show logs from all services |
| `make docker-logs-orchestrator` | Show only orchestrator logs |
| `make docker-logs-worker` | Show only worker logs |
| `make docker-test` | Run tests inside Docker container |
| `make docker-shell` | Open bash shell in orchestrator container |
| `make docker-shell-redis` | Open Redis CLI |
| `make docker-shell-postgres` | Open PostgreSQL shell |
| `make docker-scale-workers N=5` | Scale worker replicas (example: N=5) |

### 🗄️ Database Commands

| Command | Description |
|---------|-------------|
| `make db-migrate` | Run database migrations |
| `make db-seed` | Seed database with test data |
| `make db-reset` | ⚠️ Drop and recreate database (deletes all data) |

### 📝 Spec Checking

| Command | Description |
|---------|-------------|
| `make spec-check` | Verify code aligns with specifications |
| `make spec-list` | List all functional requirements (FR-*) |

### 🎯 Skills Management

| Command | Description |
|---------|-------------|
| `make skills-validate` | Validate all skill.yaml files |
| `make skills-list` | List all available skills |

### 🧹 Cleanup

| Command | Description |
|---------|-------------|
| `make clean` | Remove Python cache files |
| `make clean-test` | Remove test artifacts (.pytest_cache, coverage) |
| `make clean-all` | Remove everything (cache + tests + Docker volumes) |

### 📦 Git Helpers

| Command | Description |
|---------|-------------|
| `make git-status` | Show git status |
| `make git-commit-specs` | Commit specs/ with standard message |
| `make git-commit-tests` | Commit tests/ with standard message |

### ℹ️ Project Info

| Command | Description |
|---------|-------------|
| `make info` | Show project information (versions, structure) |
| `make verify` | Verify environment is set up correctly |

### 🔄 CI/CD Simulation

| Command | Description |
|---------|-------------|
| `make ci` | Run CI pipeline locally (lint + test) |
| `make ci-docker` | Run CI pipeline in Docker |

### 💻 Development Workflow

| Command | Description |
|---------|-------------|
| `make dev-start` | Start development environment (alias for docker-up) |
| `make dev-stop` | Stop development environment (alias for docker-down) |
| `make dev-restart` | Restart development environment |
| `make dev-logs` | View development logs |

### ⚡ Quick Actions

| Command | Description |
|---------|-------------|
| `make all` | Run linting and tests (quick pre-commit check) |
| `make watch` | Watch for changes and auto-run tests |

---

## 🎓 Common Workflows

### First Time Setup

```bash
make dev-setup          # Install dependencies, uv, create .env template
nano .env               # Add your API keys (ANTHROPIC_API_KEY, etc.)
make docker-up          # Start Redis, Postgres, Weaviate, Orchestrator, Workers
make test               # Run tests to verify everything works
```

### Daily Development

```bash
make dev-start          # Start all services
# ... make your code changes ...
make test               # Run tests after changes
make lint               # Check code quality
make dev-stop           # Stop services when done
```

### Before Committing

```bash
make ci                 # Run full CI pipeline (lint + test with coverage)
git add .
git commit -m "feat: your feature description"
git push
```

### Debugging

```bash
make docker-logs        # View all service logs
make docker-ps          # Check which services are running
make docker-shell       # Get shell access to orchestrator
make docker-shell-redis # Check Redis data
```

### Scaling Workers

```bash
make docker-scale-workers N=10    # Scale to 10 workers for high load
make docker-ps                    # Verify workers are running
```

---

## 🎯 Most Common Commands

**You'll use these 90% of the time:**

```bash
make help              # When you forget a command
make docker-up         # Start everything
make test              # Run tests
make lint              # Check code quality
make docker-logs       # Debug issues
make docker-down       # Stop everything
```

---

## 💡 Pro Tips

### 1. Check Environment First
```bash
make verify            # Shows what's installed/configured
```

### 2. Watch Tests While Coding
```bash
make watch             # Auto-runs tests on file changes
```

### 3. Run CI Before Push
```bash
make ci                # Ensures your code will pass GitHub Actions
```

### 4. Clean Slate Restart
```bash
make docker-down-volumes   # Remove all data
make docker-up             # Fresh start
```

### 5. View Specific Service Logs
```bash
make docker-logs-orchestrator   # Just orchestrator
make docker-logs-worker         # Just workers
```

---

## 🔧 Troubleshooting

### "Command not found: make"

**Windows:** Install via Chocolatey
```bash
choco install make
```

**Mac:** Install via Homebrew
```bash
brew install make
```

**Linux:** Usually pre-installed, or:
```bash
sudo apt-get install make    # Ubuntu/Debian
sudo yum install make         # CentOS/RHEL
```

### "No rule to make target"

Make sure you're in the project root directory:
```bash
cd /path/to/project-chimera
make help
```

### Services Not Starting

```bash
make verify              # Check what's missing
make docker-down         # Stop any stuck containers
make docker-build        # Rebuild images
make docker-up           # Start fresh
```

---

## 📚 Learning the Makefile

The Makefile is self-documenting. Commands are organized by category and have descriptions.

**Explore commands:**
```bash
make help                # See all commands
cat Makefile            # Read the source
```

**Customize for your workflow:**
- Edit `Makefile` to add your own commands
- Follow the existing pattern: `command: ## Description`
- Commands will automatically appear in `make help`

---

## ✅ Validation Before Submission

Run this checklist before submitting your project:

```bash
make verify            # ✓ Environment configured
make docker-build      # ✓ Docker images build
make docker-up         # ✓ Services start
make docker-ps         # ✓ All services healthy
make test              # ✓ Tests pass
make lint              # ✓ Code quality passes
make ci                # ✓ Full CI pipeline passes
```

If all of the above succeed, you're ready to submit! 🎉

---

**Questions?** Run `make help` or check the Makefile source for details.
