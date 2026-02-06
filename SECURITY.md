# Security Specification - Project Chimera

**Last Updated:** February 6, 2026

This document specifies formal Authentication, Authorization, Secrets Management, and Containment controls required for production readiness.

## 1. Goals
- Enforce strong AuthN for users and service-to-service communication
- Implement RBAC and least-privilege Authorization for human and agent actors
- Centralize secrets in a secrets manager (Vault/AWS Secrets Manager)
- Contain runtime processes using platform features (containers, K8s PSP/PSA, network policies)
- Protect keys & tokens in CI/CD and local development
- Provide clear onboarding and incident response steps

## 2. Authentication (AuthN)
- User AuthN:
  - Use OAuth2/OpenID Connect (OIDC) for human users (Identity Provider: GitHub, Google, or corporate IdP)
  - Require MFA for operator roles
  - Session tokens are short lived (15-60 minutes) and validated via introspection

- Service AuthN (Agent ↔ MCP ↔ Services):
  - Use mTLS between services where possible
  - Issue short-lived service tokens via Vault or cloud IAM
  - For HTTP-based MCP tooling, require OAuth2 client credentials or JWT signed by enterprise signing key

- Example: FastAPI integrates with OAuth2/OIDC provider and validates JWTs using JWKs endpoint.

## 3. Authorization (AuthZ)
- Role-based access control (RBAC):
  - Roles: `operator`, `auditor`, `developer`, `admin`, `agent` (non-human service role)
  - Map API endpoints and UI actions to roles using policy definitions
  - Use least privilege: default to deny, explicitly grant minimal permissions

- Agent-level scopes:
  - Agents have service identities (`agent:<agent_id>`) and are assigned scopes: `read:memory`, `write:memory`, `publish:content`, `manage:campaign`
  - Judges and Planners run with different scopes; workers have `execute:task` only

- Policy example (pseudo):
```
# agent-policy.hcl (for HashiCorp Vault / OPA)
path "agent/*/memory/*" {
  capabilities = ["read", "list"]
}
path "agent/*/publish" {
  capabilities = ["deny"]
}
```

## 4. Secrets Management
- DO NOT store secrets in Git. `.env` files must be in `.gitignore`.
- Use a centralized secrets manager in production (one of):
  - HashiCorp Vault
  - AWS Secrets Manager + KMS
  - Azure Key Vault

- Local development:
  - Use developer-specific local secrets vault (e.g., `vault dev` or `direnv`) and never commit real keys
  - Provide `env.example` as template (already present)

- Rotation & Access:
  - Rotate high-risk keys monthly
  - Enforce short-lived credentials for service tokens (rotate on each deployment if possible)
  - Audit all secret accesses and alerts for abnormal access patterns

- CI/CD:
  - Store secrets in GitHub Actions Secrets or Vault with short-lived tokens
  - Avoid printing secrets in logs
  - Use `actions/checkout@v4` with `persist-credentials: false` for security-sensitive jobs

## 5. Containment & Runtime Hardening
- Container image policy:
  - Use minimal base images (e.g., `python:3.11-slim`)
  - Scan images in CI (e.g., Trivy, Snyk)
  - Enforce non-root containers

- Kubernetes (production):
  - Use Pod Security Admission / Pod Security Policies (PSA)
  - Apply NetworkPolicies to segment traffic (e.g., only orchestrator ↔ redis)
  - Limit resource requests/limits, restrict hostPath, disallow privileged containers
  - Use RBAC for K8s API access

- Network & ingress:
  - Ingress controllers terminate TLS; enforce HTTPS and HSTS
  - Add Content Security Policy (CSP) and other security headers in API responses

- Runtime detection:
  - Integrate Falco for runtime anomaly detection
  - Centralize logs (Sentry + structured logs) and monitor for suspicious patterns

## 6. Secrets in Code & Tests
- Replace real API keys with test stubs or mocks in tests
- Add a pre-commit git hook to scan for accidental secrets (`detect-secrets`, `gitleaks`)
- CI step: run `gitleaks` or `trivy` as part of PR checks

## 7. Developer Onboarding (Quick Start)
1. Install Vault dev or configure cloud secrets for your environment
2. Copy `env.example` -> `.env` and load values from secrets manager
3. Use `automation/runner.py mcp-validate` to check MCP config
4. Run `python spec_check.py` before opening PRs

## 8. Incident Response & Key Compromise
- Revoke compromised secrets immediately via secrets manager
- Rotate affected keys and redeploy with new credentials
- Create an incident ticket and capture audit logs for scope of compromise

## 9. Checklist (Minimum for production)
- [ ] OIDC configured for human users
- [ ] Service identity & mTLS / short-lived tokens for services
- [ ] Secrets stored in Vault/AWS (no secrets in repo)
- [ ] Image scanning in CI
- [ ] Pod Security / PSA enabled in cluster
- [ ] Network segmentation via NetworkPolicy
- [ ] Pre-commit secret scanning (gitleaks/detect-secrets)
- [ ] CI secrets masked and audited

## 10. References
- OAuth2 / OIDC documentation
- HashiCorp Vault guides
- Kubernetes Pod Security Standards
- OWASP Top 10

---

Additions requested: if you want, I can add example FastAPI AuthN middleware (JWT/OIDC) and a sample Vault policy + K8s NetworkPolicy YAML.