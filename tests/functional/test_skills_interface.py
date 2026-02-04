"""
Test Suite for Skills Interface

Tests that all skills follow the standardized interface contract.
Ensures skills can be loaded and executed by the Worker agent.

Technical Requirement: skills/README.md Section 3 (Skill Interface Contract)
Status: FAILING (implement skills to make these pass)
"""

import pytest
from pathlib import Path
import yaml


# THESE IMPORTS WILL FAIL - That's expected! (TDD)
try:
    from skills.perception.trend_detector.skill import create_skill as create_trend_detector
    from skills.generation.caption_writer.skill import create_skill as create_caption_writer
    from skills.engagement.social_publisher.skill import create_skill as create_social_publisher
except ImportError:
    pass


class TestSkillInterface:
    """Test that all skills implement the required interface."""
    
    @pytest.mark.parametrize("skill_path,skill_id", [
        ("skills/perception/trend_detector", "trend_detector"),
        ("skills/generation/caption_writer", "caption_writer"),
        ("skills/engagement/social_publisher", "social_publisher"),
    ])
    def test_skill_has_yaml_metadata(self, skill_path, skill_id):
        """
        Interface contract: Every skill must have skill.yaml metadata file.
        
        Given: A skill directory
        When: Looking for skill.yaml
        Then: File exists and is valid YAML
        """
        # Arrange
        yaml_path = Path(skill_path) / "skill.yaml"
        
        # Act & Assert
        assert yaml_path.exists(), f"Missing skill.yaml in {skill_path}"
        
        with open(yaml_path) as f:
            metadata = yaml.safe_load(f)
        
        assert metadata["id"] == skill_id, \
            f"Skill ID in YAML should be {skill_id}"
        assert "version" in metadata, "Missing version field"
        assert "name" in metadata, "Missing name field"
        assert "description" in metadata, "Missing description field"
    
    @pytest.mark.parametrize("skill_path", [
        "skills/perception/trend_detector",
        "skills/generation/caption_writer",
        "skills/engagement/social_publisher",
    ])
    def test_skill_has_implementation_file(self, skill_path):
        """
        Interface contract: Every skill must have skill.py implementation.
        
        Given: A skill directory
        When: Looking for skill.py
        Then: File exists
        """
        # Arrange
        py_path = Path(skill_path) / "skill.py"
        
        # Act & Assert
        assert py_path.exists(), f"Missing skill.py in {skill_path}"
    
    @pytest.mark.parametrize("skill_path", [
        "skills/perception/trend_detector",
        "skills/generation/caption_writer",
        "skills/engagement/social_publisher",
    ])
    def test_skill_has_tests_directory(self, skill_path):
        """
        Interface contract: Every skill should have tests/ directory.
        
        Given: A skill directory
        When: Looking for tests/
        Then: Directory exists
        """
        # Arrange
        tests_path = Path(skill_path) / "tests"
        
        # Act & Assert
        assert tests_path.exists(), f"Missing tests/ directory in {skill_path}"
        assert tests_path.is_dir(), f"tests/ should be a directory in {skill_path}"


class TestSkillMetadataSchema:
    """Test that skill.yaml files follow the required schema."""
    
    def test_trend_detector_yaml_schema(self):
        """
        Metadata schema: trend_detector skill.yaml has all required fields.
        
        Given: trend_detector skill.yaml
        When: Parsing metadata
        Then: All required fields are present
        """
        # Arrange
        yaml_path = Path("skills/perception/trend_detector/skill.yaml")
        
        # Act
        with open(yaml_path) as f:
            metadata = yaml.safe_load(f)
        
        # Assert - Required top-level fields
        assert metadata["id"] == "trend_detector"
        assert metadata["version"]
        assert metadata["category"] == "perception"
        
        # Assert - Schema fields
        assert "input_schema" in metadata
        assert "output_schema" in metadata
        assert "mcp_servers" in metadata
        assert "resources" in metadata
        assert "constraints" in metadata
        
        # Assert - Input schema structure
        assert metadata["input_schema"]["type"] == "object"
        assert "properties" in metadata["input_schema"]
        
        # Assert - MCP dependencies
        assert "required" in metadata["mcp_servers"]
        assert isinstance(metadata["mcp_servers"]["required"], list)


