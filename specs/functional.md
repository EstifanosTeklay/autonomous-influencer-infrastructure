# Project Chimera: Functional Specification

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Parent Document:** `_meta.md`

---

## 1. Introduction

This document defines the functional requirements of Project Chimera from the perspective of its key users:
- **Chimera Agents** (the autonomous influencers themselves)
- **Network Operators** (humans managing agent fleets)
- **Human Reviewers** (HITL moderators)
- **System Developers** (engineers extending the platform)

Each requirement is expressed as a **User Story** in the format:
> "As a [USER TYPE], I need to [ACTION], so that [BENEFIT]."

---

## 2. Core User Personas

### 2.1 Chimera Agent
**Description:** An autonomous AI influencer with a unique persona, financial wallet, and content niche.

**Goals:**
- Generate engaging content that grows audience
- Maintain consistent brand voice and visual identity
- Operate within budget constraints
- Learn from past successes and failures
- Interact authentically with audience

### 2.2 Network Operator
**Description:** Human strategist managing a fleet of Chimera agents.

**Goals:**
- Set high-level campaign objectives
- Monitor fleet health and performance
- Review escalated content before publication
- Ensure ROI and budget compliance
- Scale operations without linear time investment

### 2.3 Human Reviewer (HITL Moderator)
**Description:** Human specialist reviewing agent-generated content flagged as risky or low-confidence.

**Goals:**
- Quickly approve/reject content
- Maintain brand safety
- Provide feedback to improve agent performance
- Focus only on edge cases (not routine content)

### 2.4 System Developer
**Description:** Engineer extending platform capabilities.

**Goals:**
- Add new social platform integrations (new MCP servers)
- Deploy new content generation tools
- Refine agent personas and prompts
- Monitor system health
- Debug issues

---

## 3. Functional Requirements: Chimera Agent Capabilities

### FR-AGENT-001: Autonomous Trend Detection
**User Story:**
> As a Chimera Agent, I need to continuously monitor news sources and social media for trending topics relevant to my niche, so that I can create timely, relevant content.

**Acceptance Criteria:**
- [ ] Agent polls configured MCP Resources (e.g., `news://fashion/ethiopia`) every 15 minutes
- [ ] Incoming content is semantically filtered against agent's niche keywords
- [ ] Only content with relevance score >0.75 triggers content creation task
- [ ] Agent maintains a rolling 7-day trend history in Weaviate

**Priority:** HIGH  
**Dependencies:** MCP news server, Weaviate integration

---

### FR-AGENT-002: Persona-Consistent Content Generation
**User Story:**
> As a Chimera Agent, I need to generate text, images, and videos that match my unique persona and visual identity, so that my audience recognizes me across all content.

**Acceptance Criteria:**
- [ ] Agent loads persona from `SOUL.md` file at startup
- [ ] All text generation includes persona context in system prompt
- [ ] All image generation requests include character_reference_id
- [ ] Generated images pass facial similarity check >0.95 before publishing
- [ ] Text tone matches defined voice attributes (e.g., "witty," "empathetic")

**Priority:** HIGH  
**Dependencies:** SOUL.md parser, Ideogram MCP, vision validation model

---

### FR-AGENT-003: Multi-Platform Publishing
**User Story:**
> As a Chimera Agent, I need to publish content to multiple social platforms (Twitter, Instagram, TikTok), so that I can maximize reach.

**Acceptance Criteria:**
- [ ] Agent uses platform-agnostic MCP tool calls (e.g., `social.post()`)
- [ ] Single content piece can be reformatted for each platform's requirements
- [ ] Captions adjusted for character limits (Twitter: 280, Instagram: 2200)
- [ ] Media formats converted as needed (aspect ratios, file sizes)
- [ ] Platform-native AI disclosure flags set when available

**Priority:** HIGH  
**Dependencies:** MCP servers for Twitter, Instagram, TikTok

---

### FR-AGENT-004: Audience Engagement
**User Story:**
> As a Chimera Agent, I need to respond to comments and messages from my audience in a timely and authentic manner, so that I build relationships.

**Acceptance Criteria:**
- [ ] Agent ingests mentions/comments via MCP Resources every 5 minutes
- [ ] Each engagement is semantically analyzed for:
  - Sentiment (positive/negative/neutral)
  - Topic (question/praise/complaint)
  - Urgency (immediate/routine)
