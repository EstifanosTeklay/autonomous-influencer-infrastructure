"""
Caption Writer Skill

Generates persona-consistent social media captions for various platforms.

Functional Requirement: FR-AGENT-002
"""

from typing import Any, Literal
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger()


class CaptionWriterInput(BaseModel):
    """Input parameters for Caption Writer skill."""
    
    topic: str = Field(
        description="Main subject of the post",
        examples=["Ethiopian coffee culture", "sustainable fashion trends"]
    )
    persona_id: str = Field(
        description="Agent persona ID (loads from SOUL.md)",
        examples=["chimera_fashion_eth_001"]
    )
    platform: Literal["twitter", "instagram", "tiktok", "linkedin"] = Field(
        description="Target social media platform"
    )
    tone: Literal["excited", "professional", "casual", "empowering", "educational"] = Field(
        default="casual",
        description="Desired tone of the caption"
    )
    max_length: int = Field(
        default=2200,
        gt=0,
        description="Maximum character count (platform-specific)"
    )
    include_hashtags: bool = Field(
        default=True,
        description="Whether to include hashtags"
    )
    include_call_to_action: bool = Field(
        default=True,
        description="Whether to include CTA (e.g., 'Comment below!')"
    )


class CaptionWriterOutput(BaseModel):
    """Output from Caption Writer skill."""
    
    caption: str = Field(description="Generated caption text")
    character_count: int = Field(description="Total character count")
    hashtags_used: int = Field(default=0, description="Number of hashtags included")
    estimated_engagement_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Predicted engagement potential (0.0-1.0)"
    )
    platform_compliance: bool = Field(
        description="Whether caption meets platform requirements"
    )


class CaptionWriterSkill:
    """
    Generates persona-consistent social media captions.
    
    This skill:
    - Loads agent persona from SOUL.md
    - Retrieves successful past posts from memory
    - Generates caption using LLM with persona constraints
    - Validates platform-specific requirements
    - Estimates engagement potential
    
    Attributes:
        mcp_client: Connected MCP client
        skill_id: Unique identifier for this skill
        version: Semantic version
    """
    
    def __init__(self, mcp_client: Any):
        """
        Initialize skill with MCP client.
        
        Args:
            mcp_client: Connected MCP client for LLM and memory access
        """
        self.mcp_client = mcp_client
        self.skill_id = "caption_writer"
        self.version = "1.0.0"
    
    async def execute(self, input_data: CaptionWriterInput) -> CaptionWriterOutput:
        """
        Main execution method for caption generation.
        
        Workflow:
        1. Load persona from SOUL.md via Weaviate
        2. Retrieve similar successful posts from memory
        3. Build LLM prompt with constraints
        4. Generate caption
        5. Validate platform requirements
        6. Estimate engagement score
        
        Args:
            input_data: Validated input parameters
        
        Returns:
            Generated caption with metadata
        
        Raises:
            PersonaNotFoundError: If persona_id doesn't exist
            LLMError: If caption generation fails
            ValidationError: If output doesn't meet requirements
        """
        logger.info(
            "skill_execution_started",
            skill_id=self.skill_id,
            persona_id=input_data.persona_id,
            topic=input_data.topic,
            platform=input_data.platform
        )
        
        try:
            # Step 1: Load persona (PLACEHOLDER)
            # TODO: Implement persona loading from Weaviate
            # persona = await self._load_persona(input_data.persona_id)
            
            # Step 2: Retrieve past successful posts (PLACEHOLDER)
            # TODO: Query Weaviate for similar high-engagement posts
            # past_posts = await self._get_similar_posts(input_data.topic, input_data.persona_id)
            
            # Step 3: Build LLM prompt (PLACEHOLDER)
            # TODO: Construct prompt with persona voice, tone, constraints
            # prompt = self._build_prompt(persona, input_data, past_posts)
            
            # Step 4: Generate caption (PLACEHOLDER)
            # TODO: Call LLM MCP server
            # raw_caption = await self.mcp_client.call_tool("llm.generate", {"prompt": prompt})
            
            # MOCK OUTPUT for now
            mock_caption = self._generate_mock_caption(input_data)
            
            # Step 5: Validate platform requirements
            platform_compliance = self._validate_platform(
                mock_caption,
                input_data.platform,
                input_data.max_length
            )
            
            # Step 6: Estimate engagement
            engagement_score = self._estimate_engagement(mock_caption, input_data.platform)
            
            # Count hashtags
            hashtag_count = mock_caption.count('#')
            
            logger.info(
                "skill_execution_completed",
                skill_id=self.skill_id,
                character_count=len(mock_caption),
                hashtags_used=hashtag_count,
                platform_compliance=platform_compliance
            )
            
            return CaptionWriterOutput(
                caption=mock_caption,
                character_count=len(mock_caption),
                hashtags_used=hashtag_count,
                estimated_engagement_score=engagement_score,
                platform_compliance=platform_compliance
            )
            
        except Exception as e:
            logger.error(
                "skill_execution_failed",
                skill_id=self.skill_id,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def _generate_mock_caption(self, input_data: CaptionWriterInput) -> str:
        """Generate mock caption for testing (TEMPORARY)."""
        base_caption = f"Exploring the amazing world of {input_data.topic}! "
        
        if input_data.tone == "excited":
            base_caption += "This is so incredible! ✨🔥 "
        elif input_data.tone == "professional":
            base_caption += "Here's what you need to know. "
        
        if input_data.include_call_to_action:
            base_caption += "What do you think? Drop a comment! 👇 "
        
        if input_data.include_hashtags:
            topic_words = input_data.topic.replace(" ", "")
            base_caption += f"#{topic_words} #ContentCreation #Trending"
        
        return base_caption[:input_data.max_length]
    
    def _validate_platform(
        self,
        caption: str,
        platform: str,
        max_length: int
    ) -> bool:
        """Check if caption meets platform requirements."""
        platform_limits = {
            "twitter": 280,
            "instagram": 2200,
            "tiktok": 2200,
            "linkedin": 3000
        }
        
        actual_limit = min(max_length, platform_limits.get(platform, 2200))
        return len(caption) <= actual_limit
    
    def _estimate_engagement(self, caption: str, platform: str) -> float:
        """Estimate engagement potential (PLACEHOLDER)."""
        # TODO: Use ML model or historical data
        # For now, simple heuristic
        score = 0.5  # Base score
        
        if '#' in caption:
            score += 0.1  # Hashtags help
        if '?' in caption:
            score += 0.1  # Questions engage
        if any(emoji in caption for emoji in ['✨', '🔥', '💚', '❤️']):
            score += 0.15  # Emojis increase engagement
        
        return min(score, 1.0)


def create_skill(mcp_client: Any) -> CaptionWriterSkill:
    """
    Factory function to create skill instance.
    
    Args:
        mcp_client: Connected MCP client
    
    Returns:
        Initialized CaptionWriterSkill instance
    """
    return CaptionWriterSkill(mcp_client)
