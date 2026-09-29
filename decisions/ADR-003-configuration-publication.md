# ADR-003 — Versioned configuration publication

**Status:** Accepted as reference principle

## Context

Routing, IVR, carrier and recording policies may change while calls are active. Direct edits to shared runtime tables can create region drift, partial activation and unreviewable rollback.

## Decision

Use editable drafts, schema/dependency validation, approval for sensitive policy, immutable published snapshots and an atomic active-version pointer. New interactions pin a version. Runtime acknowledgments, canary scope, synthetic tests and drift alarms gate ramp. Rollback publishes a pointer to a prior validated snapshot; retain the audit chain.

## Consequences

More storage and release orchestration are required. Emergency change is a privileged, audited workflow with explicit scope. Cached snapshots have expiry and cannot silently become permanent authority.

## Validation

Reject missing queue/prompt/number references, cycle and unauthorized retention change. Inject one-region apply failure; verify no claim of full publication. Prove in-flight calls keep their pinned version and canary rollback affects only new admissions. See [admin](../architecture/admin-supervisor-agent.md).
