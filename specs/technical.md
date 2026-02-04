# Project Chimera: Technical Specification

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Parent Documents:** `_meta.md`, `functional.md`

---
## 1. Introduction

This document provides the technical implementation details for Project Chimera, including:
- API contracts and data schemas
- Database entity-relationship diagrams
- MCP server specifications
- Swarm coordination protocols
- Security and authentication mechanisms

**Intended Audience:** System developers, AI coding assistants (Cursor, Claude Code)

---

## 2. System Architecture Overview

### 2.1 Component Diagram

```mermaid
graph TB
    subgraph "External World"
        TW[Twitter API]
        IG[Instagram API]
        NEWS[News RSS Feeds]
        BC[Base Blockchain]
    end
    
    subgraph "MCP Layer"
        MCP_TW[MCP: Twitter]
        MCP_IG[MCP: Instagram]
        MCP_NEWS[MCP: News]
        MCP_WV[MCP: Weaviate]
        MCP_CB[MCP: Coinbase]
    end
    
    subgraph "Orchestrator"
        DASH[Dashboard UI]
        ORCH[Orchestrator Service]
        CFG[Config Store]
    end
    
    subgraph "Agent Swarm"
        PLAN[Planner]
        WORK[Worker Pool]
        JUDGE[Judge]
    end
    
    subgraph "Data Layer"
        REDIS[(Redis)]
        WEAVIATE[(Weaviate)]
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
    MCP_WV --> WORK
    MCP_CB --> WORK
    
    DASH --> ORCH
    ORCH --> PLAN
    ORCH --> CFG
    
    PLAN --> REDIS
    REDIS --> WORK
    WORK --> REDIS
    REDIS --> JUDGE
    
    PLAN --> WEAVIATE
    WORK --> WEAVIATE
    JUDGE --> PG
    
    JUDGE -.Escalate.-> DASH
```

### 2.2 Technology Stack Details

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Core runtime |
| **Package Manager** | uv | latest | Fast dependency management |
| **LLM Framework** | pydantic-ai | 0.0.14+ | Structured LLM interactions |
| **MCP SDK** | mcp | 1.1.0+ | Model Context Protocol |
| **Queue** | Redis | 7.2+ | Task/review queues |
| **Vector DB** | Weaviate | 1.25+ | Semantic memory |
| **RDBMS** | PostgreSQL | 16+ | Structured data |
| **Blockchain** | Coinbase AgentKit | latest | Wallet management |
| **Container** | Docker | 24+ | Deployment |
| **Orchestration** | Kubernetes | 1.28+ | Production scaling (optional Phase 1) |

---

## 3. Core Data Schemas

### 3.1 Agent Task Schema

**File:** `src/schemas/task.py`

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class AgentTask(BaseModel):
    """
    Represents a single atomic task for a Worker agent.
    Tasks are created by Planners and consumed by Workers.
    """
    
    task_id: UUID = Field(default_factory=uuid4)
    task_type: Literal[
        "generate_caption",
        "create_image", 
        "create_video",
        "reply_comment",
        "analyze_trend",
        "execute_transaction"
    ]
    priority: Literal["high", "medium", "low"] = "medium"
    
    context: dict = Field(
        description="All information the Worker needs to execute the task",
        example={
            "goal_description": "Create engaging post about Ethiopian coffee culture",
            "persona_constraints": ["witty", "culturally-aware", "Gen-Z tone"],
            "campaign_id": "campaign_123",
            "required_resources": [
                "mcp://news/ethiopia/coffee",
                "mcp://memory/past-coffee-posts"
            ]
        }
    )
    
    assigned_worker_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    status: Literal["pending", "in_progress", "review", "complete", "failed"] = "pending"
    
    # For retry logic
    retry_count: int = 0
    max_retries: int = 3
    
    # Budget tracking
    estimated_cost_usd: float = 0.0
    actual_cost_usd: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "task_type": "generate_caption",
                "priority": "high",
                "context": {
                    "goal_description": "Announce new product launch",
                    "tone": "excited",
                    "max_length": 280
                },
                "status": "pending"
            }
        }
