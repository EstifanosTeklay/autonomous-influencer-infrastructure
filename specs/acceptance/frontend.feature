Feature: Frontend Fleet Dashboard acceptance criteria
  As a Network Operator
  I want a Dashboard to monitor agents, campaigns, and HITL
  So that I can make governance decisions quickly

  Scenario: Dashboard lists active agents
    Given multiple agents in the system
    When I open /dashboard
    Then I see an AgentCard for each active agent
    And each AgentCard shows: name, agent_id, status, posts_today, engagement_rate, budget_usage

  Scenario: HITL review item opens content preview
    Given a review item exists with a content preview
    When I click the review item
    Then a modal opens showing full artifact and Judge reasoning_trace

  Scenario: Campaign creation enforces budget field
    Given the Campaign Form is displayed
    When I submit without budget
    Then the form shows validation error "budget is required"
