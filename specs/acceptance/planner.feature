Feature: Planner task decomposition
  As a Planner Agent
  I want to decompose campaign goals into atomic tasks
  So that Workers can execute them in parallel and traceably

  Background:
    Given a campaign "Promote sustainable fashion event" with budget 50.00

  Scenario: Decompose simple campaign goal into tasks
    When the Planner receives the campaign goal
    Then it creates one or more tasks
    And each task MUST have a unique task_id
    And each task MUST include task_type, priority, context
    And tasks are pushed to Redis key "agent:{{agent_id}}:tasks"

  Scenario: Planner enforces budget constraints
    Given daily_spend 40.00 and daily_budget 50.00
    When Planner proposes an expensive task costing 11.00
    Then Planner must reject the task or lower estimated_cost_usd
    And Planner logs "BudgetExceeded" event