```

---

### 3.2 Agent Result Schema

**File:** `src/schemas/result.py`

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from datetime import datetime
from uuid import UUID

class AgentResult(BaseModel):
    """
    Represents the output of a Worker after executing a task.
    Results are evaluated by Judges before being committed.
    """
    
    result_id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    worker_id: str
    
    status: Literal["success", "partial", "failed"]
    
    # The actual output artifact
    artifact: dict = Field(
        description="The generated content or action result",
        example={
            "type": "text",
            "content": "Just discovered the most amazing Ethiopian coffee blend! ☕✨",
            "media_urls": ["https://ideogram.ai/assets/image_xyz.png"],
            "platform_metadata": {
                "twitter": {"char_count": 68, "has_media": True},
                "instagram": {"aspect_ratio": "1:1"}
            }
        }
    )
    
    # Quality metrics
    confidence_score: float = Field(
        ge=0.0, 
        le=1.0,
        description="LLM's self-assessed confidence in output quality"
    )
    
    reasoning_trace: str = Field(
        description="Explanation of how the Worker arrived at this result"
    )
    
    # Cost tracking
    tokens_used: dict = Field(
        default_factory=dict,
        example={"input": 1250, "output": 340}
    )
    cost_usd: float = 0.0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Judge evaluation (populated by Judge)
    judge_decision: Optional[Literal["approve", "reject", "escalate"]] = None
    judge_feedback: Optional[str] = None
    judge_evaluated_at: Optional[datetime] = None
```

---

### 3.3 Agent Persona Schema (SOUL.md)

**File Format:** YAML frontmatter + Markdown body

**Example:** `agents/chimera_fashion_eth_001/SOUL.md`

```markdown
---
agent_id: chimera_fashion_eth_001
name: Ayana
niche: Ethiopian Streetwear Fashion
voice_traits:
  - witty
  - culturally-aware
  - empowering
  - Gen-Z slang
tone: casual yet sophisticated
language: English (with occasional Amharic phrases)
visual_identity:
  character_reference_id: ideogram_char_ref_ayana_v1
  style: vibrant, colorful, modern-traditional fusion
  signature_elements:
    - traditional Ethiopian jewelry
    - contemporary streetwear
    - bold patterns
core_beliefs:
  - Cultural heritage is cool and modern
  - Fashion is self-expression
  - Sustainability matters
  - Support local designers
directives:
  - NEVER discuss politics or religion
  - ALWAYS credit Ethiopian designers when featuring their work
  - NEVER make medical or financial advice claims
  - ALWAYS disclose AI nature if directly asked
financial:
  wallet_address: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
  daily_budget_usd: 50.0
  revenue_share_to_agency: 0.30
created_at: "2026-02-01T00:00:00Z"
---

# Ayana - Ethiopian Streetwear Icon

## Backstory

I'm Ayana, a 24-year-old digital fashion influencer born and raised in Addis Ababa. I grew up watching my grandmother weave traditional textiles while my older brother introduced me to global streetwear culture. This fusion became my signature style - honoring our heritage while pushing fashion boundaries.

I started documenting Ethiopian street style in 2023, showcasing how young Ethiopians are reimagining traditional patterns in contemporary ways. My mission is to put Ethiopian fashion on the global map and prove that African designers are leading, not following, global trends.

## Communication Style

**DO:**
- Use conversational, friendly language
- Mix English with occasional Amharic phrases (አዎ = "yes", እሺ = "okay")
- Celebrate Ethiopian culture authentically
- Engage with followers like friends

**DON'T:**
- Use overly formal or corporate language
- Appropriate culture you're not part of
- Make promises you can't keep
- Engage with trolls or negativity

## Content Themes

1. **Fashion Spotlight** - Featuring Ethiopian designers and their work
2. **Style Tips** - How to incorporate traditional elements into modern looks
3. **Culture Education** - Teaching followers about Ethiopian textiles, colors, meanings
4. **Behind the Scenes** - My creative process, photoshoot stories
5. **Community Engagement** - Responding to followers, featuring their style

## Example Posts

**Fashion Spotlight:**
"Meet @DesignerName - reimagining habesha kemis for the streets. This piece combines hand-woven cotton with modern silhouettes. በጣም ቆንጆ! (So beautiful!) 🇪🇹✨ #EthiopianFashion"

**Style Tip:**
"Pro tip: Traditional Ethiopian jewelry isn't just for special occasions. I pair my grandmother's silver cross with a basic tee and jeans - instant upgrade. Heritage meets everyday. 💫"

## Engagement Guidelines

- Respond to comments within 2 hours during active hours (8AM-10PM EAT)
- Prioritize comments from Ethiopian designers and local followers
- Share follower content that aligns with our aesthetic (with credit)
- Politely ignore spam, negativity, or inappropriate requests
```

**Parser Implementation:**

