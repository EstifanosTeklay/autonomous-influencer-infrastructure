# Architecture Decision Records (ADRs)

This document captures key architectural decisions made during Project Chimera development, following the ADR pattern for transparent decision-making.

---

## ADR Format

Each decision follows this structure:
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: What is the issue we're addressing?
- **Decision**: What is the change we're proposing/making?
- **Consequences**: What becomes easier or more difficult?

---

## ADR-001: Multi-Database Strategy

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

We need to store different types of data with varying access patterns:
- Transactional data (user accounts, campaigns)
- Semantic data (agent memories for RAG)
- High-velocity queues (task distribution)
- Immutable financial records

Single database solutions (e.g., PostgreSQL only) would force suboptimal patterns for some use cases.

### Decision

Adopt a multi-database architecture:
- **PostgreSQL**: Transactional data, ACID compliance
- **Weaviate**: Vector embeddings, semantic search
- **Redis**: Task queues, ephemeral state, caching
- **Blockchain (Base)**: Financial transaction ledger

### Consequences

**Positive**:
- Each database optimized for its use case
- Better performance (vector search in Weaviate >> PostgreSQL with pg_vector)
- Scalability (independent scaling of databases)
- Data integrity (blockchain for immutable financial records)

**Negative**:
- Increased operational complexity
- Need to maintain data consistency across databases
- More infrastructure to manage
- Higher learning curve for developers

**Mitigations**:
- Use Docker Compose for local development (single command setup)
- Implement saga pattern for cross-database transactions
- Clear documentation on which data goes where

---

## ADR-002: FastRender Swarm Pattern

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

AI agents need to coordinate complex, multi-step tasks while maintaining:
- High throughput (many tasks in parallel)
- Quality control (validation before actions)
- Error recovery (isolated failures)

Traditional sequential agent architectures create bottlenecks.

### Decision

Implement the **FastRender Swarm pattern** with three specialized roles:
1. **Planner**: Decomposes goals into atomic tasks
2. **Worker**: Executes tasks in parallel (stateless)
3. **Judge**: Validates outputs before commitment

Tasks flow through Redis queues: `tasks` → Worker → `review` → Judge

### Consequences

**Positive**:
- High parallelism: 50+ workers can execute simultaneously
- Fault isolation: One worker failure doesn't affect others
- Quality gates: Every output validated before execution
- Clear separation of concerns

**Negative**:
- More complex than single-agent approach
- Requires queue infrastructure (Redis)
- Debugging distributed systems is harder

**Evidence**:
- Inspired by Cursor's "FastRender" browser project
- Proven pattern for high-throughput AI coordination

---

## ADR-003: Model Context Protocol (MCP) for All External Integrations

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

Agents need to interact with many external services:
- Social media platforms (Twitter, Instagram, TikTok)
- News APIs
- Image generation (Ideogram, Runway)
- Databases (Weaviate)
- Blockchain (Coinbase AgentKit)

Direct API integration in agent code creates tight coupling and fragility.

### Decision

**All external interactions go through MCP servers.** No direct API calls in agent code.

Agents call MCP tools/resources:
```python
# ❌ Bad
import tweepy
client.create_tweet(text="Hello")

# ✅ Good
await mcp_client.call_tool("twitter_post_tweet", text="Hello")
```

### Consequences

**Positive**:
- Abstraction layer: When Twitter API changes, fix ONE MCP server
- Standardization: Same pattern for all integrations
- Testability: Easy to mock MCP servers
- Reusability: MCP servers can be shared across projects

**Negative**:
- Extra layer of indirection
- Need to build/configure MCP servers
- Slight performance overhead