class TestSkillFactoryFunction:
    """Test that skills provide the create_skill() factory function."""
    
    @pytest.mark.asyncio
    async def test_trend_detector_has_factory_function(self, mock_mcp_client):
        """
        Interface contract: Skill must have create_skill() factory.
        
        Given: trend_detector module
        When: Calling create_skill()
        Then: Skill instance is returned
        """
        # Act
        skill = create_trend_detector(mock_mcp_client)
        
        # Assert
        assert skill is not None
        assert hasattr(skill, "execute"), "Skill must have execute() method"
        assert hasattr(skill, "skill_id"), "Skill must have skill_id attribute"
        assert hasattr(skill, "version"), "Skill must have version attribute"
    
    @pytest.mark.asyncio
    async def test_caption_writer_has_factory_function(self, mock_mcp_client):
        """
        Interface contract: Skill must have create_skill() factory.
        
        Given: caption_writer module
        When: Calling create_skill()
        Then: Skill instance is returned
        """
        # Act
        skill = create_caption_writer(mock_mcp_client)
        
        # Assert
        assert skill is not None
        assert hasattr(skill, "execute")
        assert skill.skill_id == "caption_writer"
    
    @pytest.mark.asyncio
    async def test_social_publisher_has_factory_function(self, mock_mcp_client):
        """
        Interface contract: Skill must have create_skill() factory.
        
        Given: social_publisher module
        When: Calling create_skill()
        Then: Skill instance is returned
        """
        # Act
        skill = create_social_publisher(mock_mcp_client)
        
        # Assert
        assert skill is not None
        assert hasattr(skill, "execute")
        assert skill.skill_id == "social_publisher"


class TestSkillExecutionInterface:
    """Test that skills implement the execute() method correctly."""
    
    @pytest.mark.asyncio
    async def test_trend_detector_execute_method(self, mock_mcp_client):
        """
        Interface contract: execute() must accept input and return output.
        
        Given: trend_detector skill
        When: Calling execute() with valid input
        Then: Output is returned (or error is raised)
        """
        # Arrange
        skill = create_trend_detector(mock_mcp_client)
        
        # Mock input based on skill.yaml
        from skills.perception.trend_detector.skill import TrendDetectorInput
        input_data = TrendDetectorInput(
            niche="fashion",
            time_window="24h",
            min_relevance=0.75
        )
        
        # Act
        result = await skill.execute(input_data)
        
        # Assert
        assert result is not None, "execute() should return output"
        assert hasattr(result, "trends"), "Output should have 'trends' field"
        assert hasattr(result, "retrieved_at"), "Output should have 'retrieved_at' field"
    
    @pytest.mark.asyncio
    async def test_caption_writer_execute_method(self, mock_mcp_client):
        """
        Interface contract: execute() must accept input and return output.
        
        Given: caption_writer skill
        When: Calling execute() with valid input
        Then: Output is returned
        """
        # Arrange
        skill = create_caption_writer(mock_mcp_client)
        
        from skills.generation.caption_writer.skill import CaptionWriterInput
        input_data = CaptionWriterInput(
            topic="Ethiopian coffee",
            persona_id="test_agent",
            platform="instagram"
        )
        
        # Act
        result = await skill.execute(input_data)
        
        # Assert
        assert result is not None
        assert hasattr(result, "caption"), "Output should have 'caption' field"
        assert hasattr(result, "character_count")
        assert isinstance(result.caption, str), "Caption should be string"