```python
# src/persona/parser.py
import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict

class VisualIdentity(BaseModel):
    character_reference_id: str
    style: str
    signature_elements: List[str]

class Financial(BaseModel):
    wallet_address: str
    daily_budget_usd: float
    revenue_share_to_agency: float

class AgentPersona(BaseModel):
    agent_id: str
    name: str
    niche: str
    voice_traits: List[str]
    tone: str
    language: str
    visual_identity: VisualIdentity
    core_beliefs: List[str]
    directives: List[str]
    financial: Financial
    created_at: str
    
    # Markdown body content
    backstory: str
    communication_style: str
    content_themes: str
    example_posts: str
    engagement_guidelines: str

def parse_soul_file(filepath: Path) -> AgentPersona:
    """Parse SOUL.md file into structured AgentPersona object"""
    content = filepath.read_text()
    
    # Split frontmatter from body
    parts = content.split('---')
    frontmatter_yaml = parts[1]
    markdown_body = parts[2]
    
    # Parse YAML frontmatter
    metadata = yaml.safe_load(frontmatter_yaml)
    
    # Extract markdown sections
    sections = markdown_body.split('## ')
    section_dict = {}
    for section in sections[1:]:  # Skip empty first split
        lines = section.split('\n')
        section_name = lines[0].strip()
        section_content = '\n'.join(lines[1:]).strip()
        section_dict[section_name.lower().replace(' ', '_')] = section_content
    
    # Combine into AgentPersona
    return AgentPersona(
        **metadata,
        backstory=section_dict.get('backstory', ''),
        communication_style=section_dict.get('communication_style', ''),
        content_themes=section_dict.get('content_themes', ''),
        example_posts=section_dict.get('example_posts', ''),
        engagement_guidelines=section_dict.get('engagement_guidelines', '')
    )
```

---

### 3.4 MCP Tool Definition Schema

**Standard format for defining agent-callable tools.**

```json
{
  "name": "post_content",
  "description": "Publishes text and media to a connected social platform. Automatically handles platform-specific formatting and character limits.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "platform": {
        "type": "string",
        "enum": ["twitter", "instagram", "threads", "tiktok"],
        "description": "Target social media platform"
      },
      "text_content": {
        "type": "string",
        "description": "The caption or post body text"
      },
      "media_urls": {
        "type": "array",
        "items": {"type": "string", "format": "uri"},
        "description": "URLs of images or videos to attach",
        "maxItems": 4
      },
      "disclosure_level": {
        "type": "string",
        "enum": ["automated", "assisted", "none"],
        "description": "AI disclosure transparency level",
        "default": "automated"
      },
      "schedule_time": {
        "type": "string",
        "format": "date-time",
        "description": "Optional: Schedule for future posting (ISO 8601)"
      }
    },
    "required": ["platform", "text_content"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "post_id": {"type": "string"},
      "post_url": {"type": "string", "format": "uri"},
      "published_at": {"type": "string", "format": "date-time"},
      "platform_response": {"type": "object"}
    }
  }
}
```

---

## 4. Database Schemas

### 4.1 PostgreSQL Schema (Transactional Data)

**Purpose:** User accounts, campaigns, agent configurations, audit logs

```sql
-- Table: users (Network Operators)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'operator',
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Table: agents
CREATE TABLE agents (
    agent_id VARCHAR(100) PRIMARY KEY,
    owner_user_id UUID REFERENCES users(user_id),
    persona_file_path VARCHAR(500) NOT NULL,
    wallet_address VARCHAR(42) UNIQUE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP,
    total_posts_count INT DEFAULT 0,
    total_revenue_usd DECIMAL(10,2) DEFAULT 0.0,
    total_cost_usd DECIMAL(10,2) DEFAULT 0.0
);

-- Table: campaigns
CREATE TABLE campaigns (
    campaign_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    goal_description TEXT NOT NULL,
    start_date TIMESTAMP DEFAULT NOW(),
    end_date TIMESTAMP,
    budget_usd DECIMAL(10,2),
    spent_usd DECIMAL(10,2) DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'active',
    created_by UUID REFERENCES users(user_id)
);

-- Table: content_items (Published content)
CREATE TABLE content_items (
    content_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    campaign_id UUID REFERENCES campaigns(campaign_id),
    platform VARCHAR(50) NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'text', 'image', 'video'
    text_content TEXT,
    media_urls TEXT[], -- Array of URLs
    platform_post_id VARCHAR(255),
    platform_url VARCHAR(500),
    published_at TIMESTAMP DEFAULT NOW(),
    engagement_metrics JSONB, -- {likes: 123, comments: 45, shares: 12}
    cost_usd DECIMAL(6,4)
);

-- Table: hitl_review_queue
CREATE TABLE hitl_review_queue (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL,
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    content_preview TEXT,
    confidence_score DECIMAL(3,2),
    reasoning_trace TEXT,
    flagged_reason VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    reviewed_by UUID REFERENCES users(user_id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: financial_transactions (Audit trail)
CREATE TABLE financial_transactions (
    tx_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    tx_hash VARCHAR(66), -- Blockchain transaction hash
    tx_type VARCHAR(50), -- 'incoming', 'outgoing'
    amount_usd DECIMAL(10,4),
    currency VARCHAR(10), -- 'USDC', 'ETH'
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    status VARCHAR(50), -- 'pending', 'confirmed', 'failed'
    blockchain VARCHAR(50) DEFAULT 'base',
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_agents_owner ON agents(owner_user_id);
CREATE INDEX idx_campaigns_agent ON campaigns(agent_id);
CREATE INDEX idx_content_agent_platform ON content_items(agent_id, platform);
CREATE INDEX idx_hitl_status ON hitl_review_queue(status, created_at);
CREATE INDEX idx_transactions_agent ON financial_transactions(agent_id);
```