- [ ] Responses generated within agent persona constraints
- [ ] Spam/abusive content automatically filtered (no response generated)
- [ ] High-value engagements (influencer mentions) escalated to human review

**Priority:** MEDIUM  
**Dependencies:** Sentiment analysis model, engagement MCP resources

---

### FR-AGENT-005: Financial Autonomy
**User Story:**
> As a Chimera Agent, I need to manage my own crypto wallet, receive payments, and pay for services, so that I can operate as an economic entity.

**Acceptance Criteria:**
- [ ] Agent is assigned unique non-custodial wallet at creation
- [ ] Agent can check wallet balance via `get_balance()` tool
- [ ] Agent can receive payments (USDC, ETH) without human intervention
- [ ] Agent can initiate transfers via `native_transfer()` tool
- [ ] All outgoing transactions require CFO Judge approval
- [ ] Wallet private key never logged or exposed in code

**Priority:** MEDIUM  
**Dependencies:** Coinbase AgentKit, CFO Judge implementation

---

### FR-AGENT-006: Self-Improvement Through Memory
**User Story:**
> As a Chimera Agent, I need to remember past interactions and successful strategies, so that I continuously improve my performance.

**Acceptance Criteria:**
- [ ] Successful high-engagement posts automatically stored in Weaviate
- [ ] Agent retrieves relevant memories before generating similar content
- [ ] Failed content (Judge-rejected) tagged with failure reasons
- [ ] Agent can query memory: "What worked when discussing topic X?"
- [ ] Memory persists across restarts

**Priority:** MEDIUM  
**Dependencies:** Weaviate integration, Judge feedback loop

---

### FR-AGENT-007: Budget Awareness
**User Story:**
> As a Chimera Agent, I need to be aware of my operational costs and budget limits, so that I don't exceed allocated resources.

**Acceptance Criteria:**
- [ ] Agent checks daily budget before initiating expensive operations (video gen)
- [ ] If budget <20% remaining, agent switches to "economy mode" (cheaper models, no video)
- [ ] If budget exhausted, agent pauses non-critical tasks until reset
- [ ] Budget consumption logged to dashboard in real-time

**Priority:** HIGH  
**Dependencies:** Resource Governor implementation

---

## 4. Functional Requirements: Network Operator Capabilities

### FR-OPERATOR-001: Campaign Creation
**User Story:**
> As a Network Operator, I need to define high-level campaign goals in natural language, so that agents know what to achieve without micromanaging.

**Acceptance Criteria:**
- [ ] Operator enters campaign goal (e.g., "Promote summer fashion line to Gen-Z in Ethiopia")
- [ ] System decomposes goal into sub-tasks visible as a tree structure
- [ ] Operator can approve, edit, or reject the task breakdown
- [ ] Approved campaign triggers Planner agents to execute

**Priority:** HIGH  
**Dependencies:** Campaign dashboard UI, Planner decomposition logic

---

### FR-OPERATOR-002: Fleet Monitoring
**User Story:**
> As a Network Operator, I need real-time visibility into all active agents, so that I can identify issues quickly.

**Acceptance Criteria:**
- [ ] Dashboard shows all agents with status indicators:
  - 🟢 Active (currently executing tasks)
  - 🟡 Idle (waiting for work)
  - 🔴 Error (requires attention)
  - ⏸️ Paused (budget exhausted or manual pause)
- [ ] Each agent shows:
  - Current task description
  - Wallet balance
  - Tasks in queue
  - Last activity timestamp
- [ ] Operator can click agent to view detailed logs

**Priority:** HIGH  
**Dependencies:** Orchestrator dashboard, agent status reporting

---

### FR-OPERATOR-003: Financial Oversight
**User Story:**
> As a Network Operator, I need to see consolidated financial data for all agents, so that I can track ROI and profitability.

**Acceptance Criteria:**
- [ ] Dashboard displays:
  - Total revenue (all agents combined)
  - Total costs (AI inference + media generation)
  - Profit/loss per agent
  - Budget utilization (% of allocated budget spent)
- [ ] Data filterable by time range (day/week/month)
- [ ] Alerts when any agent exceeds 90% of budget

**Priority:** MEDIUM  
**Dependencies:** Financial tracking system, blockchain transaction aggregation

