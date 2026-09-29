# Component and service model

This is a **logical service catalog**, not a mandate to deploy one process per row. A small installation can combine services while preserving ownership, contracts, isolation and observability. The platform supports voice and digital interactions, with channel-specific adapters feeding a common interaction/routing domain. The existing [voice topology](logical-architecture.md) is one view of this wider system.

## Plane and dependency rules

| Plane | Synchronous customer path | Can fail independently? | Example ownership |
|---|---|---|---|
| Edge/signaling | ingress, admission, SIP routing | admission may stop; existing anchored media may continue | SBC, SIP proxy, registrar |
| Media | prompt, bridge, conference, record fork | media-node loss affects its active calls | B2BUA/media server, relay |
| Real-time control | IVR decisions, queue, reservation, agent control | bound timeouts and safe degradation required | interaction, routing, agent state |
| Administration | published config, policy, tenant, identity | cached last-known-good config may serve calls | config/control APIs |
| Data/insight | event journal, recording, reporting, WFM, QM | analytics lag should not block calls; legally required recording may be a fail-closed exception | data and compliance services |

The same service may participate in several planes, but every write has one authoritative owner. Synchronous edges require a timeout, retry budget and declared fallback. Publication events require schema version, idempotency identity and replay policy. Use [state ownership](state-ownership.md) and [contracts](service-contracts.md) to review each boundary.

## Ingress, identity and tenant administration

| Logical service | Owns | Primary consumers / interface | Failure posture |
|---|---|---|---|
| Tenant and organization | tenant, business unit, site, hierarchy, quotas | admin API, policy evaluation | reject cross-tenant access; cached published hierarchy for existing routing |
| Identity and authorization | users, roles, scopes, session/token issuance, service identity | agent, supervisor, admin, APIs | deny new privileged actions if authorization unavailable |
| Provisioning and directory | agents, teams, skills, queues, external identities | admin sync/import, routing projections | versioned reconciliation; no partial publish |
| Configuration publication | immutable versioned snapshots of flow, queue, carrier, recording and routing policy | runtime config subscriptions | last-known-good with expiry; explicit rollback |
| Feature/entitlement | capability flags and licensed/contractual limits | admin UI and admission | safe default, audited changes |
| Audit | attributable append-only admin/security actions | compliance search/export | durable outbox; block sensitive mutations when audit durability is required |
| Secrets/certificate management | credential references, rotation and key lifecycle | edges, services, media | never deliver secrets through general config/event streams |

## Voice, media and interaction runtime

| Logical service | Owns | Primary consumers / interface | Failure posture |
|---|---|---|---|
| Number inventory and routing | DID/toll-free allocation, tenant binding, port state, egress eligibility | carrier edge and admin | reject unowned numbers; port cutover with rollback |
| Carrier route health | per path admission eligibility, circuit state, cost/quality policy inputs | edge/outbound policy | bounded alternate route; no blind replay of answered calls |
| SBC/edge | trust, normalization, admission, topology/media policy | carriers, SIP routing | remove unhealthy node; active-dialog impact topology-dependent |
| SIP proxy/registrar | request routing, transport, registration/location | endpoint and media tier | independent registration TTL; no fabricated reachability |
| Media/B2BUA | customer/agent legs, RTP bridge, prompts, DTMF, conference, optional transcoding | IVR, call-control, endpoint | active calls anchored on lost node usually fail |
| TURN/ICE gateway | relay allocations and NAT traversal for WebRTC | browser endpoints | reject or retry media setup; do not equate SIP answer with audio |
| IVR flow runtime | version-pinned flow instance, prompt/input state, integration calls | media and routing | bounded fallback; never block media indefinitely |
| Interaction lifecycle | interaction id, canonical state, participants, channel, correlation and terminal outcome | routing, desktop, data | idempotent terminalization and reconciliation |
| Queue | ordered waiting membership, deadlines, abandonment, priority | router, supervisor | durable/leased ownership; bounded failover |
| Router | eligibility, ranking, policy version and offer plan | queue, agent state, media | no offer without atomic capacity reservation |
| Agent state/capacity | presence, intent, device readiness, per-channel capacity, leases | router, desktop, supervisor | fail safe on stale state; reconcile with active legs |
| Offer/reservation | fencing token, attempt id, expiry, acceptance and release | router, agent gateway | single authoritative serialization point |
| Agent gateway/control | agent session delivery, call commands, acknowledgments | desktop and media | command idempotency; reconnect snapshot before new commands |
| Callback scheduler | promise window, consent, attempt budget, queue re-entry | IVR, outbound, router | no duplicate callback on retry; explicit expiry |
| Outbound campaign/dialer | list segmentation, pacing, compliance policy, attempt state | carrier routing, agent state | stop dialing when consent, pacing or state uncertain |
| Digital channel adapters | email/chat/SMS/social provider delivery and receipts | interaction and routing | channel-specific retry, ordering and consent |
| Conversation/notification | message timeline, templates, notifications and customer identity linking | desktop, digital channels | dedupe and per-channel delivery receipts |

