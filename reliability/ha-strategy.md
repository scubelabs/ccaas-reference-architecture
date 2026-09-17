# High Availability Strategy

## HA is an end-to-end property

Redundant nodes do not by themselves create a highly available contact center. Availability depends on failure independence, detection time, routing convergence, state ownership, spare capacity, retry semantics, dependency design, and operational recovery.

## Layered HA model

### Carrier layer

Use independent ingress/egress options where business requirements justify them. Validate that numbers and routing policy can actually move traffic during a failure; contractual diversity without executable failover is not resilience.

### SIP edge and routing

Prefer multiple independently schedulable nodes. New traffic should be sent only to healthy destinations. For stateful proxy behavior, explicitly determine what dialog state is local, replicated, reconstructable, or unnecessary.

### Media tier

Distribute new sessions across multiple media nodes and failure domains. Because established RTP/call state is inherently sessionful, design primarily for **blast-radius reduction** rather than assuming transparent live-session migration.

### Control services

ACD/routing workers should be replaceable while correctness-sensitive state has explicit ownership and concurrency control. Worker failure must not permanently orphan reservations or queue items.

### Data services

Separate low-latency operational state from durable history according to consistency requirements. Replication does not remove the need to define failover authority, quorum, recovery, and stale-read behavior.

## Failure detection

Detection mechanisms should be layered:

- process/container health;
- protocol-level health (for example SIP OPTIONS where appropriate);
- dependency health;
- synthetic transaction/call health;
- real traffic success rates;
- media quality/packet telemetry.

A process responding to TCP health checks can still be incapable of completing a call.

## Draining

Planned maintenance should differ from failure.

```text
ACTIVE
  ↓ stop accepting new sessions
DRAINING
  ↓ established sessions complete
EMPTY
  ↓ maintenance/restart
ACTIVE
```

Draining reduces avoidable customer impact and is especially important for media nodes.

## N+1 and failure capacity

If a pool runs near full utilization, node redundancy may exist only on paper. Capacity planning must ensure surviving nodes can absorb the defined failure case without crossing safe CPU, memory, CPS, concurrent-session, RTP, port, or downstream limits.

## Dependency isolation

An observability outage should not stop call processing. A reporting database outage should not necessarily stop an established voice call. Architecture should identify which dependencies are synchronous critical-path dependencies and which can be decoupled through events, buffering, cached configuration, or degraded operation.

## Retry ownership

Only one layer should own a given retry policy unless interactions between retries are deliberately designed. Carrier retry + SIP proxy retry + media retry + ACD retry can otherwise amplify one failure into duplicate attempts or a traffic storm.

For each retry define maximum attempts, total time budget, backoff/jitter where relevant, retryable error classes, idempotency identity, and terminal behavior.

## Availability objectives

Reliability targets should be defined per customer capability rather than as one platform number. Examples include ability to accept new inbound calls, preserve established media, route queued interactions, deliver agent events, retrieve configuration, write durable interaction records, and access historical reporting.

This prevents a healthy reporting service from masking a failed voice path—or vice versa—in a single aggregate availability metric.