class TestSkillInputValidation:
    """Test that skills validate input correctly."""
    
    @pytest.mark.asyncio
    async def test_trend_detector_rejects_invalid_time_window(self, mock_mcp_client):
        """
        Input validation: Skill should reject invalid time_window.
        
        Given: trend_detector skill
        When: Providing invalid time_window value
        Then: ValidationError is raised
        """
        # Arrange
        skill = create_trend_detector(mock_mcp_client)
        
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            from skills.perception.trend_detector.skill import TrendDetectorInput
            TrendDetectorInput(
                niche="fashion",
                time_window="invalid",  # Not in allowed enum
                min_relevance=0.75
            )
    
    @pytest.mark.asyncio
    async def test_caption_writer_rejects_invalid_platform(self, mock_mcp_client):
        """
        Input validation: Skill should reject invalid platform.
        
        Given: caption_writer skill
        When: Providing invalid platform value
        Then: ValidationError is raised
        """
        # Arrange
        skill = create_caption_writer(mock_mcp_client)
        
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            from skills.generation.caption_writer.skill import CaptionWriterInput
            CaptionWriterInput(
                topic="Test",
                persona_id="test",
                platform="myspace"  # Not in allowed enum
            )


class TestSkillRegistry:
    """Test the SkillRegistry can load and manage skills."""
    
    def test_skill_registry_loads_all_skills(self):
        """
        Registry: SkillRegistry should discover all skills.
        
        Given: skills/ directory with multiple skills
        When: Initializing SkillRegistry
        Then: All skills are loaded
        """
        # Import will fail initially (TDD)
        from src.orchestrator.skill_registry import SkillRegistry
        
        # Act
        registry = SkillRegistry()
        
        # Assert
        assert "trend_detector" in registry.skills
        assert "caption_writer" in registry.skills
        assert "social_publisher" in registry.skills
    
    def test_skill_registry_get_skill(self):
        """
        Registry: Should retrieve skill metadata by ID.
        
        Given: Initialized SkillRegistry
        When: Getting skill by ID
        Then: Metadata is returned
        """
        # Arrange
        from src.orchestrator.skill_registry import SkillRegistry
        registry = SkillRegistry()
        
        # Act
        skill_metadata = registry.get_skill("trend_detector")
        
        # Assert
        assert skill_metadata is not None
        assert skill_metadata["metadata"]["id"] == "trend_detector"
        assert "path" in skill_metadata
    
    def test_skill_registry_list_by_category(self):
        """
        Registry: Should list skills filtered by category.
        
        Given: Initialized SkillRegistry
        When: Listing skills in 'perception' category
        Then: Only perception skills are returned
        """
        # Arrange
        from src.orchestrator.skill_registry import SkillRegistry
        registry = SkillRegistry()
        
        # Act
        perception_skills = registry.list_skills(category="perception")
        
        # Assert
        assert "trend_detector" in perception_skills
        assert "caption_writer" not in perception_skills


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def mock_mcp_client():
    """
    Mock MCP client for testing skills without real MCP servers.
    """
    class MockMCPClient:
        async def read_resource(self, uri: str):
            """Mock read_resource method."""
            return {
                "articles": [
                    {
                        "title": "Mock trending article",
                        "relevance": 0.85,
                        "source": "Mock Source",
                        "url": "https://example.com/mock"
                    }
                ]
            }
        
        async def call_tool(self, tool_name: str, arguments: dict):
            """Mock call_tool method."""
            return {"status": "success", "result": "Mock result"}
    
    return MockMCPClient()


# ============================================================================
# EXPECTED TEST RESULTS
# ============================================================================
"""
When you run: pytest tests/functional/test_skills_interface.py

Expected output:
================= FAILURES =================
test_skill_has_yaml_metadata - AssertionError: Missing skill.yaml
test_skill_has_implementation_file - AssertionError: Missing skill.py
test_trend_detector_has_factory_function - ImportError
... (many tests fail)

Some tests will PASS (e.g., yaml existence if you copied the files)
Some tests will FAIL (e.g., imports, execute methods)

This is EXPECTED for TDD!

Next step: Ensure skill files exist and implement missing functionality.
"""
