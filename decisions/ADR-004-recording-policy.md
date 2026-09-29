# ADR-004 — Recording policy is separate from media ingest

**Status:** Accepted as reference principle; jurisdiction-specific behavior remains a deployment decision.

## Context

A media fork can fail after a recording request is acknowledged. Consent and payment handling may require different behavior per tenant, queue, leg and location.

## Decision

Separate policy/control from media fork and durable recording manifest. The control result is versioned and explicit (`required`, `optional`, `prohibited`, `unknown`). Recording state remains `partial|failed` until segment continuity is verified. Required-recording failure invokes a tenant-approved and tested block/degrade/terminate policy; never label unverified audio complete. Playback and transcription have separate authorization and retention.

## Consequences

Calls may be blocked or degraded when evidence is required; deployment owners must choose behavior. Storage manifests, checksums, gap reconciliation and audit become operational dependencies. See [recording architecture](../architecture/recording-transcription-quality.md).
