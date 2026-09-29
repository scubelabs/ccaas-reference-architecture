# Service contracts and endpoint inventory

These are **illustrative contracts**, not an implemented API or a claim of stable schema. Public APIs use authenticated tenant-scoped HTTP where appropriate; low-latency internal operations may use gRPC or equivalent typed RPC. The agent event stream is authenticated WebSocket/SSE with sequence and replay. SIP, RTP, WebRTC/ICE, carrier trunks and media control are protocol interfaces, not REST endpoints.

## Required contract envelope

- Identity: `tenant_id`, `actor_id`/service principal, scopes, region and explicit resource ownership.
- Correlation: `interaction_id` (when known), `trace_id`, `request_id`, `causation_id`; map SIP Call-ID/leg IDs separately.
- Concurrency: `expected_version` or ETag for configuration and mutable state; routing reservations use fencing token.
- Retry: `Idempotency-Key` scoped to tenant + operation, retained at least as long as caller retry horizon; return original result on replay.
- Time: UTC event timestamp plus monotonic local duration; include server receipt time and schema version.
- Error: machine-readable code, retryable flag, retry-after where applicable, safe message and correlation id. Never return secrets, raw SIP auth or PHI in generic error responses.
- Pagination: opaque cursor and stable ordering for history; authorization checked on every page.

## Command/API map

| Surface and example endpoint | Authority / effect | Guard and failure behavior |
|---|---|---|
| `POST /v1/agents/sessions` | agent gateway creates authenticated session | identity + device policy; duplicate session policy explicit |
| `PUT /v1/agents/me/routing-intent` | agent state sets ready/not-ready + reason | expected version; routing eligibility recalculated |
| `GET /v1/agents/me/snapshot` | agent gateway returns authoritative tasks and sequence | use after reconnect before applying stream deltas |
| `GET /v1/agents/me/events?after=seq` | ordered stream/replay | gap → snapshot refresh; no silent event loss |
| `POST /v1/interactions/{id}/commands/{answer,hold,resume,transfer,hangup}` | media/call-control orchestrator | command idempotency, leg ownership, state precondition; ambiguous outcome queried before retry |
| `POST /v1/interactions/{id}/disposition` | interaction service finalizes disposition | policy/version, idempotency; late edit audited |
| `POST /v1/queues/{id}/enqueue` | queue creates waiting item | interaction uniqueness and deadline; outbox event |
| `POST /internal/v1/reservations` | agent state/offer authority atomically reserves capacity | `interaction_id`, `attempt_id`, `agent_id`, lease, fencing; conflict is expected response |
| `POST /internal/v1/reservations/{id}/{accept,release,renew}` | authoritative offer transition | compare lease/fence; stale worker cannot accept |
| `POST /v1/callbacks` | callback service creates promise | consent, number validation, window, dedupe and attempts |
| `POST /v1/admin/config/drafts` | config service creates editable version | RBAC, schema validation, tenant boundary |
| `POST /v1/admin/config/{version}/validate` | dry-run dependency and policy checks | routing/flow/recording references and capacity rules |
| `POST /v1/admin/config/{version}/publish` | atomic release pointer switch | approval, audit durability, canary/scope; roll back pointer not history |
| `GET /v1/supervisor/queues?as_of=...` | freshness-stamped projection | lag and last event seq visible; intervention uses authoritative command path |
| `POST /v1/supervisor/interactions/{id}/{monitor,whisper,barge}` | privileged media intervention | RBAC, policy/consent, reason, durable audit, media result |
| `GET /v1/reports/{report}?from=&to=&cursor=` | governed reporting dataset | metric version, time zone, watermark, role/tenant filters |
| `GET /v1/interactions/{id}/timeline` | event/search projection | correlation and completeness marker; payload access separately scoped |
| `GET /v1/recordings/{id}/playback-grant` | recording access service | short-lived grant, purpose, audit and hold/retention check |
| `POST /v1/integrations/{id}/deliveries/replay` | integration service | operator authorization, original idempotency identity, audit |

Do not expose reservation mutation, SIP media control, or raw event journal directly to browsers. Gateways enforce authorization; owning service rechecks it. For all endpoints define request/response schemas, rate limits, timeout and compatibility before implementation.

## Example reservation

