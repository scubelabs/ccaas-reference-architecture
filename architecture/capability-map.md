# CCaaS capability map and ownership

This is the platform's logical scope and completeness checklist. **Every row is designed, not implemented** in this repository. A deployment may combine services or integrate a specialist system; the ownership, contracts, failure behavior and evidence still need to be explicit. `Core` means required for a viable production voice contact center; `Expansion` means a capability should have an architectural seam before broader product adoption; `Conditional` applies when the business/regulatory use case exists.

| Domain | Capabilities and authoritative owner | Priority | Detailed contract |
|---|---|---|---|
| Tenant foundation | organization, sites, business units, hierarchy, quotas, localization — tenant/config | Core | [admin](admin-supervisor-agent.md) |
| Identity/security | SSO, MFA, RBAC/ABAC, service principals, sessions, delegated admin — identity | Core | [security](../security/privacy-controls.md) |
| Carrier/numbering | DID/toll-free inventory, porting, inbound/outbound routes, caller ID, emergency policy — number/carrier authority | Core | [carrier](multi-carrier-routing.md) |
| Voice edge | SBC, SIP proxy/registrar, overload, interop, fraud, TLS/SRTP — edge/signaling | Core | [voice](logical-architecture.md) |
| Media | bridge, IVR prompts, DTMF, hold, transfer, conference, transcoding, TURN/WebRTC — media/B2BUA | Core | [legs](call-leg-ownership.md) |
| Interaction | identity, participant graph, channel, lifecycle, queue episodes, assignments — interaction owner | Core | [data](data-reporting-wfm.md) |
| Routing | direct, skill/proficiency, attribute, priority, affinity, capacity, fallback, reservations — router/offer authority | Core | [routing](routing-policy-engine.md) |
| Agent endpoint | login, device/connection readiness, call/task control, notes, disposition, accessibility — agent gateway/workspace | Core | [agent](admin-supervisor-agent.md) |
| Supervisor | live queues/agents, intervention, coaching, freshness, escalation — supervisor gateway/authorized media | Core | [supervisor](admin-supervisor-agent.md) |
| Administration | flow/queue/skill/policy/prompt/number/user lifecycle, validate/publish/rollback — config owner | Core | [admin](admin-supervisor-agent.md) |
| Recording/compliance | consent, capture, pause, manifest, retention, playback, legal hold — recording owner | Core where required | [recording](recording-transcription-quality.md) |
| Event/data/reporting | durable facts, operational projections, semantic metrics, dashboards, export — event/analytics owners | Core | [data](data-reporting-wfm.md) |
| Diagnostics/SRE | end-to-end correlation, synthetics, SIP/SDP/RTP, capacity, incident response — observability/operations | Core | [observability](../observability/observability-architecture.md) |
| Digital | chat, email, messaging, social, attachments, provider delivery, concurrency — channel adapters/conversation | Expansion | [digital](digital-outbound.md) |
| Rich collaboration | video, screen share/co-browse, screen recording and secure file exchange — media/collaboration adapters | Conditional | [digital](digital-outbound.md), [privacy](../security/privacy-controls.md) |
| Outbound/callback | list/consent, pacing, preview/progressive/predictive mode, promises/retries — campaign/callback | Conditional | [outbound](digital-outbound.md) |
| Customer profile | identity resolution, consent, preferences, linked accounts, history — profile authority | Expansion | [journey/case](customer-journey-case.md) |
| Case/work item | case, tasks, SLA, ownership, escalation, cross-channel continuity — case authority | Expansion | [journey/case](customer-journey-case.md) |
| Journey orchestration | triggers, next action, cross-channel step, experiment/holdout, contact policy — journey authority | Expansion | [journey/case](customer-journey-case.md) |
| Flow/automation | graphical/versioned flow DSL, bot, tool calls, human handoff — flow runtime/automation | Core for IVR; Expansion for AI | [automation](automation-ai-knowledge.md) |
| Knowledge/agent assist | article lifecycle, search/retrieval, recommendations, provenance, feedback — knowledge/assist owners | Expansion | [automation](automation-ai-knowledge.md) |
| Transcription/analytics | ASR, redaction, sentiment/topic/rules, evaluation, alert — transcription/insight | Conditional | [recording](recording-transcription-quality.md), [automation](automation-ai-knowledge.md) |
| WFM | forecast, capacity plan, schedules, adherence, time-off, intraday — workforce owner | Expansion | [data/WFM](data-reporting-wfm.md) |
| QM/coaching | sampling, forms, evaluation, disputes, coaching, calibration — quality owner | Expansion | [quality](performance-management.md) |
| Performance/VoC | goals, balanced scorecards, surveys, improvement plans — performance/survey owners | Expansion | [performance](performance-management.md) |
| Integrations/developer | APIs, webhooks, sandbox, SDK, event schema, quotas and app lifecycle — developer/integration owner | Expansion | [developer](developer-platform.md) |
| Commercial operations | usage ledger, entitlement, billing export, tenant chargeback — metering/finance | Conditional | [developer](developer-platform.md) |
| Migration/DR | wave ownership, dual-run reconciliation, carrier cutover, rollback, recovery — migration/SRE | Core | [migration](../migration/migration-strategy.md), [DR](../reliability/degradation-and-dr.md) |

## Cross-cutting completeness rules

For every capability, name: actor and entitlement; source of truth; configuration/version; command/event contract; state machine; tenant and regional boundary; idempotency and ordering; timeout/degradation; data classification/retention; observability and freshness; scale/failure domain; migration path; test evidence. A feature card without these is a backlog idea, not an architecture contract.

The main interaction is not necessarily a call. It can span voice and digital contacts, cases, bot sessions, callbacks, transfers and follow-up tasks. `customer_id`, `journey_id`, `case_id`, `interaction_id`, `conversation_id` and `leg_id` have different lifetimes. Correlation links them without collapsing their authority into one mutable record.

## Capability dependencies and release sequence

1. **Foundation:** tenant/identity/config/audit, carrier/edge/media, interaction, queue/reservation, agent endpoint and diagnostics.
2. **Proven voice:** inbound/outbound, IVR, transfer/conference, recording, reporting and failure recovery at measured load.
3. **Operational breadth:** supervisor, admin publication, case/profile, digital adapters, callback/outbound, governed metrics.
4. **Workforce and experience:** WFM/QM, knowledge, automation, journey orchestration and authorized analytics.
5. **Platform ecosystem:** developer sandbox, partner integrations, usage/billing, optional advanced AI and multi-region/industry profiles.

The [implementation sequence](../implementation/build-sequence.md) turns these dependencies into build gates. Do not advertise a domain as available merely because its API shape is documented.
