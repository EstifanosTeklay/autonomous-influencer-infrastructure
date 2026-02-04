# Project Chimera: Agent Skills Architecture

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Purpose:** Define the reusable capabilities (Skills) that Chimera agents use during operation

---

## 1. What is a Skill?

A **Skill** is a self-contained capability package that a Chimera agent can execute. Think of skills as "plugins" or "apps" that extend what an agent can do.

### Key Characteristics:

- **Atomic:** Each skill does ONE thing well
- **Reusable:** Any agent can use any skill (if it fits their persona)
- **Composable:** Skills can be chained together in workflows
- **Versioned:** Skills have version numbers and changelogs
- **Testable:** Each skill has unit tests
- **MCP-Powered:** Skills call MCP servers, never external APIs directly

### Skills vs. MCP Servers:

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| **Purpose** | Business logic for agent tasks | Low-level interface to external services |
| **Who uses it?** | Chimera agents (runtime) | Skills call these (abstraction layer) |
| **Example** | "Generate Instagram post" | "Twitter API wrapper" |
| **Language** | Python (matches agent runtime) | Any language (Node.js, Python, etc.) |
| **Location** | `skills/` directory | `mcp/servers/` or external packages |

**Mental Model:**
```
Agent Task → Skill (business logic) → MCP Server (API call) → External Service
```

---

## 2. Skill Taxonomy

Skills are organized by capability domain:

```
skills/
├── perception/          # Skills for gathering information
│   ├── trend_detector/
│   ├── comment_analyzer/
│   └── sentiment_scanner/
├── generation/          # Skills for creating content
│   ├── caption_writer/
│   ├── image_creator/
│   └── video_producer/
├── engagement/          # Skills for audience interaction
│   ├── reply_generator/
│   ├── dm_responder/
│   └── hashtag_optimizer/
├── commerce/            # Skills for financial operations
│   ├── wallet_manager/
│   ├── payment_processor/
│   └── budget_tracker/
└── meta/                # Skills for self-improvement
    ├── memory_retriever/
    ├── performance_analyzer/
    └── skill_installer/
```

---

## 3. Skill Interface Contract

Every skill MUST implement this standardized interface:

### 3.1 Directory Structure

```
skills/domain/skill_name/
├── skill.yaml           # Skill metadata and configuration
├── skill.py             # Main skill implementation
├── tests/
│   └── test_skill.py    # Unit tests
├── README.md            # Usage documentation
└── examples/            # Example usage
    └── example.py
```

### 3.2 skill.yaml Specification

```yaml
# skills/perception/trend_detector/skill.yaml

id: trend_detector
version: 1.0.0
name: Trend Detector
description: |
  Detects trending topics in a specific niche by analyzing
  news sources, social media, and search trends.

category: perception
author: Project Chimera Team
created_at: "2026-02-05T00:00:00Z"
updated_at: "2026-02-05T00:00:00Z"

# Input schema (what the skill expects)
input_schema:
  type: object
  required:
    - niche
    - time_window
  properties:
    niche:
      type: string
      description: "Topic area to monitor (e.g., 'Ethiopian fashion')"
      example: "sustainable fashion"
    time_window:
      type: string
      enum: ["1h", "6h", "24h", "7d"]
      description: "How far back to look for trends"
      default: "24h"
    min_relevance:
      type: number
      minimum: 0.0
      maximum: 1.0
      description: "Minimum relevance score (0.0-1.0)"
      default: 0.75

# Output schema (what the skill returns)
output_schema:
  type: object
  required:
    - trends
    - retrieved_at
  properties:
    trends:
      type: array
      items:
        type: object
        properties:
          topic:
            type: string
          relevance_score:
            type: number
          source:
            type: string
          url:
            type: string
    retrieved_at:
      type: string
      format: date-time

# MCP dependencies
mcp_servers:
  required:
    - news  # News aggregation MCP server
  optional:
    - twitter  # For social listening
    - weaviate  # For semantic filtering

# Resource requirements
resources:
  estimated_cost_usd: 0.002  # Per execution
  avg_execution_time_ms: 1500
  requires_api_keys:
    - NEWSAPI_KEY

# Constraints
constraints:
  rate_limit: 100/hour
  max_retries: 3
  timeout_seconds: 10
```

### 3.3 skill.py Interface

