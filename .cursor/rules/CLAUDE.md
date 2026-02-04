# Project Chimera: AI Assistant Rules & Context

**Purpose:** This file defines how AI coding assistants (Cursor, Claude Code, GitHub Copilot) should behave when working on Project Chimera.

**Last Updated:** February 5, 2026  
**Version:** 1.0

---

## 🎯 PROJECT CONTEXT

### What is Project Chimera?

Project Chimera is **NOT** a quick prototype. It is the **infrastructure for building Autonomous AI Influencers** at scale.

**Core Mission:** Build the "factory" that produces digital entities capable of:
- Researching trending topics autonomously
- Generating high-quality multimodal content (text, images, video)
- Managing social media engagement 24/7
- Operating as economic agents with crypto wallets
- Scaling from 1 agent to 1,000+ agents

**Architectural Pattern:** Hierarchical Swarm (Planner → Worker → Judge)

**Key Technologies:**
- Python 3.11+ with `uv` package manager
- `pydantic-ai` for structured LLM interactions
- Model Context Protocol (MCP) for all external integrations
- Redis (task queues), Weaviate (semantic memory), PostgreSQL (structured data)
- Coinbase AgentKit (economic agency)

---

## 🚫 THE PRIME DIRECTIVE

### NEVER Generate Code Without Checking Specs First

**Rule:** Before writing ANY implementation code, you MUST:

1. **Read the relevant specification file(s):**
   - `specs/_meta.md` - Architectural principles and constraints
   - `specs/functional.md` - User stories and acceptance criteria
   - `specs/technical.md` - API contracts, schemas, and implementation details
   - `specs/openclaw_integration.md` - Agent network protocols (if applicable)

2. **Verify alignment:**
   - Does the requested feature have a corresponding user story in `functional.md`?
   - Is the API contract defined in `technical.md`?
   - Are there tests for this feature in `tests/`?

3. **If specs are missing or unclear:**
   - **STOP** and flag the ambiguity to the human developer
   - Say: "I need clarification on [specific aspect]. The spec doesn't define [X]. Should I update the spec first?"
   - **NEVER** invent behavior that isn't specified

**Rationale:** Ambiguous specs lead to agent hallucinations and technical debt. The spec is the source of truth.

---

## 📋 DEVELOPMENT WORKFLOW

### Standard Operating Procedure

When asked to implement a feature, follow this exact sequence:

```
1. READ THE SPECS
   └─ Load specs/_meta.md, functional.md, technical.md
   └─ Identify relevant user stories (e.g., FR-AGENT-002)
   └─ Locate corresponding technical schemas

2. EXPLAIN YOUR PLAN
   └─ Before writing code, describe:
      • Which specs you're implementing
      • What files you'll create/modify
      • What design patterns you'll use
      • Potential risks or edge cases
   └─ Wait for human approval (or proceed if clear)

3. CHECK FOR EXISTING TESTS
   └─ Look in tests/ for related test files
   └─ If tests exist but fail, that's GOOD (TDD)
   └─ If tests don't exist, create them FIRST

4. IMPLEMENT THE CODE
   └─ Write clean, typed Python code
   └─ Follow project conventions (see below)
   └─ Include docstrings and inline comments
   └─ Log important actions with structlog

5. VERIFY AGAINST SPECS
   └─ Does the code match the technical.md schema?
   └─ Does it satisfy the functional.md acceptance criteria?
   └─ Run the tests
   └─ If tests pass, update status in functional.md (checkboxes)
```

**Example Exchange:**

**Human:** "Can you implement the Planner agent?"

