"""
Test Suite for Task Schema

Tests the AgentTask Pydantic model to ensure data validation works correctly.

Technical Requirement: technical.md Section 3.1 (Agent Task Schema)
Status: FAILING (implement src/schemas/task.py to make these pass)
"""

import pytest
from datetime import datetime
from uuid import UUID, uuid4


# THIS IMPORT WILL FAIL - That's expected! (TDD)
try:
    from src.schemas.task import AgentTask
except ImportError:
    pass


class TestAgentTaskSchema:
    """Test basic AgentTask creation and validation."""
    
    def test_task_creation_with_minimal_fields(self):
        """
        Schema validation: Should create task with only required fields.
        
        Given: Minimal valid task data
        When: Creating AgentTask instance
        Then: Task is created with default values
        """
        # Arrange & Act
        task = AgentTask(
            task_type="generate_caption",
            context={"goal_description": "Test goal"}
        )
        
        # Assert
        assert task.task_type == "generate_caption"
        assert task.priority == "medium", "Default priority should be 'medium'"
        assert task.status == "pending", "Default status should be 'pending'"
        assert isinstance(task.task_id, UUID), "task_id should be auto-generated UUID"
        assert isinstance(task.created_at, datetime), "created_at should be auto-generated"
    
    def test_task_creation_with_all_fields(self):
        """
        Schema validation: Should accept all optional fields.
        
        Given: Complete task data with all fields
        When: Creating AgentTask instance
        Then: All fields are set correctly
        """
        # Arrange
        task_id = uuid4()
        now = datetime.utcnow()
        
        # Act
        task = AgentTask(
            task_id=task_id,
            task_type="create_image",
            priority="high",
            context={
                "goal_description": "Create fashion image",
                "persona_id": "chimera_fashion_eth_001"
            },
            assigned_worker_id="worker_123",
            created_at=now,
            status="in_progress",
            retry_count=1,
            max_retries=3,
            estimated_cost_usd=0.05
        )
        
        # Assert
        assert task.task_id == task_id
        assert task.task_type == "create_image"
        assert task.priority == "high"
        assert task.assigned_worker_id == "worker_123"
        assert task.status == "in_progress"
        assert task.retry_count == 1
        assert task.estimated_cost_usd == 0.05
    
    def test_task_type_validation(self):
        """
        Schema validation: task_type must be valid Literal value.
        
        Given: Invalid task_type value
        When: Creating AgentTask instance
        Then: ValidationError is raised
        """
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            AgentTask(
                task_type="invalid_type",  # Not in allowed list
                context={"goal_description": "Test"}
            )
    
    def test_priority_validation(self):
        """
        Schema validation: priority must be 'high', 'medium', or 'low'.
        
        Given: Invalid priority value
        When: Creating AgentTask instance
        Then: ValidationError is raised
        """
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            AgentTask(
                task_type="generate_caption",
                priority="critical",  # Not in allowed list
                context={"goal_description": "Test"}
            )
    
    def test_status_validation(self):
        """
        Schema validation: status must be valid Literal value.
        
        Given: Invalid status value
        When: Creating AgentTask instance
        Then: ValidationError is raised
        """
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            AgentTask(
                task_type="generate_caption",
                status="running",  # Not in allowed list
                context={"goal_description": "Test"}
            )
    
    def test_context_is_required(self):
        """
        Schema validation: context field is required.
        
        Given: Task data without context
        When: Creating AgentTask instance
        Then: ValidationError is raised
        """
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            AgentTask(
                task_type="generate_caption"
                # Missing context field
            )


class TestAgentTaskSerialization:
    """Test AgentTask JSON serialization/deserialization."""
    
    def test_task_to_dict(self):
        """
        Serialization: Should convert task to dictionary.
        
        Given: A valid AgentTask instance
        When: Converting to dict
        Then: All fields are present in dictionary
        """
        # Arrange
        task = AgentTask(
            task_type="generate_caption",
            priority="high",
            context={"goal_description": "Test goal"}
        )
        
        # Act
        task_dict = task.model_dump()  # Pydantic v2
        
        # Assert
        assert "task_id" in task_dict
        assert "task_type" in task_dict
        assert task_dict["task_type"] == "generate_caption"
        assert task_dict["priority"] == "high"
        assert "context" in task_dict
    
    def test_task_to_json(self):
        """
        Serialization: Should convert task to JSON string.
        
        Given: A valid AgentTask instance
        When: Converting to JSON
        Then: Valid JSON string is produced
        """
        # Arrange
        task = AgentTask(
            task_type="create_image",
            context={"prompt": "Ethiopian fashion"}
        )
        
        # Act
        task_json = task.model_dump_json()  # Pydantic v2
        
        # Assert
        assert isinstance(task_json, str)
        assert "task_id" in task_json
        assert "create_image" in task_json
    
    def test_task_from_dict(self):
        """
        Deserialization: Should create task from dictionary.
        
        Given: A valid task dictionary
        When: Creating AgentTask from dict
        Then: Task instance is created correctly
        """
        # Arrange
        task_dict = {
            "task_type": "reply_comment",
            "priority": "low",
            "context": {
                "comment_text": "Nice post!",
                "comment_id": "comment_123"
            },
            "status": "pending"
        }
        
        # Act
        task = AgentTask(**task_dict)
        
        # Assert
        assert task.task_type == "reply_comment"
        assert task.priority == "low"
        assert task.context["comment_text"] == "Nice post!"