```python
# skills/perception/trend_detector/skill.py

from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime
import structlog

logger = structlog.get_logger()

class TrendDetectorInput(BaseModel):
    """Input parameters for Trend Detector skill."""
    niche: str
    time_window: str = "24h"
    min_relevance: float = 0.75

class Trend(BaseModel):
    """A single trending topic."""
    topic: str
    relevance_score: float
    source: str
    url: str

class TrendDetectorOutput(BaseModel):
    """Output from Trend Detector skill."""
    trends: list[Trend]
    retrieved_at: datetime

class TrendDetectorSkill:
    """
    Detects trending topics in a specific niche.
    
    This skill aggregates data from news sources and social media
    to identify what's currently gaining traction in a given domain.
    """
    
    def __init__(self, mcp_client: Any):
        """
        Initialize skill with MCP client.
        
        Args:
            mcp_client: Connected MCP client for accessing Resources/Tools
        """
        self.mcp_client = mcp_client
        self.skill_id = "trend_detector"
        self.version = "1.0.0"
    
    async def execute(self, input_data: TrendDetectorInput) -> TrendDetectorOutput:
        """
        Main execution method.
        
        Args:
            input_data: Validated input parameters
        
        Returns:
            Detected trends with relevance scores
        
        Raises:
            MCPConnectionError: If news MCP server is unavailable
            ValidationError: If input data is invalid
        """
        logger.info(
            "skill_execution_started",
            skill_id=self.skill_id,
            niche=input_data.niche,
            time_window=input_data.time_window
        )
        
        try:
            # Step 1: Fetch news articles from MCP server
            news_resource = f"news://{input_data.niche}/trending"
            raw_articles = await self.mcp_client.read_resource(news_resource)
            
            # Step 2: Filter by relevance
            relevant_trends = [
                Trend(
                    topic=article["title"],
                    relevance_score=article["relevance"],
                    source=article["source"],
                    url=article["url"]
                )
                for article in raw_articles["articles"]
                if article["relevance"] >= input_data.min_relevance
            ]
            
            # Step 3: Sort by relevance
            relevant_trends.sort(key=lambda t: t.relevance_score, reverse=True)
            
            logger.info(
                "skill_execution_completed",
                skill_id=self.skill_id,
                trends_found=len(relevant_trends)
            )
            
            return TrendDetectorOutput(
                trends=relevant_trends,
                retrieved_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(
                "skill_execution_failed",
                skill_id=self.skill_id,
                error=str(e)
            )
            raise

# Factory function for skill instantiation
def create_skill(mcp_client: Any) -> TrendDetectorSkill:
    """Factory function to create skill instance."""
    return TrendDetectorSkill(mcp_client)
```

---

## 4. Required Skills for Phase 1

Based on `specs/functional.md`, these skills are essential:

### 4.1 Skill: Trend Detector (PERCEPTION)

**ID:** `trend_detector`  
**Priority:** HIGH  
**Functional Requirement:** FR-AGENT-001  

**Input:**
```json
{
  "niche": "Ethiopian fashion",
  "time_window": "24h",
  "min_relevance": 0.75
}
```

**Output:**
```json
{
  "trends": [
    {
      "topic": "Sustainable cotton farming in Ethiopia gains international attention",
      "relevance_score": 0.92,
      "source": "Fashion Industry News",
      "url": "https://example.com/article"
    }
  ],
  "retrieved_at": "2026-02-05T16:00:00Z"
}
```

**MCP Dependencies:**
- News MCP server (required)
- Weaviate MCP (optional, for semantic filtering)

**Status:** Interface defined, implementation pending

---

### 4.2 Skill: Caption Writer (GENERATION)

**ID:** `caption_writer`  
**Priority:** HIGH  
**Functional Requirement:** FR-AGENT-002  

**Input:**
```json
{
  "topic": "Ethiopian coffee culture",
  "persona_id": "chimera_fashion_eth_001",
  "platform": "instagram",
  "tone": "excited",
  "max_length": 2200,
  "include_hashtags": true,
  "include_call_to_action": true
}
```

**Output:**
```json
{
  "caption": "Just discovered the most incredible thing about Ethiopian coffee culture! ☕✨ Did you know that the coffee ceremony is a daily social ritual that brings families together? It's not just about the caffeine - it's about connection, tradition, and taking time to appreciate the moment. 

This is exactly the kind of cultural richness I love celebrating. Our heritage isn't just history - it's alive in every cup we share! 

Who else has experienced an Ethiopian coffee ceremony? Drop a comment! 👇

#EthiopianCoffee #CoffeeCulture #EthiopianTradition #CulturalHeritage #CoffeeLovers #AddisAbaba #EthiopianPride",
  "character_count": 478,
  "hashtags_used": 7,
  "estimated_engagement_score": 0.84,
  "platform_compliance": true
}
```

**MCP Dependencies:**
- LLM MCP (Claude/Gemini) for text generation
- Weaviate MCP (for persona retrieval and past successful posts)

**Status:** Interface defined, implementation pending

---

### 4.3 Skill: Image Creator (GENERATION)

**ID:** `image_creator`  
**Priority:** HIGH  
**Functional Requirement:** FR-AGENT-002  

