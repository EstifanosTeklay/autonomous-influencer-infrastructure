Feature: Judge quality validation
  As a Judge Agent
  I want to evaluate Worker results and route them appropriately

  Scenario: Judge approves high confidence result
    Given an AgentResult with confidence_score 0.94
    When Judge evaluates the result
    Then Judge decision is "approve"
    And result is committed to PostgreSQL content_items

  Scenario: Judge escalates medium confidence result
    Given an AgentResult with confidence_score 0.82
    When Judge evaluates the result
    Then Judge decision is "escalate"
    And result is pushed to HITL queue table in PostgreSQL

  Scenario: Judge rejects low confidence result
    Given an AgentResult with confidence_score 0.60
    When Judge evaluates the result
    Then Judge decision is "reject"
    And task is re-queued to Planner