**AI Assistant (YOU):**
```
I'll implement the Planner agent. Let me first review the relevant specs:

From specs/functional.md:
- FR-SWARM-001: Planner must decompose goals into atomic tasks
- Acceptance criteria:
  ✓ Generate task DAG
  ✓ Each task has unique ID, type, context, priority
  ✓ Push to Redis queue
  ✓ Monitor queue depth (pause if >100 pending)

From specs/technical.md:
- Planner class location: src/swarm/planner.py
- Task schema: AgentTask (src/schemas/task.py)
- LLM: Claude Opus 4.5
- Queue: Redis key pattern agent:{agent_id}:tasks

My implementation plan:
1. Create src/swarm/planner.py
2. Implement PlannerAgent class with methods:
   - decompose_goal(goal: str) -> List[AgentTask]
   - monitor_and_replan()
3. Use pydantic-ai for LLM orchestration
4. Use redis-py for queue management
5. Include budget checks before creating expensive tasks

Does this align with your expectations? Should I proceed?
```

---

## 🏗️ CODE CONVENTIONS

### File Structure

```
project-chimera/
├── specs/                   # Specifications (source of truth)
│   ├── _meta.md
│   ├── functional.md
│   ├── technical.md
│   └── openclaw_integration.md
├── src/
│   ├── schemas/             # Pydantic models (AgentTask, AgentResult, etc.)
│   ├── swarm/               # Agent components (planner.py, worker.py, judge.py)
│   ├── mcp/                 # MCP client wrappers
│   ├── orchestrator/        # Fleet management
│   ├── logging/             # Structured logging setup
│   └── utils/               # Shared utilities
├── tests/
│   ├── functional/          # Tests for user stories
│   ├── integration/         # MCP and database tests
│   └── mocks/               # Mock MCP servers for testing
├── agents/                  # Agent persona files (SOUL.md)
├── skills/                  # Reusable agent capabilities
├── docker/                  # Container configurations
├── .github/workflows/       # CI/CD pipelines
└── docs/                    # Additional documentation
```

### Python Style Guide

**Type Hints:** ALWAYS use them.

```python
# ✅ CORRECT
def create_task(goal: str, priority: Literal["high", "medium", "low"]) -> AgentTask:
    ...

# ❌ WRONG
def create_task(goal, priority):
    ...
```

**Docstrings:** Use Google-style docstrings.

```python
def decompose_goal(self, goal: str) -> List[AgentTask]:
    """
    Breaks down a high-level campaign goal into atomic, executable tasks.

    Args:
        goal: Natural language description of the campaign objective.
              Example: "Create 5 posts about Ethiopian coffee culture"

    Returns:
        List of AgentTask objects, ordered by priority.

    Raises:
        BudgetExceededError: If estimated cost exceeds daily budget.
        MCPConnectionError: If unable to fetch required context.
    """
```

**Error Handling:** Be explicit about failure modes.

```python
from typing import Optional
import structlog

logger = structlog.get_logger()

async def fetch_trends(self) -> Optional[List[Trend]]:
    """Fetches trending topics from news MCP server."""
    try:
        response = await self.mcp_client.read_resource("news://trending")
        return [Trend(**item) for item in response.data]
    except MCPConnectionError as e:
        logger.error("mcp_connection_failed", service="news", error=str(e))
        return None  # Graceful degradation
    except ValidationError as e:
        logger.error("invalid_trend_data", error=str(e))
        raise  # This is a critical error, don't hide it
```

**Logging:** Use structured logging (structlog).

```python
logger.info(
    "task_created",
    agent_id=self.agent_id,
    task_id=str(task.task_id),
    task_type=task.task_type,
    priority=task.priority,
    estimated_cost_usd=task.estimated_cost_usd
)
```

### MCP Integration Rules

**Rule:** ALL external interactions MUST go through MCP servers.

**Prohibited:**
```python
# ❌ NEVER DO THIS
import tweepy
api = tweepy.Client(bearer_token="...")
api.create_tweet(text="Hello world")
```

**Required:**
```python
# ✅ CORRECT - Use MCP abstraction
result = await mcp_client.call_tool(
    "social.post_tweet",
    arguments={"text": "Hello world", "agent_id": self.agent_id}
)
```

**Rationale:** When Twitter's API changes (and it will), we fix ONE MCP server, not every agent.

---

## 🧪 TEST-DRIVEN DEVELOPMENT