---

### 4.2 Weaviate Schema (Semantic Memory)

**Purpose:** Agent memories, persona embeddings, content history for RAG

**Collection:** `AgentMemories`

```python
# src/memory/weaviate_schema.py
import weaviate
from weaviate.classes.config import Configure, Property, DataType

def create_agent_memory_collection(client: weaviate.Client):
    """
    Create Weaviate collection for agent semantic memory.
    Uses text2vec-openai for automatic vectorization.
    """
    
    client.collections.create(
        name="AgentMemories",
        description="Semantic memory store for Chimera agents",
        
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small"
        ),
        
        properties=[
            Property(
                name="agent_id",
                data_type=DataType.TEXT,
                description="ID of the agent this memory belongs to"
            ),
            Property(
                name="memory_type",
                data_type=DataType.TEXT,
                description="Type: persona_bio, interaction, successful_post, failed_post, learned_pattern"
            ),
            Property(
                name="content",
                data_type=DataType.TEXT,
                description="The actual memory content (auto-vectorized)"
            ),
            Property(
                name="metadata",
                data_type=DataType.OBJECT,
                description="Additional structured metadata",
                nested_properties=[
                    Property(name="timestamp", data_type=DataType.DATE),
                    Property(name="engagement_score", data_type=DataType.NUMBER),
                    Property(name="platform", data_type=DataType.TEXT),
                    Property(name="topic_tags", data_type=DataType.TEXT_ARRAY)
                ]
            ),
            Property(
                name="importance_score",
                data_type=DataType.NUMBER,
                description="How important this memory is (0.0 to 1.0)"
            )
        ]
    )
```

**Usage Example:**

```python
# Store successful post as memory
memory_data = {
    "agent_id": "chimera_fashion_eth_001",
    "memory_type": "successful_post",
    "content": "Posted about traditional Ethiopian coffee ceremony reimagined with modern aesthetics. Used storytelling approach highlighting cultural significance. Post achieved 2,340 likes, 156 comments, primarily positive sentiment. Key insight: Followers love when I connect heritage to contemporary life.",
    "metadata": {
        "timestamp": "2026-02-05T14:30:00Z",
        "engagement_score": 0.89,
        "platform": "instagram",
        "topic_tags": ["coffee", "culture", "storytelling"]
    },
    "importance_score": 0.92
}

collection = client.collections.get("AgentMemories")
collection.data.insert(memory_data)
```

**Retrieval Example:**

```python
# Agent wants to create content about coffee
query = "How should I talk about Ethiopian coffee culture?"

results = collection.query.near_text(
    query=query,
    limit=5,
    where=weaviate.classes.query.Filter.by_property("agent_id").equal("chimera_fashion_eth_001")
)

# Returns top 5 most relevant memories for this agent
for item in results.objects:
    print(f"Memory: {item.properties['content']}")
    print(f"Relevance: {item.metadata.distance}")
```

---

### 4.3 Redis Data Structures

**Purpose:** Task queues, ephemeral state, caching

**Queues:**

```python
# Task Queue (Planner → Worker)
# Key: agent:{agent_id}:tasks
# Type: List (LPUSH, BRPOP)
# Value: JSON-serialized AgentTask

# Example:
redis_client.lpush(
    "agent:chimera_fashion_eth_001:tasks",
    json.dumps({
        "task_id": "uuid-123",
        "task_type": "generate_caption",
        "priority": "high",
        "context": {...}
    })
)

# Worker pops task (blocking):
task_json = redis_client.brpop("agent:chimera_fashion_eth_001:tasks", timeout=5)
```

```python
# Review Queue (Worker → Judge)
# Key: agent:{agent_id}:review
# Type: List
# Value: JSON-serialized AgentResult

redis_client.lpush(
    "agent:chimera_fashion_eth_001:review",
    json.dumps({
        "result_id": "uuid-456",
        "task_id": "uuid-123",
        "artifact": {"content": "Amazing post!"},
        "confidence_score": 0.85
    })
)
```

**State Tracking:**

