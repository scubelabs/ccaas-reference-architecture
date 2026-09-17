# Voice Platform Observability Architecture

## Goal

Observability must answer a practical question: **what happened to this interaction, across every signaling, media, routing, agent, and dependency boundary?**

Dashboards alone are insufficient. The platform needs correlation, structured events, metrics, logs, protocol evidence, and synthetic testing.

## Correlation model

```text
interaction_id                 <- platform-wide business correlation
├── carrier_call_id
├── sip_dialog_id(s)
│   ├── Call-ID
│   ├── local_tag
│   └── remote_tag
├── media_session_uuid(s)
├── queue_id
├── routing_attempt_id(s)
├── agent_session_id
└── recording_id / event IDs
```

A B2BUA can create multiple SIP dialogs for one interaction. The platform therefore needs a correlation identifier above the SIP Call-ID level.

## Golden signals for voice

### Signaling

- call attempts and answers;
- SIP response distribution by carrier/route/node;
- post-dial delay and setup latency;
- INVITE retransmissions;
- transaction timeouts;
- registration count/failures;
- concurrent dialogs;
- CPS and admission rejection.

### Media

- concurrent media sessions;
- RTP packet counts by direction;
- packet loss, jitter and latency where measurable;
- no-RTP / media timeout events;
- codec distribution;
- transcoding utilization;
- media CPU/resource saturation;
- recording success/failure.

### ACD

- interactions waiting;
- queue age distribution;
- routing latency;
- routing attempts per interaction;
- reservation conflicts;
- eligible-agent count;
- agent state transitions;
- stale leases/state;
- abandoned interactions.

### Dependencies

Measure latency, error rate, saturation, timeout rate and circuit-breaker/degraded-state behavior for CRM, identity, databases, caches, event systems and external APIs.

## Structured event example

```json
{
  "event": "routing.agent_reserved",
  "interaction_id": "int-...",
  "routing_attempt_id": "route-...",
  "agent_id": "agent-1001",
  "queue_id": "support",
  "region": "region-a",
  "node": "routing-03",
  "timestamp": "...",
  "latency_ms": 12
}
```

Avoid putting credentials, payment data, health information, authentication tokens, raw customer audio, or unnecessary PII into telemetry.

## SLO examples

SLOs should measure customer-visible capability rather than process uptime alone. Candidate indicators include successful call admission, successful routing within a defined threshold, media establishment, callback completion, and agent control-plane availability.

The exact numerical objectives are business decisions and are intentionally not invented in this reference architecture.

## Synthetic monitoring

Synthetic calls can continuously validate the path that infrastructure health checks cannot:

```text
Test Caller → Carrier → SIP Edge → Media/IVR → Test Queue/Endpoint
```

A synthetic scenario can verify signaling, prompt/media receipt, DTMF, routing, answer and teardown. It should use dedicated test identities and avoid contaminating production analytics.

## Diagnostic escalation path

```text
Customer symptom
   ↓
Interaction search
   ↓
Timeline / correlated events
   ↓
SIP transaction/dialog evidence
   ↓
SDP/RTP evidence
   ↓
Node/dependency logs and metrics
   ↓
Root cause + blast radius
```

This architecture is designed so an engineer can move from a customer interaction identifier to packet-level evidence without manually guessing which nodes handled the call.
