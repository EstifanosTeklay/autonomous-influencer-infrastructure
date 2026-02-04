"""
Test Suite for Planner Agent

Tests the Planner's ability to decompose high-level campaign goals
into atomic, executable tasks.

Functional Requirement: FR-SWARM-001
Status: FAILING (TDD approach - implement Planner to make these pass)
"""

import pytest
from datetime import datetime
from uuid import UUID


# THESE IMPORTS WILL FAIL - That's expected! (TDD)
# We haven't implemented these modules yet
try:
    from src.swarm.planner import PlannerAgent
    from src.schemas.task import AgentTask
except ImportError:
    # This will fail initially - that's the point of TDD!
    pass


class TestPlannerTaskDecomposition:
    """Test Planner's core task decomposition capability."""
    
    @pytest.mark.asyncio
    async def test_planner_creates_tasks_from_simple_goal(self):
        """
        FR-SWARM-001: Planner should decompose a simple goal into tasks.
        
        Given: A simple campaign goal
        When: Planner decomposes the goal
        Then: Multiple atomic tasks are created with correct structure
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Create 3 posts about Ethiopian coffee culture"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        assert len(tasks) >= 3, "Should create at least 3 tasks"
        assert all(isinstance(task, AgentTask) for task in tasks), \
            "All returned items should be AgentTask objects"
        assert all(task.task_id is not None for task in tasks), \
            "Each task must have a unique task_id"
    
    @pytest.mark.asyncio
    async def test_planner_assigns_correct_task_types(self):
        """
        FR-SWARM-001: Tasks should have appropriate task_type values.
        
        Given: A content creation goal
        When: Planner decomposes it
        Then: Task types match the required work (caption, image, etc.)
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Create an Instagram post with image and caption about fashion"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        task_types = [task.task_type for task in tasks]
        assert "generate_caption" in task_types, \
            "Should include caption generation task"
        assert "create_image" in task_types, \
            "Should include image creation task"
    
    @pytest.mark.asyncio
    async def test_planner_sets_priority_levels(self):
        """
        FR-SWARM-001: Tasks should have appropriate priority levels.
        
        Given: A goal with urgent and non-urgent components
        When: Planner decomposes it
        Then: Priorities are assigned correctly
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "URGENT: Respond to trending topic about sustainable fashion"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        priorities = [task.priority for task in tasks]
        assert "high" in priorities, \
            "Urgent goals should create high-priority tasks"
        assert all(p in ["high", "medium", "low"] for p in priorities), \
            "All priorities must be valid values"
    
    @pytest.mark.asyncio
    async def test_planner_includes_required_context(self):
        """
        FR-SWARM-001: Each task must include context for execution.
        
        Given: A campaign goal
        When: Planner creates tasks
        Then: Each task has complete context dictionary
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Create post about Ethiopian coffee with Gen-Z tone"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        for task in tasks:
            assert "goal_description" in task.context, \
                "Context must include goal description"
            assert task.context["goal_description"] is not None, \
                "Goal description should not be empty"
    
    @pytest.mark.asyncio
    async def test_planner_generates_unique_task_ids(self):
        """
        FR-SWARM-001: Each task must have a unique UUID.
        
        Given: Any goal
        When: Planner creates tasks
        Then: All task_ids are unique UUIDs
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Create 5 different posts"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        task_ids = [task.task_id for task in tasks]
        assert len(task_ids) == len(set(task_ids)), \
            "All task IDs must be unique"
        assert all(isinstance(task_id, UUID) for task_id in task_ids), \
            "All task IDs must be valid UUIDs"


class TestPlannerBudgetAwareness:
    """Test Planner's budget checking capabilities."""
    
    @pytest.mark.asyncio
    async def test_planner_estimates_task_costs(self):
        """
        FR-SWARM-001 + Budget constraint: Tasks should have cost estimates.
        
        Given: A goal that requires expensive operations
        When: Planner creates tasks
        Then: Each task includes cost estimate
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Create a video about Ethiopian fashion"
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        video_tasks = [t for t in tasks if t.task_type == "create_video"]
        if video_tasks:
            assert video_tasks[0].estimated_cost_usd > 0, \
                "Video generation should have non-zero cost estimate"
    
    @pytest.mark.asyncio
    async def test_planner_respects_budget_limits(self):
        """
        Budget constraint: Planner should not exceed daily budget.
        
        Given: A planner with limited budget
        When: A goal would exceed the budget
        Then: Planner should reduce scope or reject
        """
        # Arrange
        planner = PlannerAgent(
            agent_id="test_agent_001",
            daily_budget_usd=5.00  # Low budget
        )
        goal = "Create 100 high-quality videos"  # Expensive goal
        
        # Act & Assert
        # Either: Planner reduces scope
        tasks = await planner.decompose_goal(goal)
        total_cost = sum(t.estimated_cost_usd for t in tasks)
        assert total_cost <= 5.00, \
            "Total estimated cost should not exceed budget"
        
        # OR: Planner raises BudgetExceededError
        # (Implementation decides which approach)


class TestPlannerQueueManagement:
    """Test Planner's interaction with Redis task queue."""
    
    @pytest.mark.asyncio
    async def test_planner_pushes_tasks_to_queue(self, mock_redis):
        """
        FR-SWARM-001: Tasks should be pushed to Redis queue.
        
        Given: A planner connected to Redis
        When: Tasks are created
        Then: Tasks are pushed to the correct queue
        """
        # Arrange
        planner = PlannerAgent(
            agent_id="test_agent_001",
            redis_client=mock_redis
        )
        goal = "Create 2 posts"
        
        # Act
        await planner.decompose_and_queue(goal)
        
        # Assert
        queue_name = "agent:test_agent_001:tasks"
        assert mock_redis.llen(queue_name) >= 2, \
            "At least 2 tasks should be in queue"
    
    @pytest.mark.asyncio
    async def test_planner_monitors_queue_depth(self, mock_redis):
        """
        FR-SWARM-001: Planner should pause if queue has >100 tasks.
        
        Given: A queue with many pending tasks
        When: Planner tries to add more tasks
        Then: Planner should pause or reject
        """
        # Arrange
        planner = PlannerAgent(
            agent_id="test_agent_001",
            redis_client=mock_redis
        )
        
        # Simulate queue with 101 tasks
        queue_name = "agent:test_agent_001:tasks"
        for i in range(101):
            mock_redis.rpush(queue_name, f"task_{i}")
        
        goal = "Create more posts"
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await planner.decompose_and_queue(goal)
        
        assert "queue" in str(exc_info.value).lower() or \
               "capacity" in str(exc_info.value).lower(), \
            "Should raise error about queue capacity"