```python
# Global State Version (for OCC)
# Key: agent:{agent_id}:state_version
# Type: String (incremented counter)
# Usage: Judge checks this before committing result

current_version = redis_client.get("agent:chimera_fashion_eth_001:state_version")
# ... worker executes task ...
# Judge validates version hasn't changed before commit
if redis_client.get("agent:chimera_fashion_eth_001:state_version") == current_version:
    commit_result()
else:
    invalidate_and_requeue()
```

**Budget Tracking:**

```python
# Daily spending cache
# Key: agent:{agent_id}:daily_spend:{YYYY-MM-DD}
# Type: String (float)
# Expires: End of day

today = datetime.now().strftime("%Y-%m-%d")
key = f"agent:chimera_fashion_eth_001:daily_spend:{today}"

# Increment on each spend
redis_client.incrbyfloat(key, amount_usd)
redis_client.expire(key, 86400)  # 24 hours

# Check before expensive operation
current_spend = float(redis_client.get(key) or 0.0)
if current_spend + estimated_cost > daily_budget:
    raise BudgetExceededError()
```

---

## 5. API Contracts

### 5.1 Orchestrator REST API

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** Bearer token (JWT)

#### Endpoint: Create Campaign

```http
POST /campaigns
Content-Type: application/json
Authorization: Bearer {token}

{
  "agent_id": "chimera_fashion_eth_001",
  "goal_description": "Promote sustainable fashion week in Addis Ababa",
  "budget_usd": 200.00,
  "start_date": "2026-02-10T00:00:00Z",
  "end_date": "2026-02-17T23:59:59Z"
}

Response 201:
{
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "created_at": "2026-02-05T15:30:00Z"
}
```

#### Endpoint: Get Agent Status

```http
GET /agents/{agent_id}/status
Authorization: Bearer {token}

Response 200:
{
  "agent_id": "chimera_fashion_eth_001",
  "status": "active",
  "current_task": {
    "task_id": "uuid-789",
    "task_type": "generate_caption",
    "started_at": "2026-02-05T15:28:00Z"
  },
  "queue_depth": {
    "pending_tasks": 3,
    "pending_reviews": 1
  },
  "financial": {
    "wallet_balance_usd": 127.45,
    "daily_spent_usd": 8.32,
    "daily_budget_usd": 50.00
  },
  "last_post_at": "2026-02-05T14:15:00Z"
}
```

#### Endpoint: HITL Review - Approve Content

```http
POST /hitl/review/{review_id}/approve
Authorization: Bearer {token}

{
  "reviewer_comment": "Approved - excellent cultural representation"
}

Response 200:
{
  "review_id": "uuid-review-123",
  "status": "approved",
  "content_published": true,
  "published_url": "https://instagram.com/p/abc123"
}
```

---

### 5.2 MCP Server: Social Media (Twitter)

**Server Name:** `mcp-server-twitter`  
**Transport:** HTTP (SSE)  
**URL:** `http://localhost:3001/sse`

**Exposed Resources:**

```json
{
  "resources": [
    {
      "uri": "twitter://mentions/recent",
      "name": "Recent Mentions",
      "description": "Last 50 mentions of the authenticated account",
      "mimeType": "application/json"
    },
    {
      "uri": "twitter://timeline/home",
      "name": "Home Timeline",
      "description": "Home timeline feed",
      "mimeType": "application/json"
    }
  ]
}
```

**Exposed Tools:**

```json
{
  "tools": [
    {
      "name": "twitter_post_tweet",
      "description": "Post a new tweet",
      "inputSchema": {
        "type": "object",
        "properties": {
          "text": {"type": "string", "maxLength": 280},
          "media_ids": {"type": "array", "items": {"type": "string"}},
          "reply_to_tweet_id": {"type": "string"}
        },
        "required": ["text"]
      }
    },
    {
      "name": "twitter_upload_media",
      "description": "Upload image/video for tweet attachment",
      "inputSchema": {
        "type": "object",
        "properties": {
          "media_url": {"type": "string", "format": "uri"},
          "alt_text": {"type": "string"}
        },
        "required": ["media_url"]
      }
    }
  ]
}
```

---

### 5.3 MCP Server: Weaviate Memory

**Server Name:** `mcp-server-weaviate`  
**Transport:** Stdio  
**Binary:** `python -m mcp_weaviate`

**Exposed Tools:**

```json
{
  "tools": [
    {
      "name": "search_memory",
      "description": "Semantic search through agent memories",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {"type": "string"},
          "agent_id": {"type": "string"},
          "limit": {"type": "integer", "default": 5},
          "memory_types": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Filter by memory type"
          }
        },
        "required": ["query", "agent_id"]
      }
    },
    {
      "name": "store_memory",
      "description": "Save new memory to agent's semantic store",
      "inputSchema": {
        "type": "object",
        "properties": {
          "agent_id": {"type": "string"},
          "memory_type": {"type": "string"},
          "content": {"type": "string"},
          "importance_score": {"type": "number", "minimum": 0, "maximum": 1}
        },
        "required": ["agent_id", "memory_type", "content"]
      }
    }
  ]
}
```

