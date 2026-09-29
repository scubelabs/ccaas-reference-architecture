# Migration strategy: incumbent CCaaS to controlled cutover

Migration is a sequence of independently reversible capabilities, not one “move all calls” event. Inventory the incumbent's routing, numbers, recordings, reports, workforce processes and integrations before selecting traffic. The legacy platform remains the authority for traffic it still owns; avoid two systems believing they own the same DID, agent reservation or interaction.

## 0. Discovery and baseline

Capture tenant/business-unit/queue/skill hierarchy, agent identities, numbers and porting lead times, carrier contracts, SIP traces, IVR graphs/prompts, time zones/holidays, routing rules, SLAs, campaigns/callbacks, digital channels, recording/consent/retention, QM/WFM definitions, APIs/webhooks, reporting metrics, PCI/PHI boundaries, support runbooks and peak/burst traffic. Classify each feature as parity required, changed by design, deferred or retired. Build a reconciliation ledger mapping legacy ids to new ids and a gap register with owner and acceptance evidence.

## 1. Read-only foundation and shadowing

Establish identity and config import, event/correlation mapping, observability, synthetic probes, and dashboards. Mirror or shadow routing decisions without delivering duplicate offers. Compare eligibility/rank decisions using identical input snapshots and explain divergences. Replay historical events into reporting/WFM projections in a separate environment; compare metric definitions, not just totals. Never duplicate live customer recordings without consent/policy.

## 2. Lab and internal pilot

Certify carrier SIP/SDP/DTMF, TLS/SRTP, WebRTC/ICE/TURN, codec, caller ID, transfer/conference, failover and recording under controlled numbers and test accounts. Pilot internal agents and one low-risk queue with feature flags. Test customer and agent audio both ways, prompt/DTMF, callback, disposition, transcript, recording completeness, report reconciliation, WFM adherence and supervisor intervention. Include negative tests and rollback drills.

## 3. Traffic migration slices

| Slice | Cutover mechanism | Rollback precondition |
|---|---|---|
| Outbound test destinations | new trunk/route for allowlisted destinations | old carrier route remains eligible, attempt reconciliation |
| Inbound pilot DIDs | carrier routing or ported pilot numbers | documented carrier reversal; porting may not be instantly reversible |
| Queue/business unit | versioned entry policy and agent assignment | no dual reservation; legacy path and capacity retained |
| Digital channel | provider webhook/route change | preserve provider event ids, conversation ownership and idempotency |
| Recording/reporting | policy and data pipeline by tenant/queue | retain required legacy access and legal holds |
| WFM/QM | parallel forecast/schedule/evaluation period | agreed metric and schedule source of truth |

Ramp 1% → 5% → 25% → 50% → 100% only as illustrative stages; actual gates depend on volume and risk. At each stage compare answer/abandon, setup latency, one-way audio, RTP quality, routing conflict, recording coverage, transcript latency, report variance and support tickets. A stage cannot pass solely because calls connect.

## Number porting and carrier cutover

Maintain an authoritative DID ledger with current owner, target carrier, emergency address/location obligations, CNAM/STIR-SHAKEN treatment where applicable, routing destination, expected cutover window, validation calls and rollback contact. Differentiate routing change from irreversible/slow porting. Freeze conflicting config, lower TTL only where it actually controls routing, schedule staffed carrier bridges, validate inbound from multiple originating networks and outbound caller ID, verify toll-free/emergency paths under approved test procedure, and retain escalation evidence. Never place live emergency test calls without agreed carrier/public-safety procedure.

## Agent and data migration

Identity mapping prevents duplicate agents. Freeze or version skill/queue changes during a wave; train agents on device permissions, state, consult/transfer, recording indicators and incident escalation. Backfill historical interaction metadata with source provenance and watermarks; keep immutable legacy recordings in their governed store or migrate with checksums, chain of custody, access controls, retention and legal-hold mapping. Do not combine old/new metric series until definitions are harmonized and the dashboard labels the cutover boundary.

## Go/no-go, rollback and hypercare

Each wave has named decision owner, preflight checklist, tested rollback, observation window and stop thresholds. Go requires protected capacity, carrier readiness, synthetic paths, dashboard/alerts, on-call staffing, recording and event durability, privacy controls, WFM/supervisor readiness and a verified route back. Rollback stops **new admission** to the new stack, preserves or drains established calls according to state, reconciles callbacks/outbound attempts to prevent duplicates and checks recordings/history. Hypercare samples call media and records daily reconciliation by queue/tenant; exit only after agreed stability and support handoff.

## Evidence artifacts

Keep configuration versions, carrier order/port confirmations, test call IDs and packet/media evidence, synthetic results, canary metrics, capacity/drill reports, recording manifests, report variance with explanation, security approvals, rollback timestamps and customer impact. A migration wave is not “done” while a critical variance or missing recording remains unexplained.

## Product-domain migration beyond telephony

Migrate customer identity links, consent/preference records, open cases/tasks and SLA clocks with provenance; preserve old/new ids and split/merge reversibility. Shadow journey triggers and outbound contact caps before activation to avoid duplicate outreach. Import approved knowledge articles with permissions, locale and effective versions; compare bot/flow outcomes in simulation. Run parallel QM rubrics, WFM schedules/adherence and report metrics long enough to explain variances. Partner/webhook cutover uses source event ids and dedupe so both platforms do not send the same customer message or callback. Decommission only after legal holds, recordings/transcripts, exports, usage/billing and support access are reconciled. See the [capability map](../architecture/capability-map.md).
