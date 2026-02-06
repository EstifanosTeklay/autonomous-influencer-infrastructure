Feature: Worker execution and review
  As a Worker Agent
  I want to pop tasks and produce artifacts
  So that Judges can validate quality before publish

  Scenario: Worker pops a pending task and executes
    Given a task exists on Redis key "agent:chimera_fashion_eth_001:tasks"
    When Worker BRPOP the queue
    Then Worker sets task.status to "in_progress"
    And Worker produces an AgentResult with artifact and confidence_score
    And Worker pushes result to Redis key "agent:chimera_fashion_eth_001:review"

  Scenario: Worker is stateless across restarts
    Given Worker was processing a task and crashes
    When Worker restarts
    Then new Worker can continue processing other tasks without global state loss
