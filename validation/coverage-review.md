# Capability review and remaining proof

This review compares the **classes of capability expected of a full CCaaS product** to this repository's current architecture. It deliberately does not treat documentation as implementation. All rows are `designed`; a future build must advance status using the [acceptance matrix](architecture-acceptance.md). The review is internal and product-neutral.

| Capability family | Before this review | Current design location | Remaining proof |
|---|---|---|---|
| Voice edge/media/ACD/HA | detailed design | [voice](../architecture/logical-architecture.md), [legs](../architecture/call-leg-ownership.md), [routing](../architecture/routing-policy-engine.md) | interop, load, failures |
| Admin/supervisor/agent | broad design | [workspaces](../architecture/admin-supervisor-agent.md), [contracts](../architecture/service-contracts.md) | runnable RBAC, UI, state reconciliation |
| Digital/outbound/callback | broad design | [channels](../architecture/digital-outbound.md) | provider delivery, consent and pacing tests |
| Recording/transcript | detailed design | [evidence](../architecture/recording-transcription-quality.md) | media segment, gap and redaction tests |
| Reporting/WFM/QM | broad design | [data/WFM](../architecture/data-reporting-wfm.md), [performance](../architecture/performance-management.md) | semantic reconciliation, backtest, calibration |
| Customer profile/case | catalog mention only | [profile and case](../architecture/customer-journey-case.md) | identity, SLA, cross-channel and sync tests |
| Journey/notifications | catalog mention only | [journey](../architecture/customer-journey-case.md), [worked flow](../call-flows/cross-channel-journey.md) | consent/contact-cap and dedupe tests |
| Flow designer/bot/assist | catalog mention only | [automation](../architecture/automation-ai-knowledge.md) | simulation, tool guard, human fallback, model evaluation |
| Knowledge/content | catalog mention only | [knowledge](../architecture/automation-ai-knowledge.md) | scoped retrieval, version/citation and no-answer tests |
| Developer/partner/usage | catalog mention only | [developer platform](../architecture/developer-platform.md) | contract, webhook, sandbox and billing reconciliation |
| Physical topology and build sequence | partial voice topology | [deployment](../architecture/deployment-blueprint.md), [stages](../implementation/build-sequence.md) | selected workload/topology, deployment and DR drill |

## Coverage does not mean equivalence

Features differ in depth, configuration, ergonomics and operational maturity across implementations. This architecture names logical responsibilities and contracts; it cannot establish parity with a shipping product, security certification, legal compliance, usable agent experience or measured reliability. Product-specific comparison belongs in a private evaluation process, not in this repository. Maintain a deployment gap ledger of selected feature, owner, status, evidence, unresolved risk and target release.

## Next concrete repository milestone

Implement the first [voice vertical slice](../implementation/build-sequence.md) with an executable SIP/media/queue/agent path and synthetic call evidence. The architecture now has enough seams to avoid burying profile, case, WFM, reporting and AI behavior inside that first call-control codebase. Do not mark subsequent families complete until their own tests run.