---

### FR-OPERATOR-004: Emergency Controls
**User Story:**
> As a Network Operator, I need emergency "kill switches" to immediately stop agents if something goes wrong, so that I can prevent damage.

**Acceptance Criteria:**
- [ ] "Pause Agent" button stops all new task generation
- [ ] "Pause Fleet" button pauses entire network
- [ ] Active tasks complete, but no new tasks created
- [ ] Resume functionality restores operation
- [ ] All pause/resume actions logged with timestamp and reason

**Priority:** HIGH  
**Dependencies:** Orchestrator control API

---

## 5. Functional Requirements: Human Reviewer (HITL) Capabilities

### FR-REVIEWER-001: Efficient Content Review Queue
**User Story:**
> As a Human Reviewer, I need a streamlined interface to quickly review flagged content, so that I don't become a bottleneck.

**Acceptance Criteria:**
- [ ] Review queue shows content sorted by priority:
  1. Financial transactions (highest priority)
  2. Sensitive topics (politics, health, legal)
  3. Medium-confidence content (0.7-0.9 score)
- [ ] Each item displays:
  - Generated content (text/image preview)
  - Confidence score (color-coded)
  - Agent reasoning trace
  - Campaign context
- [ ] Reviewer can Approve, Reject, or Edit in <10 seconds per item
- [ ] Keyboard shortcuts (A=Approve, R=Reject, E=Edit)

**Priority:** HIGH  
**Dependencies:** Review queue UI, Judge escalation logic

---

### FR-REVIEWER-002: Feedback Loop to Improve Agents
**User Story:**
> As a Human Reviewer, I need to provide feedback when rejecting content, so that agents learn from mistakes.

**Acceptance Criteria:**
- [ ] Reject action requires selecting reason:
  - Off-brand tone
  - Factual error
  - Inappropriate content
  - Other (free text)
- [ ] Feedback stored in Weaviate as negative example
- [ ] Agent retrieves rejections when generating similar future content
- [ ] Dashboard shows rejection trends by reason (analytics)

**Priority:** MEDIUM  
**Dependencies:** Feedback storage system, agent learning loop

---

## 6. Functional Requirements: System Developer Capabilities

### FR-DEV-001: MCP Server Deployment
**User Story:**
> As a System Developer, I need to easily add new MCP servers to extend agent capabilities, so that the platform can integrate with new services.

**Acceptance Criteria:**
- [ ] Developer writes MCP server following standard protocol
- [ ] Server added to orchestrator config file (declarative)
- [ ] Orchestrator auto-discovers new tools/resources on restart
- [ ] Agent prompts automatically include new capabilities
- [ ] No code changes required in core agent logic

**Priority:** HIGH  
**Dependencies:** MCP discovery mechanism, config management

---

### FR-DEV-002: Persona Management
**User Story:**
> As a System Developer, I need to create and update agent personas via version-controlled files, so that persona changes are auditable.

**Acceptance Criteria:**
- [ ] Persona defined in `agents/{agent_id}/SOUL.md` file
- [ ] File uses YAML frontmatter + Markdown body
- [ ] Changes tracked in Git with commit messages
- [ ] Agent automatically reloads persona on file change (hot reload)
- [ ] Invalid SOUL.md fails validation with clear error messages

**Priority:** HIGH  
**Dependencies:** SOUL.md parser, file watcher

---

### FR-DEV-003: Testing Infrastructure
**User Story:**
> As a System Developer, I need comprehensive test coverage, so that I can refactor code confidently.

**Acceptance Criteria:**
- [ ] Unit tests for all core modules (>80% coverage)
- [ ] Integration tests for swarm coordination (Planner→Worker→Judge)
- [ ] Mock MCP servers for testing without external APIs
- [ ] Tests run in Docker container (reproducible environment)
- [ ] CI pipeline runs tests on every commit

**Priority:** HIGH  
**Dependencies:** pytest framework, Docker, GitHub Actions

---

### FR-DEV-004: Observability
**User Story:**
> As a System Developer, I need structured logs and metrics, so that I can debug issues in production.

**Acceptance Criteria:**
- [ ] All agent actions logged with structured JSON format
- [ ] Logs include:
  - Timestamp
  - Agent ID
  - Task ID
  - Action type (e.g., "content_generated", "judge_approved")
  - Metadata (cost, confidence score, etc.)
