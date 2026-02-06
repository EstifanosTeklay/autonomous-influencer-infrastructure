# autonomous-influencer-infrastructure

# Project Chimera 🔥

**Autonomous AI Influencer Infrastructure**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![TDD](https://img.shields.io/badge/Development-TDD-orange.svg)]()

> Building the "factory" that produces autonomous AI influencers capable of researching trends, generating content, and managing engagement without human intervention.

---

## 🎯 Overview

Project Chimera is a **spec-driven, swarm-based infrastructure** for building autonomous AI influencers. Unlike fragile prompt-based systems, Chimera provides a robust engineering environment where:

- **Specifications** define the source of truth
- **Tests** are written before implementation (TDD)
- **Infrastructure** ensures reliability and scalability
- **AI agents** coordinate in swarms (Planner-Worker-Judge pattern)

### Key Features

- 🤖 **Swarm Architecture** - Hierarchical agent coordination (Planner → Worker → Judge)
- 📝 **Spec-Driven Development** - All code aligns with formal specifications
- 🧪 **Test-Driven Development** - 60+ tests define expected behavior
- 🐳 **Production-Ready** - Docker, CI/CD, monitoring, security
- 🔌 **MCP Abstraction** - All external interactions through Model Context Protocol
- 💰 **Economic Agency** - Agents manage crypto wallets autonomously
- 🔒 **Governance** - Human-in-the-loop for critical decisions

---

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "External World"
        TW[Twitter/X]
        IG[Instagram]
        NEWS[News APIs]
        BC[Blockchain]
    end
    
    subgraph "MCP Abstraction Layer"
        MCP_TW[Twitter MCP]
        MCP_IG[Instagram MCP]
        MCP_NEWS[News MCP]
        MCP_WV[Weaviate MCP]
        MCP_CB[Coinbase MCP]
    end
    
    subgraph "Agent Swarm"
        PLAN[Planner Agent]
        WORK[Worker Pool]
        JUDGE[Judge Agent]
    end
    
    subgraph "Data Layer"
        REDIS[(Redis Queue)]
        WEAVIATE[(Weaviate Vector DB)]
        PG[(PostgreSQL)]
    end
    
    TW --> MCP_TW
    IG --> MCP_IG
    NEWS --> MCP_NEWS
    BC --> MCP_CB
    
    MCP_TW --> WORK
    MCP_IG --> WORK
    MCP_NEWS --> PLAN
    MCP_WV --> PLAN
    MCP_CB --> WORK
    
    PLAN --> REDIS
    REDIS --> WORK
    WORK --> REDIS
    REDIS --> JUDGE
    
    PLAN --> WEAVIATE
    WORK --> WEAVIATE
    JUDGE --> PG
```

### Swarm Pattern

**Planner Agent:**
- Decomposes high-level goals into atomic tasks
- Monitors queue depth and budgets
- Routes tasks to workers

**Worker Pool:**
- Stateless, parallel execution
- Executes tasks using skills
- Generates result artifacts

**Judge Agent:**
- Validates worker outputs
- Assigns confidence scores
- Routes: auto-approve (>0.90), escalate (0.70-0.90), or reject (<0.70)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- uv package manager (optional but recommended)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/project-chimera.git
cd project-chimera

# 2. Run automated setup
make dev-setup

# 3. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 4. Start all services
make docker-up

# 5. Verify services are running
make docker-ps

# 6. Run tests
make test
```

### Quick Commands

```bash
make help          # Show all available commands
make docker-up     # Start all services
make test          # Run tests
make lint          # Check code quality
make docker-down   # Stop services
```

---

## 📁 Project Structure

```
project-chimera/
├── specs/                      # Source of truth - specifications
│   ├── _meta.md               # Architecture & principles
│   ├── functional.md          # User stories (FR-*)
│   ├── technical.md           # Schemas, APIs, implementation
│   └── openclaw_integration.md # Agent network protocols
├── src/                        # Source code (to be implemented)
├── tests/                      # Test suite (TDD approach)
│   ├── functional/            # Functional requirement tests
│   │   ├── test_planner.py   # FR-SWARM-001
│   │   ├── test_task_schema.py
│   │   ├── test_skills_interface.py
│   │   └── test_trend_fetcher.py
│   ├── integration/           # Integration tests
│   └── mocks/                 # Mock MCP servers
├── skills/                     # Agent capabilities
│   ├── perception/            # Information gathering
│   │   └── trend_detector/
│   ├── generation/            # Content creation
│   │   └── caption_writer/
│   └── engagement/            # Audience interaction
│       └── social_publisher/
├── agents/                     # Agent personas (SOUL.md)
├── research/                   # Research & strategy docs
│   └── tooling_strategy.md
├── .github/                    # CI/CD & templates
│   ├── workflows/
│   │   └── ci.yml             # GitHub Actions
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Service orchestration
├── Makefile                    # Standardized commands
├── pyproject.toml             # Python dependencies
├── CLAUDE.md                   # AI assistant rules
└── README.md                   # This file
```

---

## 🧪 Testing

### Test-Driven Development

This project follows **strict TDD**:
1. ✅ Write failing tests first
2. ✅ Implement code to pass tests
3. ✅ Refactor and improve

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test file
pytest tests/functional/test_planner.py -v

# Watch mode (auto-run on changes)
make watch
```

### Current Test Status

```
Total Tests: 60+
Status: FAILING (expected - TDD approach)

Tests define what needs to be built:
- test_planner.py: FR-SWARM-001 (Task Decomposition)
- test_task_schema.py: AgentTask data model
- test_skills_interface.py: Skill contract compliance
- test_trend_fetcher.py: Trend data structure validation
```

**Note:** Failing tests are **success** in TDD - they define the implementation requirements.

---

## 🐳 Docker

### Services

The Docker Compose stack includes:

| Service | Purpose | Port |
|---------|---------|------|
| **redis** | Task/review queues | 6379 |
| **postgres** | Structured data | 5432 |
| **weaviate** | Semantic memory (vectors) | 8080 |
| **orchestrator** | Control plane | 8000 |
| **worker** | Task execution (3 replicas) | - |
| **test** | Testing environment | - |

### Docker Commands

```bash
# Start services
make docker-up

# View logs
make docker-logs

# Check service health
make docker-ps

# Run tests in Docker
make docker-test

# Scale workers
make docker-scale-workers N=10

# Stop and clean up
make docker-down

# Nuclear option (clean slate)
make docker-down-volumes
```

---

## 📚 Development Workflow

### Daily Development

```bash
# Morning: Start services
make dev-start

# Make changes to code
vim src/swarm/planner.py

# Run tests
make test

# Check code quality
make lint

# Auto-format code
make format

# Before committing
make ci

# Evening: Stop services
make dev-stop
```

### Creating a New Feature

1. **Update Specification**
   ```bash
   vim specs/functional.md
   # Add new FR-* requirement
   ```

2. **Write Failing Test**
   ```bash
   vim tests/functional/test_new_feature.py
   # Test should fail initially
   ```

3. **Implement Feature**
   ```bash
   vim src/component/feature.py
   # Make tests pass
   ```

4. **Verify**
   ```bash
   make test
   make lint
   make ci
   ```

5. **Commit**
   ```bash
   git add .
   git commit -m "feat: implement FR-NEW-001"
   git push
   ```

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql://chimera:password@localhost:5432/chimera

# LLM APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...

# Social Media
TWITTER_API_KEY=...
INSTAGRAM_ACCESS_TOKEN=...

# Blockchain
CDP_API_KEY_NAME=...
CDP_API_KEY_PRIVATE_KEY=...

# Agent Configuration
DEFAULT_DAILY_BUDGET_USD=50.0
AUTO_APPROVE_THRESHOLD=0.90
```

**Important:** Never commit `.env` to Git!

---

## 🛠️ Technology Stack

### Core
- **Python 3.11+** - Modern Python with type hints
- **uv** - Fast package manager
- **pydantic-ai** - Structured LLM interactions
- **MCP SDK** - Model Context Protocol

### Data Layer
- **Redis 7.2** - Task queues, caching
- **Weaviate 1.25** - Vector database, semantic memory
- **PostgreSQL 16** - Structured data, audit logs

### AI & LLMs
- **Anthropic Claude** - Reasoning, planning, judging
- **OpenAI GPT** - Alternative LLM
- **Google Gemini** - High-volume tasks

### Content Generation
- **Ideogram** - Character-consistent images
- **Runway Gen-3** - Video generation
- **Luma AI** - Video generation

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Service orchestration
- **GitHub Actions** - CI/CD
- **CodeRabbit** - AI code review

### Blockchain
- **Coinbase AgentKit** - Wallet management
- **Base Network** - L2 blockchain

---

## 📖 Documentation

### Key Documents

- [Architecture Overview](specs/_meta.md) - Principles and constraints
- [Functional Specs](specs/functional.md) - User stories (FR-*)
- [Technical Specs](specs/technical.md) - API contracts, schemas
- [Tooling Strategy](research/tooling_strategy.md) - MCP servers
- [Skills Architecture](skills/README.md) - Agent capabilities
- [AI Assistant Rules](CLAUDE.md) - Coding conventions

### Specs First!

**The Prime Directive:** Never write code without checking specs first.

All implementation must align with:
1. `specs/_meta.md` - Architectural principles
2. `specs/functional.md` - User stories
3. `specs/technical.md` - Implementation details

---

## 🤝 Contributing

### Development Principles

1. **Spec-Driven Development (SDD)**
   - Update specs before writing code
   - All features must have FR-* requirement
   - Code must reference spec in docstrings

2. **Test-Driven Development (TDD)**
   - Write failing test first
   - Implement to make test pass
   - Refactor with confidence

3. **MCP Abstraction**
   - Never call external APIs directly
   - Always use MCP servers
   - Maintain loose coupling

4. **Type Safety**
   - Type hints on all functions
   - Pydantic models for data
   - mypy strict mode

5. **Security**
   - No hardcoded secrets
   - Environment variables only
   - Audit all transactions

### Pull Request Process

1. Fork the repository
2. Create feature branch (`feat/amazing-feature`)
3. Update specs if needed
4. Write tests (should fail)
5. Implement feature (tests pass)
6. Run `make ci` (must pass)
7. Create Pull Request
8. CodeRabbit AI will review
9. Human approval required
10. Merge to main

### Code Review Checklist

- [ ] Spec reference in PR description
- [ ] Tests added/updated
- [ ] All tests pass (`make test`)
- [ ] Code quality passes (`make lint`)
- [ ] No hardcoded secrets
- [ ] Type hints present
- [ ] Docstrings added
- [ ] MCP abstraction used

---

## 📊 Project Status

### Current Phase: **Foundation (Week 1)**

#### Completed ✅
- [x] Specifications (specs/)
- [x] Test suite (tests/)
- [x] Docker infrastructure
- [x] CI/CD pipeline
- [x] Skills architecture
- [x] AI assistant rules

#### In Progress 🚧
- [ ] Core agent implementation (Planner, Worker, Judge)
- [ ] MCP server integrations
- [ ] Skill implementations

#### Planned 📋
- [ ] Persona system
- [ ] Content generation
- [ ] Social platform posting
- [ ] Wallet management
- [ ] Multi-agent orchestration

## 🎯 Success Metrics

### Velocity Metrics
- Target: 70% autonomous operation
- High-confidence auto-approvals: ≥60%
- Medium-confidence async approvals: ≤30%
- Low-confidence rejections: ≤10%

### Quality Metrics
- Judge rejection rate: <15%
- HITL approval rate: >90%
- Zero policy violations
- Character consistency: >0.95

### Economic Metrics
- Revenue per agent: >$500/month
- Cost per agent: <$300/month
- Profit margin: >40%

---

## 🔒 Security

### Best Practices

- ✅ All secrets in environment variables
- ✅ No API keys in code
- ✅ Encrypted wallet keys (AWS Secrets Manager)
- ✅ Input sanitization at perception layer
- ✅ Judge validation before external actions
- ✅ Rate limiting at MCP layer
- ✅ Audit logs for all transactions
- ✅ Security scanning in CI/CD (Trivy, TruffleHog)

### Threat Model

**Threats:**
- Prompt injection attacks
- Agent misbehavior (hallucinations)
- Financial theft (wallet compromise)
- API abuse (rate limits)

**Mitigations:**
- Input validation
- Judge validation gates
- Encrypted secrets
- Rate limiting
- Comprehensive logging

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - For Claude AI and the vision of helpful, harmless, and honest AI
- **10Academy** - For the Forward Deployed Engineer training program
- **OpenClaw** - For the agent social network concept
- **Coinbase** - For AgentKit enabling economic agency

---

## 📞 Contact & Support
- **Loon Video:**(https://www.loom.com/share/80b1f41054a14d28a2fe90dd46c7797b)
- **Issues:** [GitHub Issues](https://github.com/EstifanosTeklay/project-chimera/issues)
- **Discussions:** [GitHub Discussions](https://github.com/EstifanosTeklay/project-chimera/discussions)
- **Email:** estifanosteklay1@gmail.com

---

## 🚀 Getting Started Checklist

- [ ] Clone repository
- [ ] Install dependencies (`make setup`)
- [ ] Create `.env` from `.env.example`
- [ ] Add API keys to `.env`
- [ ] Start Docker services (`make docker-up`)
- [ ] Run tests (`make test`)
- [ ] Read specifications (`specs/`)
- [ ] Review AI assistant rules (`CLAUDE.md`)
- [ ] Start implementing (follow TDD!)

---

**Built with ❤️ using Spec-Driven Development and Test-Driven Development**

*"In TDD, a failing test is a successful test. It tells you exactly what needs to be built next."*

---

## 🎓 Learning Resources

### Recommended Reading
- [The Trillion Dollar AI Code Stack](https://a16z.com/ai-code-stack/) - a16z
- [OpenClaw: Agent Social Network](https://openclaw.org/)
- [MoltBook: Social Media for Bots](https://moltbook.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [pydantic-ai Documentation](https://ai.pydantic.dev/)

### Key Concepts
- Spec-Driven Development (SDD)
- Test-Driven Development (TDD)
- Swarm Intelligence
- Model Context Protocol (MCP)
- Agentic Workflows
- Economic Agency

---

**Last Updated:** February 5, 2026  
**Version:** 0.1.0  
