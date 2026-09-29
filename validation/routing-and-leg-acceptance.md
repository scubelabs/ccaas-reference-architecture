# Routing and call-feature acceptance matrix

This is a proof plan, not a claim that the repository implements a router or B2BUA. For every test record policy/config version, interaction/queue/attempt/leg ids, timestamps, SIP/SDP/ICE/RTP observations, agent state, recording segments, report facts and customer impact. Test both the intended result and safe recovery after injected failure.

| Test | Invariant / expected result | Evidence |
|---|---|---|
| Skill required vs preferred | unqualified agent never eligible; soft preference can relax only on approved edge | candidate exclusions and policy trace |
| Proficiency threshold and expiry | level below minimum or expired certification excluded despite idle time | skill-source version and reason code |
| Attribute missing/stale | declared fallback or no-route; no inferred hard match | provenance/TTL and decision trace |
| Longest idle and tie | deterministic outcome; reject/offer/wrap-up semantics match policy | idle ledger and scoring trace |
| Priority aging | high-priority SLA improves without unbounded low-priority starvation | distribution under sustained mixed load |
| Omnichannel capacity | chat/voice mix honors explicit capacity and one voice reservation | concurrent task/lease record |
| Two routers race | exactly one reservation fence wins | atomic conflict and retry trace |
| Worker crash/lost response | same attempt returns existing outcome, no duplicate offer | idempotency ledger and agent notifications |
| Region partition | stale owner cannot reserve or bridge | epoch/fence rejection and admission trace |
| Agent late accept | expired offer rejected; C remains recoverable | agent event sequence, C/A legs |
| Blind transfer target fails | C↔A preserved or declared fallback, no false complete | dialog/bridge state and interaction history |
| Attended consult canceled | B ends, C↔A restored, assignment unchanged | leg graph and media observations |
| Attended transfer completes | C↔B media confirmed before A release; I preserved | SIP/SDP/RTP, assignment/recording continuity |
| REFER/Replaces variant | target outcome, dialog mapping and recording policy validated | REFER/NOTIFY/Replaces ladder and new media path |
| Hold/resume | customer treatment and RTP direction correct; failed renegotiation leaves true state | SDP and per-direction RTP |
| Mute vs hold | local send disabled without falsely changing C hold | endpoint track and bridge state |
| DTMF | correct far-end digit with no forbidden logging | method trace and endpoint/IVR receipt |
| Conference joins/leaves | mixer carries permitted audio, participant graph and R match | RTP/mix, consent, segment manifest |
| Supervisor monitor/whisper/barge | audio recipients match mode; privilege/consent and audit hold | media test, denied test, audit trail |
| A/C/B disconnect mid-feature | terminal/recovery semantics, leases and recording reconcile | fault-injection timeline |
| Media node loss | active anchored legs fail as declared, no false seamless survival | customer impact and R partial status |
| Reporting after transfer | queue episodes, agent intervals, AHT and recording coverage follow definitions | raw-to-metric reconciliation |

## Gates

1. **Contract:** state machines, command schemas, ownership and idempotency tests.
2. **Single call:** two-way audio, signaling/SDP, RTP counters, recording and terminal event.
3. **Feature interop:** each command on every supported carrier/endpoint/codec combination; unsupported combinations explicitly blocked.
4. **Load and concurrency:** race, lease expiry, burst offers, multi-leg media/mixer/recording capacity.
5. **Failure:** worker/media/region/network loss during each transition, replay and reconciliation.
6. **Production canary:** synthetic and real-call sample with customer-visible SLOs, fairness, recording completeness and rollback.

An architecture feature advances from designed to lab-proven only with its corresponding artifacts. See the [overall acceptance matrix](architecture-acceptance.md).