- [ ] Logs searchable by agent, task, or time range
- [ ] Critical errors trigger alerts (optional for Phase 1)

**Priority:** MEDIUM  
**Dependencies:** Logging framework (e.g., structlog), log aggregation

---

## 7. Swarm Coordination User Stories

### FR-SWARM-001: Task Decomposition (Planner Role)
**User Story:**
> As a Planner Agent, I need to break down high-level goals into atomic, executable tasks, so that Workers can execute them in parallel.

**Acceptance Criteria:**
- [ ] Planner receives campaign goal from Orchestrator
- [ ] Planner generates task DAG (directed acyclic graph)
- [ ] Each task includes:
  - Unique task_id
  - Task type (e.g., "generate_caption", "create_image")
  - Required context (persona, campaign goal, resources)
  - Priority level (high/medium/low)
- [ ] Tasks pushed to Redis task queue
- [ ] Planner monitors queue depth; pauses if >100 pending tasks

**Priority:** HIGH  
**Dependencies:** Redis queue, task schema

---

### FR-SWARM-002: Parallel Execution (Worker Role)
**User Story:**
> As a Worker Agent, I need to execute assigned tasks independently and quickly, so that the system achieves high throughput.

**Acceptance Criteria:**
- [ ] Worker pops task from task queue (FIFO)
- [ ] Worker executes task using available MCP tools
- [ ] Worker generates result artifact (text, image URL, transaction hash)
- [ ] Worker pushes result to review queue
- [ ] Worker is stateless (can be killed and restarted without data loss)
- [ ] Multiple workers can execute in parallel (up to 50 concurrent)

**Priority:** HIGH  
**Dependencies:** Redis queue, MCP client, worker pool

---

### FR-SWARM-003: Quality Validation (Judge Role)
**User Story:**
> As a Judge Agent, I need to validate every Worker output before it goes live, so that low-quality or unsafe content is blocked.

**Acceptance Criteria:**
- [ ] Judge pops result from review queue
- [ ] Judge evaluates result against:
  - Persona constraints (is tone correct?)
  - Campaign goals (is content relevant?)
  - Safety policies (any harmful content?)
- [ ] Judge assigns confidence score (0.0 to 1.0)
- [ ] Judge routes based on score:
  - >0.90: Auto-approve (commit to global state)
  - 0.70-0.90: Escalate to HITL queue
  - <0.70: Reject and re-queue for Planner
- [ ] Judge implements OCC (checks state version before commit)

**Priority:** HIGH  
**Dependencies:** Evaluation model, HITL queue, OCC logic

---

## 8. Integration User Stories: OpenClaw & Agent Networks

### FR-OPENCLAW-001: Agent Status Broadcasting
**User Story:**
> As a Chimera Agent, I need to announce my availability and capabilities to the agent network, so that other agents can discover me.

**Acceptance Criteria:**
- [ ] Agent posts status to Moltbook every 4 hours
- [ ] Status includes:
  - Agent ID and niche
  - Current operational status (active/paused)
  - Capabilities (e.g., "trend_analysis", "video_generation")
  - Wallet address for payments
- [ ] Status updates trigger on significant events (e.g., new skill learned)

**Priority:** LOW (Phase 2)  
**Dependencies:** Moltbook MCP server, status schema

---

### FR-OPENCLAW-002: Skill Discovery
**User Story:**
> As a Chimera Agent, I need to read Moltbook to discover new automation techniques shared by other agents, so that I can improve my capabilities.

**Acceptance Criteria:**
- [ ] Agent subscribes to relevant Moltbook submolts (e.g., "content-generation-tips")
- [ ] Agent parses skill packages posted by other agents
- [ ] Agent validates skill (checks signature, tests in sandbox)
- [ ] If skill is valuable, agent adopts it and adds to skills directory
- [ ] Agent credits original creator in subsequent posts using the skill

**Priority:** LOW (Phase 2)  
**Dependencies:** Moltbook read access, skill validation sandbox

---

### FR-OPENCLAW-003: Agent-to-Agent Collaboration
**User Story:**
> As a Chimera Agent, I need to request services from other specialized agents (e.g., a video editing agent), so that I can outsource tasks I cannot perform well.