class TestPlannerErrorHandling:
    """Test Planner's error handling and edge cases."""
    
    @pytest.mark.asyncio
    async def test_planner_handles_empty_goal(self):
        """
        Edge case: Planner should handle empty or invalid goals.
        
        Given: An empty goal string
        When: Planner tries to decompose it
        Then: Planner should raise ValidationError
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        
        # Act & Assert
        with pytest.raises(ValueError):
            await planner.decompose_goal("")
    
    @pytest.mark.asyncio
    async def test_planner_handles_vague_goal(self):
        """
        Edge case: Planner should handle vague goals.
        
        Given: A vague, ambiguous goal
        When: Planner tries to decompose it
        Then: Planner should create at least one task or ask for clarification
        """
        # Arrange
        planner = PlannerAgent(agent_id="test_agent_001")
        goal = "Do something"  # Very vague
        
        # Act
        tasks = await planner.decompose_goal(goal)
        
        # Assert
        # Minimum viable behavior: create at least 1 task
        assert len(tasks) >= 1, \
            "Even vague goals should produce at least one task"


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def mock_redis():
    """
    Mock Redis client for testing queue operations.
    
    Returns a simple in-memory dict-based mock of Redis.
    """
    class MockRedis:
        def __init__(self):
            self.store = {}
        
        def rpush(self, key, value):
            if key not in self.store:
                self.store[key] = []
            self.store[key].append(value)
            return len(self.store[key])
        
        def lpop(self, key):
            if key in self.store and self.store[key]:
                return self.store[key].pop(0)
            return None
        
        def llen(self, key):
            return len(self.store.get(key, []))
        
        def delete(self, key):
            if key in self.store:
                del self.store[key]
    
    return MockRedis()


# ============================================================================
# EXPECTED TEST RESULTS (all should FAIL initially)
# ============================================================================
"""
When you run: pytest tests/functional/test_planner.py

Expected output:
================= FAILURES =================
test_planner_creates_tasks_from_simple_goal - ImportError: No module named 'src.swarm.planner'
test_planner_assigns_correct_task_types - ImportError: No module named 'src.swarm.planner'
test_planner_sets_priority_levels - ImportError: No module named 'src.swarm.planner'
... (all tests fail)

This is CORRECT for TDD!

Next step: Implement src/swarm/planner.py to make these tests pass.
"""