class TestAgentTaskBudgetTracking:
    """Test budget-related fields and calculations."""
    
    def test_estimated_cost_defaults_to_zero(self):
        """
        Budget: estimated_cost_usd should default to 0.0.
        
        Given: Task created without cost estimate
        When: Accessing estimated_cost_usd
        Then: Value is 0.0
        """
        # Arrange & Act
        task = AgentTask(
            task_type="generate_caption",
            context={"goal_description": "Test"}
        )
        
        # Assert
        assert task.estimated_cost_usd == 0.0
    
    def test_actual_cost_is_optional(self):
        """
        Budget: actual_cost_usd is None until task completes.
        
        Given: Newly created task
        When: Accessing actual_cost_usd
        Then: Value is None
        """
        # Arrange & Act
        task = AgentTask(
            task_type="create_video",
            context={"prompt": "Fashion video"}
        )
        
        # Assert
        assert task.actual_cost_usd is None
    
    def test_can_set_actual_cost_after_completion(self):
        """
        Budget: actual_cost_usd can be set when task completes.
        
        Given: A completed task
        When: Setting actual_cost_usd
        Then: Value is stored correctly
        """
        # Arrange
        task = AgentTask(
            task_type="create_image",
            context={"prompt": "Test image"}
        )
        
        # Act
        task.actual_cost_usd = 0.05
        task.status = "complete"
        
        # Assert
        assert task.actual_cost_usd == 0.05
        assert task.status == "complete"


class TestAgentTaskRetryLogic:
    """Test retry-related fields."""
    
    def test_retry_count_defaults_to_zero(self):
        """
        Retry logic: retry_count should start at 0.
        
        Given: Newly created task
        When: Accessing retry_count
        Then: Value is 0
        """
        # Arrange & Act
        task = AgentTask(
            task_type="analyze_trend",
            context={"niche": "fashion"}
        )
        
        # Assert
        assert task.retry_count == 0
    
    def test_max_retries_defaults_to_three(self):
        """
        Retry logic: max_retries should default to 3.
        
        Given: Newly created task
        When: Accessing max_retries
        Then: Value is 3
        """
        # Arrange & Act
        task = AgentTask(
            task_type="generate_caption",
            context={"topic": "Test"}
        )
        
        # Assert
        assert task.max_retries == 3
    
    def test_can_increment_retry_count(self):
        """
        Retry logic: retry_count can be incremented.
        
        Given: A task that failed
        When: Incrementing retry_count
        Then: Value increases correctly
        """
        # Arrange
        task = AgentTask(
            task_type="create_image",
            context={"prompt": "Test"}
        )
        
        # Act
        task.retry_count += 1
        
        # Assert
        assert task.retry_count == 1


class TestAgentTaskTimestamps:
    """Test timestamp fields."""
    
    def test_created_at_is_auto_generated(self):
        """
        Timestamps: created_at is set automatically.
        
        Given: Newly created task
        When: Accessing created_at
        Then: Timestamp is close to current time
        """
        # Arrange
        before = datetime.utcnow()
        
        # Act
        task = AgentTask(
            task_type="generate_caption",
            context={"goal": "Test"}
        )
        
        after = datetime.utcnow()
        
        # Assert
        assert before <= task.created_at <= after
    
    def test_started_at_is_initially_none(self):
        """
        Timestamps: started_at is None for pending tasks.
        
        Given: Newly created task
        When: Accessing started_at
        Then: Value is None
        """
        # Arrange & Act
        task = AgentTask(
            task_type="reply_comment",
            context={"comment": "Test"}
        )
        
        # Assert
        assert task.started_at is None
    
    def test_completed_at_is_initially_none(self):
        """
        Timestamps: completed_at is None for incomplete tasks.
        
        Given: Newly created task
        When: Accessing completed_at
        Then: Value is None
        """
        # Arrange & Act
        task = AgentTask(
            task_type="create_video",
            context={"script": "Test"}
        )
        
        # Assert
        assert task.completed_at is None


# ============================================================================
# EXPECTED TEST RESULTS
# ============================================================================
"""
When you run: pytest tests/functional/test_task_schema.py

Expected output:
================= FAILURES =================
test_task_creation_with_minimal_fields - ImportError: No module named 'src.schemas.task'
test_task_creation_with_all_fields - ImportError: No module named 'src.schemas.task'
... (all tests fail with ImportError)

This is CORRECT for TDD!

Next step: Implement src/schemas/task.py according to technical.md specification.
"""