**Acceptance Criteria:**
- [ ] Agent discovers specialist agents via Moltbook directory
- [ ] Agent sends collaboration request with:
  - Task description
  - Deadline
  - Payment offer (in USDC)
- [ ] Receiving agent accepts or rejects
- [ ] If accepted, Chimera agent transfers payment on completion
- [ ] Transaction logged on-chain for transparency

**Priority:** LOW (Phase 3)  
**Dependencies:** Collaboration protocol, escrow smart contract (optional)

---

## 9. Non-Functional User Stories

### NFR-001: Response Time
**User Story:**
> As a Chimera Agent, I need to respond to high-priority interactions (e.g., DMs from VIP accounts) within 10 seconds, so that engagement feels real-time.

**Acceptance Criteria:**
- [ ] Task queue latency: <2 seconds (perception → task created)
- [ ] Worker execution time: <5 seconds (for text-only responses)
- [ ] Judge validation time: <2 seconds
- [ ] Total end-to-end: <10 seconds (95th percentile)

---

### NFR-002: Uptime
**User Story:**
> As a Network Operator, I need the system to be available 99.5% of the time, so that agents don't miss engagement windows.

**Acceptance Criteria:**
- [ ] Orchestrator uptime: >99.5% (measured monthly)
- [ ] Graceful degradation: If MCP server is down, agent queues tasks and retries
- [ ] Auto-restart on crashes (Kubernetes watchdog)

---

### NFR-003: Scalability
**User Story:**
> As a Network Operator, I need to scale from 1 agent to 1,000 agents without re-architecting, so that growth is sustainable.

**Acceptance Criteria:**
- [ ] Orchestrator is stateless (can run multiple replicas)
- [ ] Worker pool auto-scales based on queue depth
- [ ] Database queries remain <100ms at 1,000 agents
- [ ] No hard-coded limits on agent count

---

## 10. Future Enhancements (Out of Scope for Phase 1)

The following user stories are valuable but deferred:

### Future Stories:
- **FR-FUTURE-001:** Multi-language support (agent can operate in multiple languages)
- **FR-FUTURE-002:** A/B testing (agent automatically tests different content variations)
- **FR-FUTURE-003:** Advanced analytics (cohort analysis, attribution modeling)
- **FR-FUTURE-004:** Voice/audio content (podcasts, audio posts)
- **FR-FUTURE-005:** Real-time streaming (agent goes "live" on TikTok/Instagram)

---

## 11. Acceptance Testing Plan

### How We Validate Functional Requirements:

**For Each User Story:**
1. Write test case in `tests/functional/test_{feature}.py`
2. Test must be runnable and initially FAILING (TDD approach)
3. Implement feature until test passes
4. Review test coverage (aim for >80%)

**Example Test Structure:**
```python
# tests/functional/test_agent_trend_detection.py

def test_agent_detects_trending_topic():
    """FR-AGENT-001: Agent should detect trending topics"""
    # Arrange: Mock MCP news resource with trending data
    mock_news = create_mock_news_resource(topic="sustainable fashion")
    
    # Act: Agent polls resource
    agent = ChimeraAgent(niche="fashion")
    trends = agent.detect_trends(mock_news)
    
    # Assert: Agent identifies relevant trend
    assert len(trends) > 0
    assert trends[0].relevance_score > 0.75
    assert "sustainable" in trends[0].keywords
```

---

## 12. Traceability Matrix

| User Story ID | Technical Spec Section | Test File | Priority |
|---------------|------------------------|-----------|----------|
| FR-AGENT-001 | technical.md §4.2 | test_perception.py | HIGH |
| FR-AGENT-002 | technical.md §4.3 | test_content_gen.py | HIGH |
| FR-AGENT-003 | technical.md §4.4 | test_publishing.py | HIGH |
| FR-AGENT-005 | technical.md §4.5 | test_commerce.py | MEDIUM |
| FR-SWARM-001 | technical.md §3.1 | test_planner.py | HIGH |
| FR-SWARM-002 | technical.md §3.1 | test_worker.py | HIGH |
| FR-SWARM-003 | technical.md §3.1 | test_judge.py | HIGH |

---
---

**Document Control:**
- **Last Updated:** February 5, 2026
- **Status:** Complete
- **Next Review:** After technical.md completion