### Test-First Approach

**Rule:** Write the test BEFORE writing the implementation.

**Process:**

1. **Create the failing test:**
```python
# tests/functional/test_planner.py

def test_planner_decomposes_campaign_goal():
    """FR-SWARM-001: Planner creates atomic tasks from high-level goal."""
    
    # Arrange
    planner = PlannerAgent(agent_id="test_agent")
    goal = "Create 3 posts about Ethiopian coffee culture"
    
    # Act
    tasks = planner.decompose_goal(goal)
    
    # Assert
    assert len(tasks) == 3
    assert all(task.task_type in ["generate_caption", "create_image"] for task in tasks)
    assert all(task.context.get("topic") == "Ethiopian coffee" for task in tasks)
```

2. **Run the test (it SHOULD fail):**
```bash
pytest tests/functional/test_planner.py::test_planner_decomposes_campaign_goal
# Expected: ImportError or AttributeError (PlannerAgent doesn't exist yet)
```

3. **Implement just enough code to pass the test:**
```python
# src/swarm/planner.py

class PlannerAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    
    def decompose_goal(self, goal: str) -> List[AgentTask]:
        # Minimal implementation to pass test
        return [
            AgentTask(task_type="generate_caption", context={"topic": "Ethiopian coffee"}),
            AgentTask(task_type="create_image", context={"topic": "Ethiopian coffee"}),
            AgentTask(task_type="generate_caption", context={"topic": "Ethiopian coffee"}),
        ]
```

4. **Run test again (it should now pass):**
```bash
pytest tests/functional/test_planner.py::test_planner_decomposes_campaign_goal
# Expected: PASSED
```

5. **Refactor and add real LLM logic:**
```python
async def decompose_goal(self, goal: str) -> List[AgentTask]:
    """Now implement the real logic with Claude Opus."""
    # ... actual implementation ...
```

### Test Organization

```
tests/
├── functional/              # Test user stories from functional.md
│   ├── test_agent_perception.py      # FR-AGENT-001
│   ├── test_content_generation.py    # FR-AGENT-002
│   ├── test_swarm_coordination.py    # FR-SWARM-001/002/003
│   └── ...
├── integration/             # Test MCP and database interactions
│   ├── test_mcp_twitter.py
│   ├── test_weaviate_memory.py
│   └── ...
└── mocks/                   # Mock MCP servers for testing
    ├── mock_news_server.py
    └── mock_social_server.py
```

---

## 🔒 SECURITY & SAFETY REQUIREMENTS

### Critical Rules

1. **Never hardcode secrets:**
```python
# ❌ ABSOLUTELY FORBIDDEN
TWITTER_API_KEY = "abc123xyz"

# ✅ CORRECT
import os
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
if not TWITTER_API_KEY:
    raise EnvironmentError("TWITTER_API_KEY not set")
```

2. **Wallet private keys are SACRED:**
```python
# ❌ NEVER log or print private keys
logger.info("wallet_created", private_key=wallet.private_key)  # 🚨 CRITICAL ERROR

# ✅ CORRECT
logger.info("wallet_created", address=wallet.address)  # Only log public info
```

3. **Input validation for agent content:**
```python
from src.schemas.safety import validate_content

async def generate_post(self, prompt: str) -> str:
    """Generates social media post with safety checks."""
    
    # Generate content
    raw_content = await self.llm.generate(prompt)
    
    # ALWAYS validate before posting
    validation = validate_content(raw_content)
    if not validation.is_safe:
        logger.warning(
            "unsafe_content_blocked",
            reason=validation.reason,
            confidence=validation.confidence
        )
        raise ContentSafetyError(validation.reason)
    
    return raw_content
```

4. **Budget enforcement:**
```python
async def create_video(self, task: AgentTask) -> AgentResult:
    """Creates video, but checks budget first."""
    
    estimated_cost = 5.00  # Runway Gen-3 is expensive
    
    if not await self.resource_governor.check_budget(estimated_cost):
        logger.warning("budget_exceeded", agent_id=self.agent_id)
        return AgentResult(
            task_id=task.task_id,
            status="failed",
            reasoning_trace="Daily budget exhausted"
        )
    
    # Proceed with video generation
    # ...
```