## Experience, compliance and insight

| Logical service | Owns | Primary consumers / interface | Failure posture |
|---|---|---|---|
| Agent workspace | interaction/task UI, controls, device UX, disposition | agent gateway, CRM | restore from server snapshot; UI is not state authority |
| Supervisor control | monitor, whisper/barge request, queue oversight, intervention audit | media, agent state, router | explicit RBAC and media consent; no unaudited bypass |
| Recording policy/control | consent, start/stop/pause/resume decision and required-policy result | media, admin, compliance | fail open/closed per tenant/jurisdiction policy, never silently |
| Recording ingest/storage | segment manifest, checksums, encryption, retention, legal hold | playback, QA, export | reconcile missing segments and storage acknowledgments |
| Transcription/AI pipeline | consent-gated job, redaction, model/version and transcript lifecycle | QA, search, analytics | asynchronous backlog; mark partial/unavailable, not false complete |
| Quality management | evaluation form/version, sampling, score, dispute/coaching | supervisor, WFM | historical score references source version and recording |
| WFM forecasting | demand forecast, shrinkage and scenario assumptions | workforce planners | forecasts labeled by data cutoff and uncertainty |
| WFM scheduling/adherence | schedule, time-off, intraday changes, adherence events | agent/supervisor | event lag shown; no silent overwrite of approved schedule |
| Reporting/metrics | governed metric definitions and aggregates | dashboards, exports, WFM | delayed watermark shown; never read operational caches as history |
| Search/history | authorized interaction index, recordings/transcript references | agent/supervisor/compliance | stale index labeled; durable source remains authoritative |
| Integration/webhook | CRM, ticketing, workforce and partner delivery | external systems | outbox, signed delivery, retry/DLQ, idempotency |
| Event journal and projections | immutable domain event stream and rebuildable read models | insight, history, audit | lag and replay tracked; do not put BI queries on routing store |
| Observability/synthetics | correlation, traces, RTP/SIP telemetry, canary calls | SRE/engineering | telemetry outage should not stop calls unless policy requires evidence |

## Functional surfaces and API ownership

- **Agent**: login/readiness, tasks/call controls, notes/disposition, contact/context, device diagnostics and callback promises. Server authorizes every command; UI cannot directly change agent capacity.
- **Supervisor**: live queue/agent views with freshness, coaching, intervention, monitoring, reporting and schedule adjustments. Privileged media actions require reason, policy and audit.
- **Administrator**: tenant/hierarchy, users/roles, number/carrier, queues/skills, flow/prompt, routing, recording, retention, integrations, schedules, campaigns, configuration promotion and rollback.
- **Customer**: channel entry, IVR/self-service, callback, queue updates, consent and escalation.
- **Engineer/SRE**: correlation search, signaling/media evidence, route decision trace, config version, release health and failure drills. Access to payload/recording is separately controlled.

## Deployment mapping and technology examples

A possible voice mapping is Kamailio-class proxy, FreeSWITCH-class B2BUA/media, RTPengine-class relay, coturn-class TURN, durable relational records, low-latency coordination store and append-only event log. These are **implementation examples**, not interchangeable equivalents. Product and version selection, licenses, protocol interoperability, media benchmarks and operational ownership require proof. Keep media regional; place stateless APIs across failure domains; make queue/reservation authority explicit; isolate reporting query capacity from live routing.

## Adjacent platform capabilities

| Logical service | Boundary and authority |
|---|---|
| Knowledge/content | versioned articles, search permissions, retrieval provenance and publication workflow; agent assist may suggest, never silently alter authoritative answers |
| Bot/virtual agent | consent-aware dialog state, tool permissions, escalation with context; failed automation returns to queue without losing customer history |
| Survey/voice-of-customer | eligibility, opt-out, delivery and response; sampling avoids duplicate surveys after transfers |
| Usage/metering/billing | immutable usage facts with tenant, rate-plan version and reconciliation; billing disputes do not rewrite call events |
| Notification/template | versioned templates, localization, deliverability and opt-out; no PII in generic alerts |
| Developer platform | scoped API keys/OAuth, quotas, webhooks, sandbox, contract/version lifecycle and abuse controls |
| Release/platform operations | service registry, deployment inventory, config drift, SLO/incident/change management and cost attribution |

These can be integrated or delegated to external products. The architecture still assigns an owner for policy, data classification, failure behavior and audit at each boundary.

The [routing policy engine](routing-policy-engine.md) defines eligibility and ranking contracts. [Call-leg ownership](call-leg-ownership.md) separates interaction, SIP dialog, media bridge, participant and recording authority.
