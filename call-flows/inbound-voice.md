# Inbound Voice — End-to-End Call Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant CR as Carrier
    participant E as SBC / SIP Edge
    participant K as SIP Routing
    participant M as Media / IVR
    participant R as ACD Routing
    participant S as Agent State
    participant A as Agent Gateway/Endpoint

    C->>CR: PSTN call
    CR->>E: INVITE
    E->>E: trust, policy, normalization, admission
    E->>K: INVITE
    K->>M: route to media/IVR
    M-->>C: early/answer media as designed
    M->>M: collect IVR context
    M->>R: route(interaction, queue, skills, context)
    R->>S: find/reserve eligible capacity
    S-->>R: reservation
    R-->>M: selected agent + routing attempt
    M->>A: establish agent leg
    A-->>M: answer
    M-->>E: call established
    Note over C,A: media connected through configured media path
    A->>M: agent/customer call ends
    M->>R: interaction termination/disposition events
```

## Phase 1 — Admission

Carrier ingress should be authenticated/trusted according to the carrier model, normalized as needed, rate/admission controlled, and correlated with a platform interaction identifier as early as practical.

## Phase 2 — IVR

The media/application tier owns prompt/media behavior and gathers routing context. External service calls should not have unbounded latency. The IVR needs defined fallback behavior when CRM, identity or other dependencies fail.

## Phase 3 — Routing

The routing request should contain sufficient context to make a deterministic policy decision: tenant/business unit, queue, skills, priority, language, customer context, channel, and other approved attributes.

The routing system must reserve—not merely observe—agent capacity before delivery.

## Phase 4 — Agent delivery

Agent delivery can create a separate SIP/WebRTC/media leg. The platform should distinguish `reserved`, `offered`, `ringing`, `accepted`, `connected`, `failed`, and `timed-out` states so recovery behavior is explicit.

## Phase 5 — Connected interaction

Routing-worker availability should not be required to keep an already established media session alive. This separation reduces the blast radius of control-plane failure.

## Phase 6 — Termination

Call teardown should generate idempotent finalization events for agent state, queue/routing state, interaction history, recording metadata, analytics and downstream consumers.

## Correlation requirement

Every phase should preserve `interaction_id` even when SIP Call-IDs or media UUIDs change across B2BUA boundaries. This is the foundation for end-to-end troubleshooting.
