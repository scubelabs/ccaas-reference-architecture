# Deployment decisions to resolve before implementation

These are not gaps to fill with universal defaults. Record the chosen option, owner, rationale, test, rollback and date in a deployment-specific ADR. The repository's logical service model remains valid across choices, but concrete topology and compliance behavior may change.

| Decision | Why it changes architecture | Required evidence |
|---|---|---|
| Target tenants, channels, countries and jurisdictions | consent, outbound restrictions, emergency routing, data residency | legal/security review and channel/region matrix |
| Protected workload and objectives | node/AZ/region capacity, staffing, RTO/RPO and SLO budget | traffic trace, burst profile, benchmark, failure drill |
| Tenant isolation tier | dedicated media/data/keys vs shared pools and cost | cross-tenant test, threat model, noisy-neighbor load |
| Number ownership and carrier diversity | inbound failover/port rollback may be carrier-constrained | DID ledger, carrier contract and routed synthetic calls |
| SIP edge/media products and versions | interop, licenses, topology, codec and recording behavior | SIP/SDP/RTP matrix and failure benchmarks |
| Agent endpoint type and networks | WebRTC/TURN, native SIP, device/OS support | two-way audio/ICE and permission test matrix |
| Queue and reservation authority | atomicity, lease/fence, partition behavior | concurrent routing and stale-owner rejection |
| Event/state technologies | consistency, replay, outage buffering and costs | crash/duplicate/replay, saturation and RPO tests |
| Required recording failure mode | block/terminate/degrade choice per tenant and law | compliance approval and injected recorder failure |
| Retention/legal hold and AI vendors | storage/region, egress, transcript/search deletion | data-flow map, vendor terms and deletion test |
| Metric semantics and time zones | SLA/AHT/occupancy comparisons to incumbent | approved semantic dictionary and historical reconciliation |
| WFM method and labor rules | forecasting, scheduling constraints and adherence | planner signoff, backtest and exception review |
| Outbound dialer mode | consent, pacing, abandonment and jurisdiction rules | legal review and campaign simulation |
| Migration wave/rollback | port reversibility, dual ownership and hypercare | pilot call evidence and exercised rollback |

A decision is closed only when the implementation and proof are linked. “Use Kubernetes,” “use Redis,” or “add another carrier” is not a substitute for the associated state, failure and acceptance decisions.
