---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

## 🐛 Bug Description

<!-- Clear, concise description of the bug -->

**What happened:**


**What should have happened:**


---

## 📋 Spec Reference

<!-- Does this violate a specification? -->

**Related Spec:**
- [ ] Functional requirement: FR-[ID] from `specs/functional.md`
- [ ] Technical spec: Section from `specs/technical.md`
- [ ] Architectural principle from `specs/_meta.md`

**Spec citation:**
```
Example: FR-SWARM-001 states "Planner must monitor queue depth" but...
```

---

## 🔄 Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

**Minimal reproducible example:**
```python
# Code that reproduces the bug
```

---

## 🎯 Expected vs Actual Behavior

**Expected:**
<!-- What should happen according to specs -->

**Actual:**
<!-- What actually happens -->

---

## 🌍 Environment

**System Information:**
- OS: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
- Python Version: [e.g., 3.11.5]
- Docker Version: [e.g., 24.0.6]
- Branch: [e.g., main, develop]

**Dependencies:**
```bash
# Output of: uv pip list | grep -E "(pydantic|anthropic|mcp)"
```

**Docker Environment:**
```bash
# Output of: docker-compose ps
```

---

## 📊 Logs & Error Messages

**Error Output:**
```
Paste error messages, stack traces, or logs here
```

**Relevant Logs:**
```bash
# From: docker-compose logs orchestrator
# or: make docker-logs
```

---

## 💥 Impact

**Severity:**
- [ ] Critical - System is broken/unusable
- [ ] High - Major feature not working
- [ ] Medium - Feature partially working
- [ ] Low - Minor issue or cosmetic

**Affected Components:**
- [ ] Planner Agent
- [ ] Worker Agent  
- [ ] Judge Agent
- [ ] Orchestrator
- [ ] Skills
- [ ] Database
- [ ] Other: ___________

---

## 🔍 Additional Context

<!-- Screenshots, related issues, potential causes, etc. -->

---

## ✅ Checklist

- [ ] I've checked existing issues for duplicates
- [ ] I've provided a minimal reproducible example
- [ ] I've included relevant logs/errors
- [ ] I've referenced the related spec (if applicable)
- [ ] I've tested on the latest version
