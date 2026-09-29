# From reference design to an executable CCaaS platform

The repository currently contains **architecture, contracts and proof plans**, not running services. Building all catalog capabilities at once would conceal correctness and interoperability failures. This sequence creates vertical slices with explicit go/no-go gates and avoids treating placeholders as implemented features.

| Stage | Build | Acceptance gate |
|---|---|---|
| 0. Foundation | mono-repo/service templates, tenant identity, config publication, schema registry, event envelope, observability, test harness | tenant isolation, idempotency, config rollback and trace correlation in CI |
| 1. Voice ingress | carrier test trunk, SBC/SIP routing, media/B2BUA, number inventory, WebRTC test endpoint | inbound/outbound two-way audio, SIP/SDP/RTP traces, fail/timeout classification |
| 2. Core interaction | interaction service, IVR flow, queue, atomic reservation, agent state/gateway/desktop | configure → call → IVR → queue → offer → answer → bridge → hangup → disposition; concurrency race and crash replay |
| 3. Voice features | hold/mute/DTMF, consult/blind/attended transfer, conference, callback, supervisor monitor | leg graph, media receipt, recording continuity and feature-failure tests across interop matrix |
| 4. Evidence/data | policy-controlled recording, segment manifest, event/outbox, timeline, governed reports | mandatory recorder failure behavior, no gaps mislabeled complete, raw-to-metric reconciliation |
| 5. Administration/operations | flow designer, policy validation/canary, roles, supervisor, capacity and SRE tools | draft/publish/rollback, stale-view intervention guard, N-1 load and incident drill |
| 6. Omnichannel/customer | digital adapters, profile/identity, case/task, journey and notifications | provider dedupe, cross-channel context handoff, consent/quiet-hour and case SLA |
| 7. Workforce/intelligence | WFM, QM, knowledge, transcription/assist, surveys | backtest, rubric calibration, model/human fallback, privacy and lineage |
| 8. Ecosystem/scale | API/webhooks/sandbox, usage/entitlement, multi-region and migration tooling | partner contract tests, usage reconciliation, region partition, carrier/number cutover drill |

## First executable repository milestone

A credible first milestone needs code and infrastructure artifacts, not an architecture diagram: `SIP carrier/test endpoint → SBC/proxy → media/IVR → queue/router/agent-state → agent WebRTC endpoint`, with one versioned admin config, one recording policy, one interaction timeline and an end-to-end synthetic call. Test valid call, no agent, invalid skill, agent late answer, one-way RTP, carrier failure, media failure, recorder failure and event-bus outage. Preserve SIP ladder, SDP, RTP counters, state transitions, config version and report facts as evidence.

## Engineering standards for each service

Each service ships a typed contract, owner, data schema/migration, idempotency and version behavior, tenancy authorization, threat model, health/readiness, SLO and saturation signal, runbook, load test, failure drill, compatibility test and deployment/rollback procedure. A service can be combined physically with another when a small deployment warrants it; logical write ownership remains explicit.

## Decision gates

Before coding a production stack, settle the deployment-specific [open decisions](../decisions/OPEN-DECISIONS.md): workload, region/jurisdiction, carrier/number, media engine and license, reservation store and partition policy, recording failure mode, privacy/retention and RTO/RPO. Those choices alter topology and test gates. Keep [capability status](../validation/architecture-acceptance.md) separate from source completion: designed → implemented → lab-proven → load-proven → failure-proven → production-observed.