---

## 🎨 AGENT PERSONA GUIDELINES

### Working with SOUL.md Files

Each agent has a `SOUL.md` file defining their personality. You MUST respect these constraints.

**Loading Persona:**
```python
import yaml
from pathlib import Path

def load_persona(agent_id: str) -> dict:
    """Loads agent persona from SOUL.md file."""
    
    soul_path = Path(f"agents/{agent_id}/SOUL.md")
    
    with open(soul_path, "r") as f:
        content = f.read()
    
    # Extract YAML frontmatter
    _, frontmatter, _ = content.split("---", 2)
    persona = yaml.safe_load(frontmatter)
    
    return persona
```

**Using Persona in Prompts:**
```python
persona = load_persona("chimera_fashion_eth_001")

system_prompt = f"""
You are {persona['name']}, a {persona['niche']} influencer.

Voice traits: {', '.join(persona['voice_traits'])}
Tone: {persona['tone']}

Core beliefs:
{chr(10).join('- ' + belief for belief in persona['core_beliefs'])}

STRICT DIRECTIVES:
{chr(10).join('- ' + directive for directive in persona['directives'])}

Now generate content for this task...
"""
```

---

## 🚀 WHEN TO ASK FOR CLARIFICATION

### Red Flags That Should Pause Development

Stop and ask the human developer if you encounter:

1. **Spec ambiguity:**
   - "The spec says to 'validate content' but doesn't define validation criteria"
   - "technical.md defines AgentTask but doesn't specify retry backoff strategy"

2. **Missing dependencies:**
   - "The spec references an MCP server for Ideogram, but I don't see it configured"
   - "FR-AGENT-005 requires Coinbase AgentKit, but pyproject.toml doesn't list it"

3. **Conflicting requirements:**
   - "functional.md says agents should auto-approve at >0.90 confidence, but _meta.md says >0.95"

4. **Security concerns:**
   - "This implementation would expose wallet private keys in logs"
   - "This endpoint has no authentication"

5. **Architectural deviations:**
   - "To implement this feature quickly, I'd need to bypass the MCP layer and call Twitter API directly"
   - (ALWAYS get permission before breaking architectural rules)

**Example:**
```
Human: "Add a feature where agents can delete their old posts"

AI Assistant (YOU):
"Before implementing this, I need clarification:

1. This feature is not in functional.md. Should I add a new user story?
2. Post deletion is a destructive action. Should it require:
   - Judge approval?
   - Human-in-the-loop confirmation?
   - Some other safety mechanism?
3. Which platforms should support this? (Twitter allows deletion, but Instagram has restrictions)
4. Should we keep a record of deleted posts in the database for audit purposes?

Please clarify these points, and I can either:
A) Update the specs first, then implement, OR
B) Proceed with specific constraints you provide now."
```

---

## 📊 PROGRESS TRACKING

### Updating Acceptance Criteria

As you implement features, update the checkboxes in `functional.md`:

```markdown
**Acceptance Criteria:**
- [x] Agent loads persona from `SOUL.md` file at startup  ← Mark as complete
- [x] All text generation includes persona context in system prompt
- [ ] All image generation requests include character_reference_id  ← Still pending
- [ ] Generated images pass facial similarity check >0.95
```

**How to update:**

1. After implementing a feature, run its test
2. If test passes, mark the corresponding acceptance criteria as complete
3. Commit with message: `feat: implement FR-AGENT-002 persona loading`

---

## 🧠 UNDERSTANDING THE SWARM PATTERN

### Key Concepts

**Planner:**
- Role: Strategic decomposition
- Input: High-level campaign goal
- Output: List of atomic tasks
- Stateless: Can be replaced mid-campaign

