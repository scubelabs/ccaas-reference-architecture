# State Ownership

State ownership is one of the most consequential design decisions in a distributed contact-center platform. If multiple services believe they authoritatively own the same mutable state, partial failures can produce duplicate routing, stale presence, lost interactions, or conflicting recovery actions.

## State classification

| State | Example | Characteristics | Candidate owner |
|---|---|---|---|
| Registration | agent SIP Contact | ephemeral, TTL-based | registrar/location service |
| SIP dialog | tags, route set | session-scoped | SIP UA/B2BUA/proxy transaction-dialog layer |
| Media session | RTP endpoints/codecs | session-scoped | media server |
| Agent presence | logged in/offline | near-real-time | agent-state service |
| Agent capacity | available/busy/concurrency | highly dynamic | agent-state/routing domain |
| Queue membership | waiting interaction | highly dynamic, correctness-sensitive | ACD/queue domain |
| Routing decision | selected agent/target | transactional/idempotent | routing domain |
| Interaction record | timestamps/disposition | durable | interaction-data service |
| Configuration | queues/skills/policies | durable/versioned | configuration service |
| Audit record | administrative changes | immutable/durable | audit/event domain |

## Source of truth vs cache

A system should distinguish an authoritative owner from projections and caches. Redis, for example, can be useful for low-latency state, but saying "Redis owns agent state" is incomplete. The architecture must define:

- which service is permitted to mutate the state;
- whether Redis is authoritative, derived, or a coordination mechanism;
- how TTL/lease expiration works;
- how state is rebuilt after loss;
- how conflicting updates are ordered;
- what consistency is required before routing a customer.

## Routing race example

Two routing workers can simultaneously observe Agent 1001 as `AVAILABLE` and attempt to reserve the same agent for different interactions.

The correctness boundary therefore needs an atomic reservation/lease or equivalent concurrency mechanism:

```text
AVAILABLE
    │ atomic reserve(interaction-id)
    ▼
RESERVED
    │ agent accepts / media connects
    ▼
BUSY
    │ interaction ends + wrap-up
    ▼
WRAP_UP
    │ ready
    ▼
AVAILABLE
```

The exact implementation can vary, but the state transition must have a single authoritative serialization point.

## Failure questions

For every state type the architecture should answer:

1. What is the authoritative owner?
2. Is the state ephemeral or durable?
3. What is the consistency requirement?
4. Can it be reconstructed?
5. What happens when its owner is unavailable?
6. What is the stale-state detection mechanism?
7. What is the recovery/reconciliation process?
8. Which operations must be idempotent?

These questions will be applied to each major CCaaS subsystem as the reference architecture expands.