**Input:**
```json
{
  "prompt": "Young Ethiopian woman wearing traditional jewelry with modern streetwear, vibrant Addis Ababa street scene",
  "character_reference_id": "ideogram_char_ref_ayana_v1",
  "style": "photorealistic",
  "aspect_ratio": "1:1",
  "platform": "instagram"
}
```

**Output:**
```json
{
  "image_url": "https://ideogram.ai/assets/generation_xyz.png",
  "similarity_score": 0.97,
  "generation_time_ms": 4200,
  "cost_usd": 0.05,
  "metadata": {
    "model": "ideogram-v2",
    "seed": 42,
    "safety_check": "passed"
  }
}
```

**MCP Dependencies:**
- Ideogram MCP (required) for character-consistent generation
- Vision MCP (required) for similarity validation

**Status:** Interface defined, implementation pending

---

### 4.4 Skill: Social Publisher (ENGAGEMENT)

**ID:** `social_publisher`  
**Priority:** HIGH  
**Functional Requirement:** FR-AGENT-003  

**Input:**
```json
{
  "platforms": ["twitter", "instagram"],
  "content": {
    "text": "Caption text here...",
    "media_urls": ["https://example.com/image.png"],
    "hashtags": ["EthiopianFashion"]
  },
  "agent_id": "chimera_fashion_eth_001",
  "schedule_time": null,
  "ai_disclosure": true
}
```

**Output:**
```json
{
  "publications": [
    {
      "platform": "twitter",
      "post_id": "1234567890",
      "url": "https://twitter.com/ayana_eth/status/1234567890",
      "published_at": "2026-02-05T16:30:00Z",
      "status": "success"
    },
    {
      "platform": "instagram",
      "post_id": "ABC123XYZ",
      "url": "https://instagram.com/p/ABC123XYZ",
      "published_at": "2026-02-05T16:30:05Z",
      "status": "success"
    }
  ],
  "total_cost_usd": 0.0
}
```

**MCP Dependencies:**
- Twitter MCP (required)
- Instagram MCP (required)
- Platform-specific MCP servers as needed

**Status:** Interface defined, implementation pending

---

### 4.5 Skill: Comment Replier (ENGAGEMENT)

**ID:** `comment_replier`  
**Priority:** MEDIUM  
**Functional Requirement:** FR-AGENT-004  

**Input:**
```json
{
  "comment_id": "comment_xyz",
  "comment_text": "Love your style! Where did you get that jacket?",
  "comment_author": "@fashionlover",
  "post_context": "Post about Ethiopian streetwear",
  "persona_id": "chimera_fashion_eth_001",
  "max_length": 280
}
```

**Output:**
```json
{
  "reply_text": "Thank you! 🙏 It's from a local Addis designer - @designername. Supporting our Ethiopian creators is everything! 💚💛❤️",
  "sentiment": "positive",
  "confidence_score": 0.88,
  "requires_human_review": false
}
```

**MCP Dependencies:**
- LLM MCP for reply generation
- Sentiment analysis MCP (optional)
- Weaviate MCP for context retrieval

**Status:** Interface defined, implementation pending

---

### 4.6 Skill: Wallet Manager (COMMERCE)

**ID:** `wallet_manager`  
**Priority:** MEDIUM  
**Functional Requirement:** FR-AGENT-005  

**Input:**
```json
{
  "action": "check_balance",
  "agent_id": "chimera_fashion_eth_001"
}
```

**Output:**
```json
{
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "balances": [
    {
      "token": "ETH",
      "amount": "0.5",
      "value_usd": 1250.00
    },
    {
      "token": "USDC",
      "amount": "500",
      "value_usd": 500.00
    }
  ],
  "total_value_usd": 1750.00,
  "last_updated": "2026-02-05T16:00:00Z"
}
```

**MCP Dependencies:**
- Coinbase AgentKit MCP (required)

**Status:** Interface defined, implementation pending

---

## 5. Skill Development Workflow

### How to Create a New Skill:

**Step 1: Define the skill.yaml**
```bash
mkdir -p skills/category/skill_name
touch skills/category/skill_name/skill.yaml
```

**Step 2: Write the skill interface (skill.py)**
```python
# Follow the interface contract from Section 3.3
```

**Step 3: Write failing tests**
```python
# skills/category/skill_name/tests/test_skill.py

async def test_skill_executes_successfully():
    """Test that skill can execute with valid input."""
    # This should FAIL initially (TDD)
    skill = create_skill(mock_mcp_client)
    result = await skill.execute(valid_input)
    assert result.some_field == expected_value
```

**Step 4: Implement the skill**
```python
# Fill in the execute() method logic
```

**Step 5: Verify tests pass**
```bash
pytest skills/category/skill_name/tests/
```

