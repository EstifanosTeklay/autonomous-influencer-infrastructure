# Project Chimera: Meta Specification

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Status:** Active Development

---

## 1. Project Vision

### 1.1 Strategic Objective
Project Chimera is the infrastructure and orchestration system for **Autonomous AI Influencers**. We are building the "factory," not the product itself. The end goal is a scalable platform where a single human operator (or small team) can manage a fleet of thousands of virtual influencers that autonomously:

- Research trending topics in their niche
- Generate high-quality multimodal content (text, images, video)
- Engage with audiences across social platforms
- Manage their own finances via crypto wallets
- Operate 24/7 without constant human supervision

### 1.2 The Problem We're Solving
Current AI content systems fail at scale because they:
- Rely on fragile, ad-hoc prompts
- Lack systematic quality control
- Cannot handle financial autonomy
- Break when requirements change
- Require constant human micromanagement

### 1.3 Our Solution
A **spec-driven, swarm-based architecture** where:
- **Intent** is captured in executable specifications (this directory)
- **Infrastructure** (CI/CD, Docker, MCP) ensures reliability
- **Agents** operate in coordinated swarms (Planner-Worker-Judge pattern)
- **Humans** intervene only for high-risk or low-confidence decisions
- **Economics** are handled autonomously via blockchain wallets

---

## 2. Core Architectural Principles

### 2.1 Specification-Driven Development (SDD)
**Rule:** No code is written until the specification exists and is approved.

**Rationale:** AI agents (including our development tools) need precise, unambiguous instructions. Vague specs lead to hallucinations and technical debt.

**Implementation:**
- All features must have corresponding entries in `functional.md` and `technical.md`
- Specs are version-controlled and reviewed before implementation
- Changes to specs trigger test updates first, then code

### 2.2 Swarm Architecture (FastRender Pattern)
**Pattern:** Hierarchical role-based agent coordination

**Three Agent Types:**
1. **Planner** - Strategic decomposition of goals into tasks
2. **Worker** - Stateless, parallel execution of atomic tasks
3. **Judge** - Quality validation and governance

