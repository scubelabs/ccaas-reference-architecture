# ADR-002 — Authoritative state and asynchronous projections

**Status:** Accepted as reference principle

## Context

Voice admission, agent capacity and queue assignment require low-latency correctness. Reporting, WFM and search need durable history and tolerate bounded lag. A single shared database or event bus as an implicit owner makes retries and partitions ambiguous.

## Decision

Each aggregate has one write authority; commands use idempotency keys, version checks and fencing where leases can outlive a worker. Persist critical state transitions with an outbox before publishing events. Projections consume at-least-once delivery, dedupe, expose watermark and rebuild from durable sources. A region/partition policy must prevent simultaneous owners of a reservation shard.

## Consequences

Reporting may lag live routing, so UI shows freshness. The event bus is not a substitute for an authoritative reservation store. Consumer replay and schema evolution become first-class operational tasks. An ambiguous command outcome is queried by idempotency key before retry.

## Validation

Crash between commit and publication, duplicate event, reordered events, expired lease, stale-region writer, replay/backfill and projection catch-up must produce one defensible interaction outcome. See [contracts](../architecture/service-contracts.md), [data](../architecture/data-reporting-wfm.md) and [acceptance](../validation/architecture-acceptance.md).
