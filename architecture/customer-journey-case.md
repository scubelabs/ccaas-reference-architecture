# Customer profile, cases and journey orchestration

A contact center must preserve context across channels and time. One customer may have many identifiers, conversations, interactions and cases; an interaction can be anonymous until identity is verified. The platform should not equate a phone number with a person or make a model's identity guess authoritative.

## Identity and consent model

| Object | Owner | State and guard |
|---|---|---|
| `CustomerProfile` | profile service | tenant-scoped stable id, verified identity links, provenance/version, merge/split audit |
| `Address` | profile service | phone/email/channel handle with verified/unverified state and last-verified time |
| `Preference` | preference/consent service | language, accessibility, channel, quiet hours, contact purpose and expiry |
| `ConsentRecord` | consent authority | scope/purpose/channel/jurisdiction, capture method, effective/withdrawn time, proof |
| `Case` | case service | issue, owner/team, priority, SLA, status, related interactions, policy version |
| `Task` | case/work-item service | assignment, deadline, dependencies, state, resolution and reopen reason |
| `Journey` | journey service | goal, step graph, suppression window, experiment cohort, current action |
| `Conversation` | digital/interaction service | channel thread, provider ids and delivery receipts; may link to case/journey |

Identity resolution is a staged process: anonymous intake → candidate match with source/confidence → approved verification → linked profile. A merge is reversible with lineage and privacy controls. Data fetched from CRM carries source, timestamp, TTL and field-level authorization; it is not silently copied into every log or analytics event. Profile query failure cannot bypass mandatory verification or consent.

## Case lifecycle and handoff

`new → triaged → assigned → in_progress → pending_customer|pending_external → resolved → closed`, with `reopened` as a versioned transition. The case may outlive calls and agent shifts. SLA policy records business calendar, pause/resume conditions, escalation, due time and version. A case owner is not automatically the next voice agent; routing may prefer that agent as a soft affinity while preserving skills, capacity and tenant guards. Transfers add assignment history and linked interactions; they do not overwrite earlier owner/evidence. Attachments are scanned, classified, encrypted and retention-scoped.

Create/assign/update/resolve commands use expected version and idempotency key. External ticket sync uses an outbox and bidirectional mapping with conflict policy; when the external system is unavailable, mark sync pending and show it to the agent. Do not claim a case is closed externally on local API success alone.

## Journey decisioning

A journey is a version-pinned, consent-aware orchestration across IVR, bot, agent, callback, email/chat/SMS and follow-up. Trigger inputs include customer action, event, schedule, case change and campaign membership. Eligibility checks tenant, contact policy, quiet hours, suppression, experiment cohort and current unresolved work before an action is emitted. A durable step ledger prevents duplicate messages/calls after retries; each step has max attempts, deadline, compensation and terminal state. A contact cap spans campaigns and service journeys where required.

Example: failed self-service payment → verified profile and case context → eligible callback offer → agent follow-up → consented survey. A customer may switch voice to chat; pass a context token and conversation link, not an unauthenticated transcript dump. If the destination channel fails, the journey records delivery unknown and falls back only under approved policy.

## APIs/events (illustrative)

- `GET /v1/customers/{id}?fields=...` returns provenance, verification and field-scoped data; search by phone is rate-limited and not proof of identity.
- `POST /v1/customers/identity-links` requires verification evidence; merge/split is privileged and audited.
- `POST /v1/cases`, `PATCH /v1/cases/{id}` and `POST /v1/cases/{id}/tasks` use idempotency and expected version.
- `GET /v1/cases/{id}/timeline` joins case actions to authorized interactions and attachments with completeness watermark.
- `POST /v1/journeys/{id}/triggers` dedupes source event; `POST /v1/journeys/{id}/pause|resume|cancel` is versioned.
- Events: `profile.linked/unlinked`, `consent.granted/withdrawn`, `case.assigned/resolved/reopened`, `journey.step_scheduled/sent/failed`, each with tenant, aggregate version and correlation.

## Failure and proof

Test ambiguous identity, wrong-tenant lookup, profile merge rollback, consent withdrawal between schedule and send, duplicate trigger, quiet-hour boundary, case-owner change during call, external sync outage, cross-channel handoff and deletion/legal hold. Measure case SLA from its authoritative calendar, journey completion by durable step outcomes and context reuse without leaking data. A dashboard showing “customer 360” must expose stale/missing sources and verification level.