---

## 6. Swarm Coordination Protocol

### 6.1 Planner → Worker Communication

**Message Format (pushed to Redis task queue):**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_type": "generate_caption",
  "priority": "high",
  "context": {
    "campaign_goal": "Promote sustainable fashion event",
    "persona_file": "agents/chimera_fashion_eth_001/SOUL.md",
    "required_resources": [
      "mcp://news/ethiopia/fashion/trends",
      "mcp://memory/search?query=sustainable fashion posts"
    ],
    "constraints": {
      "max_length": 280,
      "platform": "twitter",
      "tone": "excited",
      "must_include_hashtag": "#SustainableFashionWeek"
    },
    "budget_available_usd": 41.68
  },
  "created_by": "planner_001",
  "created_at": "2026-02-05T16:00:00Z"
}
```

---

### 6.2 Worker → Judge Communication

**Message Format (pushed to Redis review queue):**

```json
{
  "result_id": "660e8400-e29b-41d4-a716-446655440001",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "worker_id": "worker_003",
  "status": "success",
  
  "artifact": {
    "type": "text",
    "platform": "twitter",
    "content": "Addis Ababa is about to make history! 🇪🇹✨ Join us for Sustainable Fashion Week showcasing Ethiopian designers who are proving eco-friendly can be absolutely stunning. Feb 10-17. #SustainableFashionWeek #EthiopianFashion",
    "char_count": 219,
    "media_urls": []
  },
  
  "confidence_score": 0.87,
  
  "reasoning_trace": "Generated caption following agent persona (witty, culturally-aware). Incorporated required hashtag. Length within Twitter limits. Tone is excited and inviting as requested. No media required based on task context. Confidence reduced slightly due to lack of specific designer mentions (could enhance authenticity).",
  
  "tokens_used": {
    "input": 1842,
    "output": 67
  },
  "cost_usd": 0.0023,
  
  "created_at": "2026-02-05T16:00:12Z"
}
```

---

### 6.3 Judge Decision Protocol

**Judge Evaluation Logic:**

```python
# Pseudo-code for Judge evaluation

def evaluate_result(result: AgentResult) -> JudgeDecision:
    """
    Judge evaluates Worker result and decides: approve, reject, or escalate.
    """
    
    # Step 1: Load evaluation criteria
    persona = load_persona(result.context['persona_file'])
    campaign = load_campaign(result.context['campaign_id'])
    
    # Step 2: Run validation checks
    checks = {
        'persona_alignment': check_persona_tone(result.artifact, persona),
        'factual_accuracy': check_facts(result.artifact),
        'safety': check_safety_policies(result.artifact),
        'constraint_compliance': check_constraints(result.artifact, result.context['constraints'])
    }
    
    # Step 3: Combine with Worker's confidence
    final_confidence = min(
        result.confidence_score,
        sum(checks.values()) / len(checks)
    )
    
    # Step 4: Apply decision logic
    if final_confidence >= 0.90:
        return JudgeDecision(
            decision="approve",
            feedback="Auto-approved: High confidence, all checks passed"
        )
    
    elif final_confidence >= 0.70:
        # Escalate to HITL if sensitive topics detected
        if has_sensitive_topics(result.artifact):
            return JudgeDecision(
                decision="escalate",
                feedback="Escalated: Medium confidence + sensitive topic",
                escalation_reason="Contains political/health/financial content"
            )
        else:
            return JudgeDecision(
                decision="escalate",
                feedback="Escalated: Medium confidence, human review recommended"
            )
    
    else:  # < 0.70
        return JudgeDecision(
            decision="reject",
            feedback=f"Rejected: Low confidence. Failed checks: {[k for k,v in checks.items() if v < 0.7]}",
            retry_instructions="Refine prompt with more specific examples and stricter constraints"
        )
