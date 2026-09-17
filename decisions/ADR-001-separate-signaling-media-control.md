# ADR-001 — Separate Signaling, Media, Control and Data Concerns

**Status:** Accepted as a reference-architecture principle

## Context

Contact-center platforms combine workloads with very different performance and failure characteristics. SIP proxying, RTP processing, ACD decisions, agent presence, configuration and historical analytics should not be assumed to share the same scaling unit or availability behavior.

## Decision

Model the platform as four explicit architectural planes:

- **Signaling:** SIP routing, registration and dialog signaling.
- **Media:** RTP/SRTP and media applications.
- **Control:** ACD, agent state, orchestration, configuration and APIs.
- **Data:** durable interaction history, events, analytics and audit.

This is a logical separation. A small deployment may colocate functions physically, but ownership and dependencies remain explicit.

## Consequences

### Positive

- signaling and media can scale according to different bottlenecks;
- control-plane failure need not terminate established media by design;
- data/reporting outages can be decoupled from real-time call processing where appropriate;
- failure domains become easier to reason about and test;
- observability can measure each plane independently.

### Costs

- more interfaces and correlation requirements;
- distributed state must be designed rather than hidden in one process;
- operational complexity increases;
- cross-plane consistency and recovery semantics must be explicit.

## Rejected simplification

A single monolithic call-processing tier can be appropriate at smaller scale, but the reference architecture does not assume that its failure, scaling and deployment boundaries remain suitable for a carrier-grade multi-service platform.

## Validation

Architecture reviews should identify every critical dependency that crosses planes and ask whether its failure unnecessarily propagates into real-time interaction handling.