```json
{
  "tenant_id": "t-123",
  "interaction_id": "i-456",
  "routing_attempt_id": "ra-2",
  "agent_id": "a-789",
  "queue_id": "q-1",
  "policy_version": "p-42",
  "lease_ms": 12000,
  "idempotency_key": "t-123:i-456:ra-2"
}
```

Successful response includes `reservation_id`, monotonically increasing `fencing_token`, `expires_at`, `agent_state_version` and `outcome=reserved|existing`. A conflict returns a typed ineligible/conflict result, not an alternate agent chosen silently. A late accept with an expired fence fails even if an old notification reaches the desktop.

## Event catalog (minimum)

| Event | Producer | Consumer and invariant |
|---|---|---|
| `interaction.created/queued/connected/ended` | interaction lifecycle | reporting/history; one terminal outcome per interaction revision |
| `routing.attempted/offered/accepted/expired` | router/offer authority | timeline, supervisor; attempt id + policy version |
| `agent.intent_changed/capacity_changed` | agent state | routing projection; ordered per agent |
| `media.leg_created/connected/ended/quality_observed` | media | interaction, telemetry; leg IDs, not only SIP Call-ID |
| `recording.required/started/segment_stored/failed/finalized` | recording | compliance and QA; explicit incomplete state |
| `transcript.started/partial/final/failed/redacted` | transcription | search/QM; revision and model version |
| `config.published/rolled_back` | configuration | runtimes pin version, ack application |
| `schedule.published/adherence_observed` | WFM | supervisor/agent; event-time + projection watermark |
| `audit.action_recorded` | audit | compliance; actor, purpose, before/after hashes |

Events use `event_id`, `aggregate_id`, `aggregate_version`, `schema_version`, `occurred_at`, `recorded_at`, `tenant_id`, causation and correlation. Producers commit state and outbox together where atomic durability is required. Consumers dedupe by `event_id`, handle at-least-once delivery, persist offsets and send poison events to a reviewed DLQ. Cross-aggregate total ordering is **not** promised.

## Versioning and compatibility

Additive fields are tolerated; required semantic changes get a new event/API version. A consumer must not infer new meanings from an old event name. Pin configuration per interaction/flow. Contract tests cover old producer/new consumer and new producer/old consumer across rolling deployments; schema registry or CI checks reject incompatible changes.

## Customer, automation, workforce and developer API additions

| Endpoint or event family | Owning service | Required guard |
|---|---|---|
| `GET /v1/customers/{id}`, `POST /v1/customers/identity-links` | profile/identity | field ABAC, provenance, verified linkage and merge audit |
| `POST /v1/cases`, `PATCH /v1/cases/{id}`, `POST /v1/cases/{id}/tasks` | case/work item | tenant, expected version, SLA calendar and idempotency |
| `POST /v1/journeys/{id}/triggers`, `POST /v1/journeys/{id}/cancel` | journey | consent/quiet-hour/contact cap, step ledger and dedupe |
| `POST /v1/admin/flows/{version}/simulate|validate|publish` | flow config/runtime | graph/dependency/policy validation, approval and canary |
| `GET /v1/knowledge/search`, `POST /v1/assist/{interaction_id}/feedback` | knowledge/assist | article scope/version and no unauthorized raw transcript |
| `POST /v1/qm/evaluations`, `POST /v1/qm/evaluations/{id}/disputes` | quality | evidence/rubric version, evaluator scope and history |
| `POST /v1/wfm/forecasts/{id}/publish`, `POST /v1/wfm/schedules/{id}/publish` | workforce | assumptions, labor policy, expected version and audit |
| `GET /v1/performance/scorecards?as_of=...`, `POST /v1/surveys/dispatch` | performance/survey | metric version, sample sufficiency, consent and dedupe |
| `POST /v1/developer/apps`, `POST /v1/integrations/{id}/webhooks` | developer/integration | scopes, egress, signing, quotas, secret isolation and review |
| `GET /v1/usage?from=&to=` | metering | immutable fact references, rate version, watermark and tenant scope |

The detailed state machines and failure behavior live in [customer journey/case](customer-journey-case.md), [automation](automation-ai-knowledge.md), [performance](performance-management.md) and [developer ecosystem](developer-platform.md). These endpoint shapes are illustrative; implementation requires a published schema and compatibility suite.