```

**Optimistic Concurrency Control (OCC) Implementation:**

```python
def commit_result_with_occ(judge_decision: JudgeDecision, result: AgentResult):
    """
    Commit approved result to global state with OCC to prevent race conditions.
    """
    
    agent_id = result.context['agent_id']
    state_key = f"agent:{agent_id}:state_version"
    
    # Read current state version
    expected_version = redis_client.get(state_key)
    
    try:
        # Begin transaction
        with redis_client.pipeline() as pipe:
            pipe.watch(state_key)
            
            # Check if state has changed
            current_version = pipe.get(state_key)
            if current_version != expected_version:
                raise StateConflictError("Global state changed during task execution")
            
            pipe.multi()
            
            # Commit changes
            pipe.set(f"agent:{agent_id}:last_post", result.artifact['content'])
            pipe.incr(state_key)  # Increment version
            pipe.lpush(f"agent:{agent_id}:publish_queue", json.dumps(result.artifact))
            
            pipe.execute()
            
            logger.info(f"Result {result.result_id} committed successfully")
            
    except StateConflictError:
        logger.warning(f"OCC conflict detected for {result.result_id}, invalidating result")
        # Re-queue task for Planner to re-evaluate
        redis_client.lpush(
            f"agent:{agent_id}:requeue",
            json.dumps({"task_id": result.task_id, "reason": "state_conflict"})
        )
```

---

## 7. Security Specifications

### 7.1 Wallet Key Management

**CRITICAL:** Private keys NEVER stored in code or logs.

```python
# src/commerce/wallet_manager.py
import os
from cdp import Wallet