**Why This Matters**:
- Social platform APIs change frequently
- Reduces agent code complexity
- Follows industry best practice (MCP is Anthropic's standard)

---

## ADR-004: Spec-Driven Development (SDD)

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

AI coding assistants (GitHub Copilot, Claude Code) can hallucinate or misinterpret vague requirements, leading to:
- Code that doesn't match intent
- Inconsistent implementations
- Technical debt

### Decision

**No code is written until the specification exists.**

Workflow:
1. Write spec in `specs/` directory
2. Review and approve spec
3. Write failing tests based on spec (TDD)
4. Implement to make tests pass
5. Code references spec in comments

### Consequences

**Positive**:
- AI agents have clear, unambiguous instructions
- Specifications serve as documentation
- Reduced hallucination and misalignment
- Easier to onboard new developers/agents

**Negative**:
- Slower initial progress (spec-writing upfront)
- Requires discipline to maintain specs
- Can feel bureaucratic for small changes

**Evidence**:
- Recommended in challenge requirements
- Proven pattern for AI-assisted development
- Matches industry trend (GitHub Spec Kit pattern)

---

## ADR-005: Test-Driven Development (TDD)

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

How do we ensure AI-generated code is correct?
How do we prevent regressions?
How do we define "done"?

### Decision

Follow strict TDD:
1. Read spec
2. Write failing test
3. Run test (verify it fails - RED)
4. Write minimal code to pass
5. Run test (verify it passes - GREEN)
6. Refactor if needed
7. Commit

Tests define the "empty slots" that AI agents must fill.

### Consequences

**Positive**:
- Tests ARE the specification (executable)
- Confidence in refactoring
- Prevents regressions
- Clear definition of "done"

**Negative**:
- Slower initial development
- Requires test-writing discipline
- Can be tedious for simple code

**Metrics**:
- Target: >80% code coverage
- All critical paths must have tests

---

## ADR-006: Confidence-Based Human-in-the-Loop (HITL)

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

Agents will make mistakes. Pure automation is risky (harmful content, financial errors).
But pure manual review is slow and defeats the purpose of automation.

### Decision

Dynamic confidence-based routing:
- **High confidence (>0.90)**: Auto-approve
- **Medium confidence (0.70-0.90)**: Human review
- **Low confidence (<0.70)**: Auto-reject, retry
- **Sensitive topics**: Always human review (regardless of confidence)

### Consequences

**Positive**:
- 70% of tasks auto-execute (high velocity)
- 25% reviewed asynchronously (safety)
- 5% auto-rejected (avoid bad outputs)
- Humans focus on edge cases

**Negative**:
- Requires calibration of confidence thresholds
- Risk of miscalibration (false positives/negatives)
- Humans can become bottleneck if too many escalations

**Monitoring**:
- Track HITL approval rate (should be >90%)
- Adjust thresholds based on data

---

## ADR-007: Phase 1 OpenClaw Integration is Read-Only

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

OpenClaw (agent social network) offers opportunities:
- Learn from other agents' discoveries
- Share successful strategies
- Collaborate with specialist agents

But also risks:
- Malicious skills (code injection)
- Prompt injection attacks
- Reputation damage from bad posts

### Decision

**Phase 1**: Read-only monitoring
- Monitor Moltbook for valuable skills/strategies
- Do NOT post yet
- Validate all external skills in sandbox

**Phase 2** (future): Active participation
- Announce agent capabilities
- Share successful strategies
- Limited posting

**Phase 3** (future): Economic collaboration
- Agent-to-agent hiring
- Paid collaborations

### Consequences

**Positive**:
- Low-risk learning period
- Time to build security filters
- Prove value before investing heavily

**Negative**:
- Can't contribute back to community immediately
- Miss early network effects

**Security First**:
- All external content sanitized
- Skills validated before adoption
- Human approval for Phase 2 transition

---

## ADR-008: Non-Custodial Wallets via Coinbase AgentKit

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

Agents need financial autonomy:
- Receive payments (sponsorships, tips)
- Pay for services (external APIs, other agents)
- Manage budgets

Options:
1. Custodial (we hold keys): Centralized risk
2. Non-custodial (agents hold keys): True autonomy

### Decision

Use **Coinbase AgentKit** for non-custodial wallets:
- Each agent gets unique wallet
- Private keys encrypted in secrets manager
- "CFO Judge" reviews all transactions

### Consequences

**Positive**:
- True financial autonomy
- On-chain transparency (audit trail)
- Agents are economic actors
- Decentralized (no single point of failure)

**Negative**:
- Key management complexity
- Blockchain gas fees
- Irreversible transactions

**Security**:
- Keys in AWS Secrets Manager / Vault
- Budget limits enforced
- CFO Judge for governance

---

## ADR-009: PostgreSQL Over MongoDB for Transactional Data

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

Need to store structured data: users, agents, campaigns, content.

Options:
- **PostgreSQL**: Relational, ACID, strong consistency
- **MongoDB**: Document-based, flexible schema, eventual consistency

### Decision

Use **PostgreSQL** for transactional data.

### Reasoning

**Why PostgreSQL**:
- ACID transactions (critical for financial data)
- Strong typing (catches errors early)
- Mature ecosystem (migrations, ORMs, tools)
- JSON support (JSONB for flexible fields)
- Powerful queries (joins, aggregations)

**Why NOT MongoDB**:
- Our data is relational (users → agents → campaigns)
- Need transactions (updating agent + campaign atomically)
- Strong consistency required (financial accuracy)

### Consequences

**Positive**:
- Data integrity guaranteed
- Complex queries easy (SQL)
- Industry-standard patterns

**Negative**:
- Schema migrations required
- Less flexible than schemaless

**Hybrid Approach**:
- Use JSONB columns for truly dynamic data (engagement metrics)
- Best of both worlds

---

## ADR-010: Weaviate Over Pinecone for Vector Database

**Date**: 2026-02-05  
**Status**: Accepted  
**Decision Makers**: Project Lead  

### Context

Need vector database for semantic memory (RAG).

Options:
- **Weaviate**: Open-source, self-hostable, full-featured
- **Pinecone**: Managed service, simpler setup
- **PostgreSQL + pgvector**: All-in-one solution

### Decision

Use **Weaviate**.

### Reasoning

**Why Weaviate**:
- Open-source (no vendor lock-in)
- Self-hostable (cost control, data privacy)
- Rich querying (hybrid search, filters)
- Good Python SDK
- Built-in vectorizers (OpenAI integration)

**Why NOT Pinecone**:
- Vendor lock-in
- Cost scales with usage
- Less control over infrastructure

**Why NOT pgvector**:
- Performance at scale is worse
- Less optimized for vector search

### Consequences

**Positive**:
- Full control over data
- Better performance for semantic search
- No ongoing SaaS costs

**Negative**:
- Need to host/manage Weaviate
- More complex setup than managed service

**Deployment**:
- Docker Compose for local dev
- Kubernetes for production

---

## Summary of Decisions

| ADR | Decision | Status | Impact |
|-----|----------|--------|--------|
| 001 | Multi-Database Strategy | Accepted | High |
| 002 | FastRender Swarm Pattern | Accepted | Critical |
| 003 | MCP for All Integrations | Accepted | Critical |
| 004 | Spec-Driven Development | Accepted | High |
| 005 | Test-Driven Development | Accepted | High |
| 006 | Confidence-Based HITL | Accepted | Critical |
| 007 | Read-Only OpenClaw (Phase 1) | Accepted | Medium |
| 008 | Non-Custodial Wallets | Accepted | High |
| 009 | PostgreSQL vs MongoDB | Accepted | Medium |
| 010 | Weaviate vs Pinecone | Accepted | Medium |
| 011 | React + TypeScript + Tailwind | Accepted | High |
| 012 | Agent State Machine | Accepted | High |
| 013 | MCP Sense Logs as Artifact | Accepted | Critical |
| 014 | Agent Learning via Memory | Proposed | Medium |

---

## ADR-011: React + TypeScript + Tailwind for Dashboard Frontend

**Date**: 2026-02-06  
**Status**: Accepted  

### Context
Network Operators monitor agents, campaigns, and HITL queue via dashboard. Need performant, type-safe frontend.

### Decision
Use **React 18+ with TypeScript and Tailwind CSS**.
- **Vite** for build (5x faster than webpack)
- **TanStack Query** for server state
- **Zustand** for dashboard state
- **React Hook Form + Zod** for forms

### Consequences
**Positive**: Rapid development, type safety, mature ecosystem, component reusability  
**Negative**: Larger bundle size, Node.js dependency

---

## ADR-012: Agent Lifecycle as State Machine for Observability

**Date**: 2026-02-06  
**Status**: Accepted  

### Context
Current: tasks have status (pending, in_progress, complete). Missing: agent-level lifecycle visibility for debugging and auditing.

### Decision
Define strict **Agent State Machine** with logged transitions:
```
CREATED → INITIALIZING → ACTIVE → QUIET → PAUSED → ARCHIVED
                          ↓       ↓      ↑
                      LEARNING ←────────┘
```

Each transition logged with timestamp, trigger reason, and metrics snapshot (tasks completed, avg confidence, cost efficiency, error patterns).

### Consequences
**Positive**: Complete audit trail, easier debugging, enables alerting, supports "agent rewind"  
**Negative**: Increased logging/storage overhead

---

## ADR-013: MCP Sense Logs as First-Class Artifact

**Date**: 2026-02-06  
**Status**: Accepted  

### Context
How do we capture agent decision-making? How do we demonstrate transparency to auditors? Current MCP_INTERACTION_LOG.md is subjective and not machine-parseable.

### Decision
Implement **MCP Sense Protocol** with structured JSON logging:
- Every MCP tool call logged with params/result
- Agent decision traces logged
- Logs are machine-parseable and queryable
- Enables "agent replay" (exact reproduction)

Storage tiers:
- **Short-term**: Redis (7 days, query index)
- **Long-term**: PostgreSQL (queryable archive)
- **Public**: MCP_SENSE_LOG.md (human-readable digest)

Structure:
```json
{
  "session_id": "uuid",
  "agent_id": "chimera_fashion_eth_001",
  "timestamp": "2026-02-06T15:30:00Z",
  "event": "mcp_tool_call",
  "tool": "trend_detector",
  "params": {"query": "sustainable fashion", "window": 7},
  "result": {...},
  "duration_ms": 234,
  "confidence": 0.87
}
```

### Consequences
**Positive**: Full transparency, reproducible traces, auditable, regulatory compliant  
**Negative**: Privacy concerns (need redaction), storage overhead, query API complexity

---

## ADR-014: Agent Learning Via Memory Consolidation

**Date**: 2026-02-06  
**Status**: Proposed  

### Context
Agents execute thousands of tasks. Without learning mechanisms, they repeat mistakes and miss strategic improvement. How can agents improve long-term?

### Decision
**Memory Consolidation Pattern** (leverages existing Weaviate infrastructure):

**Phase 1 - Active**: Worker stores memories as it executes
- Successful post → tagged "successful_post" with engagement score
- Failed post → tagged "failed_post" with failure analysis
- New pattern discovered → tagged "learned_pattern"

**Phase 2 - Consolidation**: Judge review triggers learning signal
- High-confidence successful posts → memory.importance_score += 0.1
- Rejected posts → memory.importance_score -= 0.1
- Similar patterns → merge/deduplicate

**Phase 3 - Retrieval**: Planning leverages learned memories
- Planner queries: "posts about coffee that performed well?"
- Weaviate returns top memories via semantic search
- Planner includes in task context → Worker has examples

Result: Agent naturally improves because it remembers what worked.

### Example Workflow
```
Day 1: Post about Ethiopian coffee → 500 likes (success)
       Memory stored: "Coffee posts with cultural story → high engagement"

Day 15: Planner planning new coffee post
        Queries: "What do I know about coffee posts?"
        Retrieves: Day 1 memory (high importance)
        Includes in context: "Remember: storytelling approach works"
        
Worker generates new post using learned strategy
Result: 600 likes (improvement)
```

### Consequences
**Positive**: 
- Agents continuously improve without fine-tuning
- Transparent (humans can read memories)
- Leverages existing infrastructure
- Cross-platform consistency (shared memories)

**Negative**: 
- Memories can become stale (outdated strategies)
- Requires careful memory curation/cleanup
- Risk of amplifying errors (if bad memory has high importance)

**Experiments**:
- A/B test: agent with memory vs. agent without
- Measure: engagement metrics, task success rate, cost efficiency
- Hypothesis: Agent with memory should show 15%+ improvement in engagement by week 4

---

## Decision-Making Process

**How decisions are made**:

1. Identify architectural question
2. Research options (read docs, test prototypes)
3. Document tradeoffs in ADR format
4. Review with team (or self-review for solo)
5. Accept or reject
6. Implement according to decision

**When to create an ADR**:
- Any decision that affects multiple components
- Technology choices (databases, frameworks)
- Architectural patterns
- Security/compliance decisions
- Anything that future developers will ask "why did they do it this way?"

**Living Document**:
- ADRs can be deprecated or superseded
- Never delete ADRs (historical context matters)
- Reference ADRs in code comments

---

**Last Updated**: February 6, 2026  
**Total ADRs**: 14 (13 Accepted, 1 Proposed)  
**Next Review**: After Phase 1 implementation complete
