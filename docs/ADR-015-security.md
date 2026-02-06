# ADR-015: Security — AuthN, AuthZ, Secrets, Containment

Status: Proposed

Context
-------
The project currently lacks a formal security architecture covering authentication, authorization, secrets management, and runtime containment. Production-readiness requires explicit decisions so developers and operators have a clear path to secure deployments.

Decision
--------
Adopt the following decisions:

- Authentication: Use OIDC/OAuth2 for human users and short-lived JWTs for services. Validate tokens via JWKs endpoint and require MFA for operator/admin roles.
- Authorization: Enforce RBAC with predefined roles (`operator`, `developer`, `agent`, `auditor`, `admin`). Use policy engines (OPA) for complex rules when needed.
- Secrets: Use a centralized secrets manager (HashiCorp Vault preferred). Do not store secrets in Git. Use short-lived service credentials and rotate regularly.
- Containment: Run agents and workers in containers with least-privilege, enforce PSP/PSA in K8s, use NetworkPolicies, resource limits, and runtime detection (Falco).

Consequences
------------
- Increases operational complexity (need to run/consume Vault or cloud secrets) but significantly improves security posture.
- Requires changes to CI/CD to integrate secret retrieval and ensure secrets are not leaked.
- Requires onboarding documentation and example configurations (FastAPI middleware, Vault policies, K8s policies).

Next Steps
----------
1. Implement `docs/security/*` artifacts and populate `SECURITY.md`.
2. Integrate `spec_check.py` to require presence of `SECURITY.md` and `docs/security`.
3. Add CI checks for image scanning and secret scanning (e.g., Trivy, Gitleaks).
4. Provide sample FastAPI middleware and Vault policies in `examples/security/`.
