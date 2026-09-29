# Architecture acceptance and proof matrix

A reference design is a set of testable contracts. This repository contains **designs only**; no production topology, API, carrier path, recorder or reporting stack is implemented here. Mark each capability `designed`, `implemented`, `lab-proven`, `load-proven`, `failure-proven` or `production-observed` separately. Do not promote one level based on a diagram.

| Capability | Architectural invariant | Minimum proof artifact |
|---|---|---|
| Inbound/outbound voice | tenant/number routing, bounded carrier attempts, distinct signaling/media | multi-carrier SIP ladder, two-way audio capture and failover classification |
| Agent routing | atomic reservation/fence, no duplicate offer across worker loss | concurrent reservation test, stale-fence rejection and reconciliation trace |
| IVR/self-service | version-pinned flow and bounded external dependency | prompt/DTMF/ASR test, timeout/fallback and publish rollback |
| WebRTC endpoint | ICE/DTLS-SRTP path and device readiness separate from SIP answer | candidate pair, stats and bidirectional audio on target networks |
| Digital channels | provider dedupe and single task ownership | duplicate webhook, retry, delivery unknown and reassign test |
| Callback/outbound | consent, time window, pacing, deduped attempts | timeout-after-commit/redial prevention and carrier throttling |
| Recording | policy decision, segment continuity, durable manifest | consent/pause/failure tests, checksum and gap report |
| Transcription | versioned provenance, redaction and partial status | source segment comparison, PII redaction and retry/DLQ evidence |
| Supervisor intervention | role, reason, consent, actual media result | unauthorized denial and monitor/whisper audit + media proof |
| Reporting | governed denominator and late-event reconciliation | raw-event-to-metric sample and watermark/variance report |
| WFM | forecast assumptions and published schedule/adherence versions | historical backtest, schedule exception and delayed-event test |
| Admin/config | validate/publish/canary/rollback and audit | incompatible config rejection, regional ACK drift and rollback drill |
| Tenant/security | row/field isolation, payload boundary and least privilege | cross-tenant API/export tests and threat-model findings |
| HA/DR | new admission vs active-session behavior declared | node/AZ/region drills, capacity envelope and RTO/RPO measurement |
| Migration | wave gates, number ledger and rollback | pilot evidence, route reversal, data reconciliation and hypercare signoff |

## Review questions

For each service: who owns writes; what is the source of truth; which endpoint/event schema exists; what times out; what can be retried; what happens when the response is lost; what customer experience results from a failure; how is state reconciled; what telemetry proves it; what policy changes across tenant/region/jurisdiction; how does it deploy/roll back; what capacity is needed in the defined failure domain? A blank answer is a design gap, not an implementation detail.

## Scenario suite

1. Two routers reserve the last available agent concurrently; one succeeds, one gets a conflict.
2. Accepted offer response is lost; retry returns the same attempt, and stale fence cannot bridge another interaction.
3. Region partition leaves both sides locally healthy; only one authority admits new work for an owned shard.
4. Media node dies mid-recording; call and recording are marked failed/partial with customer impact.
5. Event backbone fails after hangup; terminal facts reconcile without duplicate billing/reporting.
6. Recorder is mandatory but storage unavailable; policy-selected fail behavior is observable and tested.
7. Supervisor intervention is requested during transfer; role/consent and current leg are revalidated.
8. Reporting receives a late transfer event; historical revision and as-of watermark explain the change.
9. WFM schedule changes while agent has an active voice leg; adherence and routability remain independently correct.
10. Carrier pilot DID reroute fails; rollback of new admission and in-flight call accounting is demonstrated.

For detailed skill/proficiency/attribute routing, transfer, conference and leg-failure gates, see [routing and leg acceptance](routing-and-leg-acceptance.md).

## Additional product gates

| Capability | Minimum proof |
|---|---|
| Customer profile and case | ambiguous identity resolution, cross-tenant isolation, merge/split lineage, case SLA and external sync outage |
| Journey and notification | consent withdrawn between scheduling/delivery, contact cap, duplicate trigger and channel-switch handoff |
| Flow authoring and bot | graph validation, bounded loop/tool timeout, pinned version, human fallback and prompt-injection denial |
| Knowledge/assist | permission-filtered retrieval, article citation/version, no-answer behavior, feedback and model rollback |
| Performance/QM/surveys | rubric calibration, evidence revision, dispute, small-sample disclosure, survey dedupe and bias review |
| Developer ecosystem | scoped app install/revoke, webhook replay/signature, quota, sandbox isolation and version compatibility |
| Usage/entitlement | leg-level correction, transfer/conference reconciliation, quota transition and billing dispute trace |

The [build sequence](../implementation/build-sequence.md) orders these gates. Capability coverage is not evidence of implementation.

# External voice adapter acceptance

For every enabled external voice route, verify authenticated callback/WebSocket ingress, duplicate and out-of-order delivery, instruction deadline, ambiguous originate/transfer result reconciliation, stream gap and disconnect behavior, codec and bidirectional playback where used, consent-gated recording completeness, provider/local leg mapping, accurate queue/reservation/assignment metrics and call teardown. Test new-call routing under provider outage separately from established-call survival; do not infer one from the other. The [adapter design](../architecture/programmable-voice-adapters.md) defines the intended boundary.