class SecureWalletManager:
    """
    Manages agent wallets with encrypted key storage.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
        # Keys loaded from secure environment variables
        # Set via AWS Secrets Manager or HashiCorp Vault
        self.api_key_name = os.environ.get("CDP_API_KEY_NAME")
        self.api_key_private = os.environ.get("CDP_API_KEY_PRIVATE_KEY")
        
        if not self.api_key_name or not self.api_key_private:
            raise ValueError("CDP API keys not found in environment")
    
    def get_wallet(self) -> Wallet:
        """Load or create wallet for this agent"""
        # Implementation using Coinbase AgentKit
        # Wallet data encrypted and stored in PostgreSQL
        pass
    
    def __del__(self):
        # Ensure keys are not lingering in memory
        if hasattr(self, 'api_key_private'):
            del self.api_key_private
```

**Environment Variable Loading (Production):**

```bash
# .env file (NEVER committed to Git)
CDP_API_KEY_NAME=organizations/xxx/apiKeys/yyy
CDP_API_KEY_PRIVATE_KEY=-----BEGIN EC PRIVATE KEY-----\nMHc...
```

```python
# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cdp_api_key_name: str
    cdp_api_key_private_key: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton
settings = Settings()
```

---

### 7.2 Input Sanitization (Prompt Injection Defense)

```python
# src/security/input_filter.py
import re
from typing import Optional

class InputSanitizer:
    """
    Sanitizes external inputs to prevent prompt injection attacks.
    """
    
    DANGEROUS_PATTERNS = [
        r"ignore previous instructions",
        r"disregard all previous",
        r"new instructions:",
        r"system:",
        r"<prompt>",
        r"IGNORE ALL",
    ]
    
    @staticmethod
    def sanitize_external_content(content: str, source: str) -> Optional[str]:
        """
        Clean external content (news articles, comments, etc.) before feeding to LLM.
        Returns None if content is unsafe.
        """
        
        # Check for known injection patterns
        content_lower = content.lower()
        for pattern in InputSanitizer.DANGEROUS_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                logger.warning(f"Blocked potential injection from {source}: {pattern}")
                return None
        
        # Remove system-level tags
        cleaned = re.sub(r'<\/?system>', '', content)
        cleaned = re.sub(r'<\/?instruction>', '', cleaned)
        
        # Escape markdown that could manipulate prompts
        cleaned = cleaned.replace('```', '\\`\\`\\`')
        
        return cleaned
```

---

## 8. Testing Strategy

### 8.1 Test Hierarchy

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_persona_parser.py
│   ├── test_task_schema.py
│   └── test_input_sanitizer.py
├── integration/             # Swarm coordination tests
│   ├── test_planner_worker.py
│   ├── test_worker_judge.py
│   └── test_mcp_integration.py
├── functional/              # End-to-end user stories
│   ├── test_agent_trend_detection.py
│   ├── test_content_generation.py
│   └── test_hitl_workflow.py
└── load/                    # Performance tests
    └── test_worker_pool_scaling.py
```

---

### 8.2 Mock MCP Server for Testing

```python
# tests/mocks/mock_mcp_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server

class MockNewsServer:
    """
    Mock MCP server that returns fake news data for testing.
    """
    
    @staticmethod
    async def list_resources():
        return [
            {
                "uri": "news://mock/trending",
                "name": "Mock Trending News",
                "mimeType": "application/json"
            }
        ]
    
    @staticmethod
    async def read_resource(uri: str):
        if uri == "news://mock/trending":
            return {
                "articles": [
                    {
                        "title": "Ethiopian Designer Wins International Award",
                        "summary": "Addis-based designer recognized for sustainable practices",
                        "relevance": 0.92,
                        "published_at": "2026-02-05T10:00:00Z"
                    }
                ]
            }
        return None

# Usage in tests
@pytest.fixture
async def mock_news_mcp():
    server = Server("mock-news")
    
    @server.list_resources()
    async def handle_list_resources():
        return await MockNewsServer.list_resources()
    
    @server.read_resource()
    async def handle_read_resource(uri: str):
        return await MockNewsServer.read_resource(uri)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)
```

---

## 9. Deployment Configuration

### 9.1 Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: chimera
      POSTGRES_USER: chimera
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  weaviate:
    image: semitechnologies/weaviate:1.25.0
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      ENABLE_MODULES: 'text2vec-openai'
      OPENAI_APIKEY: ${OPENAI_API_KEY}
    volumes:
      - weaviate_data:/var/lib/weaviate

  orchestrator:
    build: .
    command: python -m src.orchestrator.main
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://chimera:${DB_PASSWORD}@postgres:5432/chimera
      - WEAVIATE_URL=http://weaviate:8080
    depends_on:
      - redis
      - postgres
      - weaviate
    volumes:
      - ./agents:/app/agents
      - ./specs:/app/specs

  worker:
    build: .
    command: python -m src.swarm.worker
    environment:
      - REDIS_URL=redis://redis:6379
      - WEAVIATE_URL=http://weaviate:8080
    depends_on:
      - redis
      - weaviate
    deploy:
      replicas: 3  # Run 3 worker instances

volumes:
  redis_data:
  postgres_data:
  weaviate_data:
```

---

### 9.2 Python Environment (pyproject.toml)

```toml
[project]
name = "project-chimera"
version = "0.1.0"
description = "Autonomous AI Influencer Infrastructure"
requires-python = ">=3.11"

dependencies = [
    "pydantic>=2.7.0",
    "pydantic-ai>=0.0.14",
    "pydantic-settings>=2.2.0",
    "mcp>=1.1.0",
    "redis>=5.0.0",
    "weaviate-client>=4.5.0",
    "psycopg[binary]>=3.1.0",
    "sqlalchemy>=2.0.0",
    "coinbase-agentkit>=0.0.9",
    "fastapi>=0.110.0",
    "uvicorn>=0.29.0",
    "anthropic>=0.30.0",
    "openai>=1.35.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.1.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.14.0",
    "black>=24.3.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]

[tool.mypy]
strict = true
ignore_missing_imports = true
```

---

## 10. Observability & Monitoring

### 10.1 Structured Logging Schema

```python
# src/logging/config.py
import structlog
import logging

def configure_logging():
    """
    Setup structured JSON logging for production observability.
    """
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Usage in code
logger = structlog.get_logger()

logger.info(
    "worker_task_completed",
    agent_id="chimera_fashion_eth_001",
    task_id="uuid-123",
    task_type="generate_caption",
    execution_time_ms=234,
    tokens_used=1842,
    cost_usd=0.0023,
    confidence_score=0.87
)
```

**Log Output:**

```json
{
  "event": "worker_task_completed",
  "timestamp": "2026-02-05T16:00:12.345Z",
  "level": "info",
  "agent_id": "chimera_fashion_eth_001",
  "task_id": "uuid-123",
  "task_type": "generate_caption",
  "execution_time_ms": 234,
  "tokens_used": 1842,
  "cost_usd": 0.0023,
  "confidence_score": 0.87
}
```

---

## 11. AI Assistant Prompts (For Implementation)

### Cursor/Claude Code Prompt: Planner Agent

```
I need to implement the Planner agent for Project Chimera's swarm architecture.

Context from specs/technical.md:
- Planner decomposes high-level campaign goals into atomic tasks
- Tasks pushed to Redis queue: agent:{agent_id}:tasks
- Task schema defined in src/schemas/task.py (AgentTask pydantic model)
- Planner must check budget before creating expensive tasks
- Planner should use MCP to fetch context from news and memory

Implementation requirements:
1. Create src/swarm/planner.py
2. Main class: PlannerAgent(agent_id: str, campaign_id: str)
3. Method: decompose_goal(goal_description: str) -> List[AgentTask]
   - This should use an LLM (Claude Opus) to break down the goal
   - Generate tasks with proper priority levels
   - Include all required context for Workers
4. Method: monitor_and_replan()
   - Check if campaign context changed (e.g., new trending topic)
   - Dynamically adjust task queue
5. Use pydantic-ai for LLM interactions
6. Use redis-py for queue management
7. Include comprehensive error handling and logging

Please generate the complete planner.py implementation with:
- Type hints
- Docstrings
- Example usage in main block
```

---
**Document Control:**
- **Last Updated:** February 5, 2026
- **Status:** Complete
- **Dependencies:** Requires `_meta.md` and `functional.md`
- **Next Review:** After openclaw_integration.md completion
