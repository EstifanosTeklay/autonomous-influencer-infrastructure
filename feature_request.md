---
name: Feature Request
about: Suggest a new feature or enhancement
title: '[FEATURE] '
labels: ['enhancement', 'needs-spec']
assignees: ''
---

## 💡 Feature Description

<!-- Clear, concise description of the proposed feature -->

**What feature do you want:**


**Why is it needed:**


---

## 📋 Spec Alignment

<!-- IMPORTANT: New features must align with Project Chimera's architecture -->

**Aligns with:**
- [ ] Architectural principles in `specs/_meta.md`
- [ ] Planner-Worker-Judge pattern
- [ ] MCP abstraction layer
- [ ] Skill interface contract

**Potential spec impact:**
- [ ] New functional requirement (add to `specs/functional.md`)
- [ ] New technical spec (add to `specs/technical.md`)
- [ ] New skill category
- [ ] Modification to existing spec

**Proposed Functional Requirement:**
```
FR-[CATEGORY]-[NUMBER]: [Title]

User Story:
> As a [USER TYPE], I need to [ACTION], so that [BENEFIT].

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

---

## 🎯 Use Cases

**Who benefits:**
- [ ] Chimera Agents (autonomous influencers)
- [ ] Network Operators (human managers)
- [ ] System Developers
- [ ] End users / audience

**Example scenarios:**
1. Scenario 1: ...
2. Scenario 2: ...

---

## 🏗️ Proposed Implementation

**High-level approach:**
<!-- How might this be implemented? -->

**Components affected:**
- [ ] `src/swarm/` - Agent logic
- [ ] `src/schemas/` - Data models
- [ ] `skills/` - New skill or modification
- [ ] `specs/` - Specification updates
- [ ] Database schema changes
- [ ] Other: ___________

**New dependencies required:**
```
- package-name  # Why needed
```

---

## 🔄 Alternatives Considered

**Alternative 1:**
<!-- What other approaches did you consider? -->

**Why not chosen:**


**Alternative 2:**


---

## 🧪 Testing Strategy

**How should this be tested:**
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Manual testing steps

**Test scenarios:**
1. Test case 1
2. Test case 2

---

## 📊 Success Metrics

**How do we measure success:**
- Metric 1: ...
- Metric 2: ...

**Performance impact:**
- [ ] No performance impact
- [ ] May improve performance
- [ ] May affect performance (explain):

---

## 🎨 UI/UX Considerations

<!-- If this affects user interface or experience -->

**Mockups/Wireframes:**
<!-- Attach images or links -->

---

## 🔐 Security Considerations

**Security implications:**
- [ ] No security impact
- [ ] Requires new secrets/API keys
- [ ] Affects authentication/authorization
- [ ] Data privacy considerations
- [ ] Other: ___________

**Mitigation plan:**


---

## 📈 Priority & Effort

**Priority:**
- [ ] Critical - Core functionality
- [ ] High - Important enhancement
- [ ] Medium - Nice to have
- [ ] Low - Future consideration

**Estimated effort:**
- [ ] Small (< 1 day)
- [ ] Medium (1-3 days)
- [ ] Large (1 week)
- [ ] XL (> 1 week)

**Complexity:**
- [ ] Low - Simple implementation
- [ ] Medium - Moderate complexity
- [ ] High - Complex, many dependencies

---

## 🔗 Related Issues

<!-- Link to related issues or PRs -->

Related to #[issue-number]
Depends on #[issue-number]

---

## 📚 Additional Context

<!-- Any other context, research, links, etc. -->

**Research:**
- Link 1: ...
- Link 2: ...

**References:**
- Similar feature in other projects: ...
- Academic papers: ...

---

## ✅ Checklist

- [ ] I've checked existing issues/PRs for duplicates
- [ ] I've explained the use case clearly
- [ ] I've considered spec alignment
- [ ] I've thought through implementation approach
- [ ] I've identified affected components
- [ ] I've considered security implications

---

## 🤖 AI Review Notes

<!-- For CodeRabbit or other AI reviewers when this becomes a PR -->

**Review focus:**
- Does this align with Project Chimera's architectural principles?
- Is the spec update complete and clear?
- Are tests comprehensive?
