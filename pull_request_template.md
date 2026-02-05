# Pull Request: [Title]

<!-- 
Replace [Title] above with a concise description following conventional commits:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Adding or updating tests
- refactor: Code refactoring
- chore: Maintenance tasks

Example: "feat(swarm): implement Planner agent task decomposition"
-->

## 📋 Spec Alignment

<!-- CRITICAL: Reference the specification this PR implements -->

**Implements:**
- [ ] Functional Requirement: FR-[REQUIREMENT-ID] (from `specs/functional.md`)
- [ ] Technical Spec: Section X.Y from `specs/technical.md`
- [ ] Follows principles in `specs/_meta.md`

**Spec Reference:**
```
Example:
- FR-SWARM-001: Task Decomposition (Planner Role)
- technical.md Section 3.1: Agent Task Schema
```

**Acceptance Criteria Met:**
<!-- Copy acceptance criteria from specs/functional.md -->
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## 📝 Description

### What does this PR do?

<!-- Clear, concise explanation of the changes -->

### Why is this change needed?

<!-- Business or technical justification -->

### How does it work?

<!-- Brief technical explanation -->

---

## 🧪 Testing

### Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Tests follow TDD approach (written before implementation)
- [ ] All tests pass locally (`make test`)

**Test Files:**
```
- tests/functional/test_[feature].py
- tests/integration/test_[integration].py
```

**Test Coverage:**
<!-- Run: make test-cov -->
```
Coverage: X%
Lines covered: Y/Z
```

### Manual Testing

<!-- How did you verify this works? -->

**Steps to test:**
1. Step 1
2. Step 2
3. Expected result

---

## 🏗️ Architecture

### Pattern Used

- [ ] Planner-Worker-Judge pattern
- [ ] MCP abstraction layer
- [ ] Skill interface contract
- [ ] Other: ___________

### Components Modified

- [ ] `src/swarm/` - Agent components
- [ ] `src/schemas/` - Data models
- [ ] `src/orchestrator/` - Control plane
- [ ] `skills/` - Agent capabilities
- [ ] Other: ___________

### Dependencies

**New dependencies added:**
<!-- List any new packages in pyproject.toml -->
```
- package-name==version  # Reason for adding
```

---

## 🔒 Security Checklist

- [ ] No hardcoded API keys or secrets
- [ ] Environment variables used for configuration
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive information
- [ ] Authentication/authorization checked (if applicable)
- [ ] SQL injection prevention (if applicable)

---

## 📊 Code Quality

### Linting & Formatting

- [ ] Code passes `make lint` (black, ruff, mypy)
- [ ] No new linting errors introduced
- [ ] Type hints added for all functions
- [ ] Docstrings added for public functions

### Code Review Preparation

- [ ] Code is self-explanatory with clear variable names
- [ ] Complex logic has explanatory comments
- [ ] No commented-out code or TODOs (unless tracked in issues)
- [ ] Git commit history is clean and meaningful

---

## 🚀 Deployment Considerations

### Breaking Changes

- [ ] This PR contains breaking changes
- [ ] Migration path documented
- [ ] Backward compatibility maintained

### Environment Variables

**New environment variables required:**
```
VARIABLE_NAME=default_value  # Description
```

### Database Changes

- [ ] No database changes
- [ ] Database migration included
- [ ] Migration tested locally

---

## 📸 Screenshots (if applicable)

<!-- Add screenshots for UI changes, dashboard updates, etc. -->

---

## 🔗 Related Issues

<!-- Link related issues -->

Closes #[issue-number]
Related to #[issue-number]

---

## ✅ Pre-Merge Checklist

**Required before merging:**

- [ ] All CI checks pass
- [ ] Code review approved by at least one reviewer
- [ ] Spec alignment verified
- [ ] Test coverage adequate (>80% for new code)
- [ ] Documentation updated (if needed)
- [ ] No merge conflicts
- [ ] Branch is up to date with main

---

## 📚 Additional Notes

<!-- Any additional context, considerations, or future work -->

---

## 🤖 AI Review Instructions

<!-- Instructions for CodeRabbit AI reviewer -->

**Focus areas for AI review:**
1. Spec compliance: Does this match specs/functional.md and specs/technical.md?
2. Security: Any hardcoded secrets or vulnerabilities?
3. Architecture: Follows Project Chimera patterns?
4. Test coverage: Adequate tests for new functionality?

**Specific concerns:**
<!-- Any areas you want extra scrutiny on -->

---

<!-- 
REMINDER: Project Chimera follows Spec-Driven Development
- All code must align with specifications
- Tests must be written before implementation
- MCP abstraction must be used for external calls
- Reference CLAUDE.md for AI coding conventions
-->
