# Interaction data, reporting, WFM and analytics

Real-time control stores, durable records, event journal, search and analytical warehouse have different semantics and workloads. Routing must not synchronously query a reporting warehouse. Reporting must not treat a transient queue cache as historical truth.

The [data-store topology](data-store-topology.md) maps reporting's columnar warehouse, metric-definition authority, search/live projections, event log and source transactional outboxes to HA and scaling boundaries. The [interaction handoff ledger](interaction-ownership.md) defines which operational owners produce each source fact.

## Canonical entities and keys

| Entity | Identity / authority | Important relationships |
|---|---|---|
| Tenant, business unit, site, team | tenant/organization service | resource hierarchy and effective policy version |
| Account/agent/agent session | identity + agent state | agent can have multiple sessions; policy decides active control |
| Customer/contact | customer identity service/integration | multiple channel addresses; matches carry provenance |
| Interaction | interaction lifecycle | tenant, channel, direction, customer, config version, terminal outcome |
| Segment/leg | media/channel adapter | one interaction can have multiple carrier/SIP/agent legs and transfers |
| Queue entry | queue service | one or more queue episodes per interaction; enqueue/dequeue reason |
| Routing attempt/offer/reservation | router/offer authority | multiple attempts; fence and terminal outcome per attempt |
| Agent assignment | interaction/agent state | accept, connect, hold, transfer, wrap-up and disposition intervals |
| Recording/transcript | recording/transcription | segment manifest and transcript revision, access policy |
| Schedule/forecast/adherence | WFM | agent/site/timezone, publication and observation revisions |
| Evaluation | QM | rubric/version, evidence span, evaluator, dispute |
| Event | producing aggregate | event id, aggregate version, event/record times, correlation |

Assign `interaction_id` at intake, carry it through SIP B2BUA call-id changes, media UUID, queue episodes, routing attempts, agent sessions and recordings. Preserve external IDs in a mapping table, not as the platform primary key. An event is a fact about a transition, not the entire current state; projections are rebuildable and include watermark/version.

## Time and metric semantics

Store UTC instants and original local time zone/offset for business calendars. Distinguish event time from ingestion time and correction time. Interval calculations use ordered authoritative transitions and clearly handle transfers, consult, multiple agents, reconnection and missing terminal events. Late events produce revisions with provenance; published dashboard queries expose `as_of`, watermark, data cutoff and metric-definition version.

| Metric | Example definition decision that must be published |
|---|---|
| Offered | count unique queue episodes admitted, or unique interactions? Separate these. |
| Answered | customer-agent media connected, agent accepted, or IVR answered? Define one explicitly. |
| Service level | eligible answered within threshold / eligible offered; define exclusions and interval allocation. |
| Abandon | customer leaves while waiting; short-abandon threshold and IVR exit exclusions explicit. |
| AHT | talk + hold + after-call work divided by handled assignments; consult/transfer allocation explicit. |
| Occupancy | handling time / (handling + eligible available time), by channel and concurrency model. |
| ASA | average wait among answered queue episodes; abandoned separately. |
| Forecast error | compare actual offered workload against frozen forecast version and interval. |
| Adherence | observed routing/presence state vs published schedule, with exception and lag policy. |
| Recording coverage | complete eligible recorded interactions / required interactions; partial and prohibited separate. |
| Transcript coverage | final eligible transcripts / eligible interactions, with model version and lag. |

Do not ship a dashboard named “service level” without the denominator, threshold, treatment of transfers/abandons and timezone. Live supervisor tiles and historical reports may temporarily differ due to late facts; expose reconciliation rather than quietly changing definitions.

## Data pipeline

`Owning service + transactional outbox → event backbone → validated schema → operational read model → warehouse/lake → governed semantic layer → dashboard/export/WFM/QM`.

Separate PII-restricted event topics from broad telemetry. Tokenize or minimize phone numbers; never put audio, payment data or raw transcript into generic logs. Backfill/replay uses source ids and versioned transformations, dedupe, DLQ, lineage and reconciliation totals. Operational history may need a durable command-side record independent of the event backbone. Analytical consumers can tolerate lag; routing reservations cannot.

## Workforce management

### Forecast

Inputs: offered volume by queue/channel/interval, handle-time distribution, seasonality, holidays, campaigns, callbacks, digital concurrency, service objectives, shrinkage and special events. Forecast stores assumptions, model/version, training cutoff, confidence interval and planner override. Volume and AHT uncertainty flow into staffing scenarios; Erlang C is an approximation for qualifying voice queue assumptions, not a universal omnichannel staffing model.

### Scheduling

Build schedules against staffing requirements, labor/contract rules, skill constraints, breaks, time off, site/timezone and fairness. Approval/publish is versioned; agents see the applicable schedule and supervisor edits have reason/audit. Offer shift swaps/voluntary time-off through explicit approval, not direct mutations of historical state.

### Intraday and adherence

Observe agent state transitions from the authoritative agent-state domain, compare with the published schedule, account for event lag and grace/exception policy. Intraday reforecast responds to actual demand and staffing. WFM may recommend capacity changes; only the agent-state/config authority changes routability. Do not penalize an agent because telemetry arrived late or an endpoint disconnected without reconciliation.

## Reporting and retention

RBAC/ABAC applies at row and field level, including export and scheduled report delivery. Record metric definitions, query version, source watermark and report generation time. Bound expensive queries and isolate compute. Apply retention/legal hold to interaction facts, audio, transcript, audit, backups and exports separately; deletion must traverse derived indexes and document exceptions. Regional data residency requires explicit pipeline and vendor placement, not just a storage-region setting.

## Cross-lifecycle data

`customer_id` is a verified profile link; `case_id` persists across contacts; `journey_id` persists across actions; `conversation_id` groups channel messages; `interaction_id` is one contact episode. Their authorities and merge/split provenance are specified in [customer journey and case](customer-journey-case.md). [Performance and quality](performance-management.md) consumes governed facts and evidence revisions; it cannot redefine routing state or overwrite agent history.