**Step 6: Document in README.md**
```markdown
# Usage examples, edge cases, troubleshooting
```

---

## 6. Skill Registry

The Orchestrator maintains a registry of available skills:

```python
# src/orchestrator/skill_registry.py

from typing import Dict, Any
import yaml
from pathlib import Path

class SkillRegistry:
    """Central registry of all available skills."""
    
    def __init__(self):
        self.skills: Dict[str, Any] = {}
        self._load_skills()
    
    def _load_skills(self):
        """Scan skills/ directory and load all skill.yaml files."""
        skills_dir = Path("skills")
        
        for skill_yaml in skills_dir.rglob("skill.yaml"):
            with open(skill_yaml) as f:
                skill_metadata = yaml.safe_load(f)
                self.skills[skill_metadata["id"]] = {
                    "metadata": skill_metadata,
                    "path": skill_yaml.parent
                }
    
    def get_skill(self, skill_id: str) -> Dict[str, Any]:
        """Retrieve skill metadata by ID."""
        return self.skills.get(skill_id)
    
    def list_skills(self, category: str = None) -> list[str]:
        """List all available skills, optionally filtered by category."""
        if category:
            return [
                skill_id for skill_id, data in self.skills.items()
                if data["metadata"]["category"] == category
            ]
        return list(self.skills.keys())
```

---

## 7. Skill Orchestration in Swarm

### How Workers Use Skills:

```python
# src/swarm/worker.py

from src.orchestrator.skill_registry import SkillRegistry
import importlib

class Worker:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.skill_registry = SkillRegistry()
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute a task using the appropriate skill."""
        
        # Map task_type to skill_id
        skill_mapping = {
            "analyze_trend": "trend_detector",
            "generate_caption": "caption_writer",
            "create_image": "image_creator",
            "reply_comment": "comment_replier"
        }
        
        skill_id = skill_mapping.get(task.task_type)
        
        if not skill_id:
            raise ValueError(f"No skill mapped for task type: {task.task_type}")
        
        # Load skill dynamically
        skill_metadata = self.skill_registry.get_skill(skill_id)
        skill_path = skill_metadata["path"]
        
        # Import skill module
        spec = importlib.util.spec_from_file_location(
            skill_id,
            skill_path / "skill.py"
        )
        skill_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(skill_module)
        
        # Create skill instance
        skill = skill_module.create_skill(self.mcp_client)
        
        # Execute skill
        result = await skill.execute(task.context)
        
        return AgentResult(
            task_id=task.task_id,
            worker_id=self.worker_id,
            status="success",
            artifact=result.dict()
        )
```

---

## 8. Testing Strategy for Skills

### Unit Tests (Isolated):
```python
# Test skill logic with mocked MCP responses
async def test_trend_detector_filters_by_relevance():
    mock_mcp = create_mock_mcp_client()
    skill = TrendDetectorSkill(mock_mcp)
    
    result = await skill.execute(TrendDetectorInput(
        niche="fashion",
        min_relevance=0.80
    ))
    
    assert all(trend.relevance_score >= 0.80 for trend in result.trends)
```

### Integration Tests (With Real MCP):
```python
# Test skill with actual MCP server (in test environment)
async def test_trend_detector_with_real_news_mcp():
    real_mcp = connect_to_mcp(mcp_config_test)
    skill = TrendDetectorSkill(real_mcp)
    
    result = await skill.execute(TrendDetectorInput(niche="technology"))
    
    assert len(result.trends) > 0
    assert result.retrieved_at is not None
```

---

## 9. Skill Versioning & Updates

### Semantic Versioning:
- **MAJOR:** Breaking changes to input/output schema
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes

### Example:
```yaml
# skill.yaml
id: trend_detector
version: 2.1.0  # MAJOR.MINOR.PATCH

changelog:
  - version: 2.1.0
    date: "2026-03-01"
    changes:
      - "Added support for Reddit as trend source"
  - version: 2.0.0
    date: "2026-02-15"
    changes:
      - "BREAKING: Changed output schema to include sentiment"
  - version: 1.0.0
    date: "2026-02-05"
    changes:
      - "Initial release"
```

---

## 10. Future Skill Ideas (Out of Scope for Phase 1)

- **Video Editor Skill:** Automated video editing and captioning
- **Collaboration Broker:** Finds and negotiates with other agents
- **A/B Tester:** Runs content experiments automatically
- **Analytics Reporter:** Generates performance reports
- **Skill Installer:** Downloads and installs new skills from agent network

---



---
**Document Control:**
- **Created:** February 5, 2026
- **Status:** Complete - Skills Architecture
- **Next Steps:** Implement skill skeletons, then move to Task 3 (Testing & Infrastructure)
- **Owner:** Project Lead