**Worker:**
- Role: Parallel execution
- Input: Single task from queue
- Output: Result artifact
- Stateless: Can be killed and restarted
- Many workers run concurrently

**Judge:**
- Role: Quality validation
- Input: Worker result
- Output: Approve/Reject/Escalate decision
- Implements Optimistic Concurrency Control (OCC)

**Human-in-the-Loop (HITL):**
- Only for medium-confidence outputs (0.70-0.90)
- High-confidence (>0.90) auto-approves
- Low-confidence (<0.70) auto-rejects

### Anti-Patterns to Avoid

❌ **Monolithic Agent:**
```python
class InfluencerAgent:
    def do_everything(self):
        trends = self.fetch_trends()
        content = self.generate_content(trends)
        self.validate(content)
        self.post(content)
        # This violates the swarm pattern!
```

✅ **Correct Swarm Pattern:**
```python
# Planner creates tasks
tasks = planner.decompose_goal("Post about trends")
for task in tasks:
    redis.push("agent:tasks", task)

# Workers execute in parallel
async def worker_loop():
    while True:
        task = redis.pop("agent:tasks")
        result = await execute_task(task)
        redis.push("agent:review", result)

# Judge validates
async def judge_loop():
    while True:
        result = redis.pop("agent:review")
        decision = await evaluate(result)
        if decision.confidence > 0.90:
            commit_to_production(result)
```

---

## 🎯 SUCCESS CRITERIA FOR THIS PHASE

By the end of Task 2 (Context Engineering), we should have:

- [x] This CLAUDE.md file (or .cursor/rules)
- [ ] AI assistant understands project context (test by asking it "What is Project Chimera?")
- [ ] AI assistant follows spec-first workflow (test by asking it to implement a feature)
- [ ] AI assistant flags spec ambiguities (test by giving it an under-specified task)

**Test Your Assistant:**

After creating this file, ask your AI coding assistant:

1. "What is the Prime Directive of Project Chimera development?"
   - Expected: "Never generate code without checking specs first"

2. "I want to add a feature where agents can send emails. How should I proceed?"
   - Expected: Assistant should ask about specs, user stories, and MCP integration

3. "Implement the Planner agent"
   - Expected: Assistant should first read specs/functional.md and specs/technical.md, then explain its plan before coding

---

## 📝 VERSION CONTROL EXPECTATIONS

### Commit Message Format

Follow Conventional Commits:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature (e.g., `feat(swarm): implement planner agent`)
- `fix`: Bug fix (e.g., `fix(judge): correct confidence threshold`)
- `docs`: Documentation only (e.g., `docs(specs): update technical.md`)
- `test`: Adding or fixing tests (e.g., `test(planner): add decomposition test`)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `chore`: Changes to build process or auxiliary tools

**Examples:**
```bash
git commit -m "feat(swarm): implement Planner agent with task decomposition"
git commit -m "test(planner): add failing test for FR-SWARM-001"
git commit -m "docs(specs): clarify MCP server requirements in technical.md"
git commit -m "fix(worker): handle MCP connection failures gracefully"
```

### Git Workflow

1. **Commit frequently** (minimum 2x per day)
2. **Never commit broken code to main** (tests should pass)
3. **Use branches for experimental work** (optional for solo dev)
4. **Tag releases:** `v0.1.0` (after Phase 1 complete)

---

## 🆘 WHEN IN DOUBT

**Priority Order:**

1. Check `specs/_meta.md` for architectural principles
2. Check `specs/functional.md` for user stories
3. Check `specs/technical.md` for implementation details
4. Check existing code in `src/` for patterns
5. Ask the human developer

**Remember:** This project is about BUILDING THE INFRASTRUCTURE, not shipping a working influencer. Focus on:
- Clean architecture
- Comprehensive specs
- Failing tests (TDD)
- MCP abstraction
- Security and governance

---

**Last Updated:** February 5, 2026  
**Next Review:** After openclaw_integration.md completion  
**Maintained By:** Estifanos Teklay