**Benefits:**
- High throughput through parallelization
- Fault isolation (one worker failure doesn't cascade)
- Quality gates at every step
- Clear separation of concerns

### 2.3 Model Context Protocol (MCP) First
**Rule:** All external interactions happen through MCP servers.

**Prohibited:** Direct API calls from agent code to Twitter, Instagram, databases, etc.

**Required:** MCP abstraction layer for:
- **Resources** (data sources agents read)
- **Tools** (functions agents execute)
- **Prompts** (reusable templates)

**Rationale:** When Twitter changes their API, we fix ONE MCP server, not every agent.

### 2.4 Economic Agency
**Capability:** Every agent has a non-custodial crypto wallet (Coinbase AgentKit)

**Enabled Actions:**
- Receive payments (sponsorships, tips, sales)
- Pay for services (compute, external APIs, other agents)
- Manage profit & loss autonomously
- Execute on-chain transactions

**Governance:** "CFO Judge" agent reviews all transactions against budget policies.

### 2.5 Human-in-the-Loop (HITL) Governance
**Dynamic Escalation:** Not all tasks require human review.

**Confidence-Based Routing:**
- **High confidence (>0.90):** Auto-execute
- **Medium confidence (0.70-0.90):** Queue for async human approval
- **Low confidence (<0.70):** Auto-reject and retry with refined prompt

**Mandatory Human Review:**
- Financial transactions above threshold
- Sensitive topics (politics, health, legal advice)
- Brand partnership content
- Security-flagged content

---

## 3. Constraints & Non-Negotiables

### 3.1 Regulatory Compliance
- **Transparency:** Agents must self-disclose as AI when directly asked
- **Platform Labeling:** Use native AI disclosure features (Twitter/Instagram API flags)
- **Data Privacy:** Strict tenant isolation in multi-tenant deployments
- **Content Policy:** Agents must refuse to generate harmful content

### 3.2 Cost Management
**Reality:** AI inference and media generation are expensive.

**Mitigation:**
- **Resource Governor:** Hard budget limits per agent, per campaign, per day
- **Tiered Models:** Use cheap models (Gemini Flash) for routine tasks, expensive models (Opus) only for complex reasoning
- **Media Strategy:** Prefer cheap "living portraits" for daily content, reserve full video generation for hero moments

**Monitoring:** Real-time cost tracking dashboard; alerts when 80% of budget consumed.

### 3.3 Security Boundaries
**Threats:**
- Prompt injection attacks (malicious content in scraped data)
- Agent misbehavior (hallucinated harmful content)
- Financial theft (compromised wallet keys)
- API abuse (rate limit violations)

**Defenses:**
- Input sanitization at perception layer
- Judge validation before ALL external actions
- Encrypted secrets management (AWS Secrets Manager / Vault)
- Rate limiting at MCP layer
- Audit logs for all transactions

### 3.4 Platform Volatility
**Assumption:** Social media APIs (Twitter, Instagram, TikTok) change frequently and unpredictably.

**Design Response:**
- Core agent logic never references platform-specific details
- MCP servers encapsulate all platform quirks
- When platform breaks, only MCP server needs updating

---

## 4. Success Criteria

### 4.1 Velocity Metrics
**Objective:** Maximize autonomous operation time

**Target:** 70% of tasks execute without human intervention
- High-confidence auto-approvals: ≥60%
- Medium-confidence async approvals: ≤30%
- Low-confidence rejections: ≤10%

### 4.2 Quality Metrics
**Objective:** Maintain brand consistency and safety

**Targets:**
- Judge rejection rate: <15% (indicates good Planner/Worker alignment)
- HITL approval rate: >90% (indicates good confidence calibration)
- Zero policy violations in production
- Character consistency score: >0.95 (facial recognition validation)

### 4.3 Economic Metrics
**Objective:** Agents are profitable economic entities

**Targets:**
- Revenue per agent per month: >$500
- Cost per agent per month: <$300
- Profit margin: >40%
- Budget adherence: 100% (no runaway costs)

### 4.4 Scalability Metrics
**Objective:** System supports fleet growth

**Targets:**
- Orchestrator can manage 1,000+ concurrent agents
- Task queue latency: <10 seconds (perception → action)
- Database query time: <100ms (95th percentile)
- Auto-scaling triggers functional

---

## 5. Development Phases

### Phase 1: Foundation (Week 1) ← **WE ARE HERE**
**Deliverables:**
- Complete specifications (this directory)
- Basic swarm architecture (Planner-Worker-Judge skeleton)
- MCP integration (at least 3 servers: Twitter, News, Weaviate)
- Failing tests (TDD approach)
- Docker environment
- CI/CD pipeline

**Success Condition:** Can demonstrate:
1. A Planner creating a task
2. A Worker executing it (mocked)
3. A Judge reviewing it
4. Tests defining expected behavior

### Phase 2: Intelligence (Week 2-3)
**Deliverables:**
- Persona system (SOUL.md parsing + Weaviate memory)
- Semantic filtering on perception inputs
- Multimodal content generation (Ideogram/Runway integration)
- Real social platform posting (via MCP)

**Success Condition:** Agent can autonomously:
1. Detect a trending topic
2. Generate a relevant post
3. Publish to test account
4. Engage with one comment

### Phase 3: Commerce (Week 4)
**Deliverables:**
- Coinbase AgentKit integration
- Wallet management system
- CFO Judge for transaction approval
- Financial dashboard

**Success Condition:** Agent can:
1. Check its wallet balance
2. Receive a test payment
3. Execute a small transfer (with CFO approval)

### Phase 4: Scale (Week 5-6)
**Deliverables:**
- Multi-agent orchestration
- OpenClaw integration (publish agent status to Moltbook)
- Advanced analytics dashboard
- Production hardening

**Success Condition:**
1. Manage 10 agents simultaneously
2. Demonstrate agent-to-agent communication
3. Full observability (logs, metrics, traces)

---

## 6. Technology Stack

### 6.1 Core Runtime
- **Language:** Python 3.11+
- **Package Management:** `uv` (modern, fast alternative to pip)
- **Framework:** `pydantic-ai` for structured LLM interactions

### 6.2 AI Models
- **Reasoning:** Claude Opus 4.5, Gemini 3 Pro (complex planning, judging)
- **Execution:** Gemini 3 Flash, Haiku 3.5 (routine tasks, high volume)
- **Vision:** Gemini Pro Vision (image validation)
- **Image Gen:** Ideogram (character consistency)
- **Video Gen:** Runway Gen-3, Luma (tiered usage)

### 6.3 Data Layer
- **Vector DB:** Weaviate (semantic memory, RAG)
- **Relational:** PostgreSQL (structured data, user accounts)
- **Cache:** Redis (task queues, episodic memory)
- **Ledger:** Base/Ethereum (financial transactions)

### 6.4 Infrastructure
- **Compute:** Kubernetes (AWS EKS / GCP GKE)
- **MCP:** `mcp` Python SDK
- **Wallets:** Coinbase AgentKit (CDP SDK)
- **Secrets:** AWS Secrets Manager / HashiCorp Vault
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana (optional for production)

---

## 7. Terminology & Definitions

### 7.1 Agent Roles
- **Chimera Agent:** A complete autonomous influencer entity (includes Planner, Workers, Judges, and unique persona)
- **Orchestrator:** The central control plane managing the agent fleet
- **Sub-Agent:** Specialized components within a Chimera (e.g., "Engagement Specialist Worker")

### 7.2 MCP Terms
- **MCP Host:** The agent runtime that connects to MCP servers (client side)
- **MCP Server:** External service providing Resources/Tools/Prompts (server side)
- **Resource:** Passive data source (e.g., `news://trends`)
- **Tool:** Executable function (e.g., `post_tweet()`)
- **Prompt:** Reusable template (e.g., `analyze_sentiment`)

### 7.3 Swarm Terms
- **Global State:** Shared context visible to all swarm components (campaigns, budgets, world facts)
- **Task Queue:** Redis queue holding pending work items for Workers
- **Review Queue:** Redis queue holding Worker outputs awaiting Judge validation
- **OCC (Optimistic Concurrency Control):** State validation mechanism preventing race conditions

### 7.4 Financial Terms
- **Agent Wallet:** Non-custodial crypto wallet (Base network) owned by a specific agent
- **CFO Judge:** Specialized Judge agent responsible for financial governance
- **Resource Governor:** Budget enforcement system
- **P&L:** Profit and Loss statement for an individual agent

---

## 8. Out of Scope (For Phase 1)

The following are important but deferred to later phases:

**Not Included in Initial Build:**
- Real video generation (use mocked/static placeholders)
- Full OpenClaw integration (define spec, implement later)
- Multi-tenancy (single-tenant for now)
- Production-grade monitoring (basic logging sufficient)
- Mobile apps (web dashboard only)
- Advanced analytics (basic metrics only)

**Rationale:** Focus on proving the core architecture first. Scale features later.

---

## 9. Versioning & Change Control

### 9.1 Specification Versioning
- Specs use semantic versioning: `MAJOR.MINOR.PATCH`
- Breaking changes (affecting existing code) increment MAJOR
- New features increment MINOR
- Clarifications/fixes increment PATCH

### 9.2 Change Process
1. Propose change in GitHub issue
2. Update spec document
3. Update or create tests to reflect new spec
4. Implement code to pass tests
5. Review and merge

**Never:** Change code first, update spec later.

---

## 10. Contact & Governance

### 10.1 Decision Authority
For Phase 1 (solo development):
- **You** are the sole architect
- Use AI coding assistants (Cursor, Claude Code) as implementation partners
- All major decisions documented in this spec

### 10.2 Escalation Path
When stuck or uncertain:
1. Consult this `_meta.md` for principles
2. Check `technical.md` for implementation details
3. Review `functional.md` for user stories
4. Ask AI assistant for implementation strategy (referencing specs)

### 10.3 AI Assistant Instructions
When working with Cursor/Claude Code:
- ALWAYS reference specs before generating code
- Ask: "Does this align with specs/_meta.md principles?"
- Explain reasoning before writing code
- Flag any spec ambiguities for human resolution
---
**Document Control:**
- **Owner:** Estifanos Teklay
- **Review Cycle:** Daily during Phase 1
- **Next Review:** After functional.md completion
