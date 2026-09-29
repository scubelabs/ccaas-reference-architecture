# Degradation, disaster recovery and operating modes

Declare behavior per **capability**, not a single platform availability percentage. The baseline topology does not preserve active RTP sessions on a lost media node or region. New admission and established-session continuity are different goals.

## Dependency policy matrix

| Dependency failure | New work | Established work | Correctness guard | Recovery evidence |
|---|---|---|---|---|
| Identity/SSO | new login denied or approved break-glass | existing session until expiry | no privilege expansion from stale token | access/audit reconciliation |
| Published config service | pin last-known-good within expiry | keep call-pinned version | no unvalidated draft activation | region ACK/version convergence |
| Queue/reservation authority | pause new offers, IVR fallback/callback | active bridge continues | never route on stale availability | lease sweep + interaction reconciliation |
| CRM/third-party lookup | IVR timeout/default branch | connected call proceeds | mark context unknown, avoid repeated unsafe writes | delayed task/outbox |
| Carrier path | eligible alternate for new attempts | existing carrier leg may fail | response classification and total retry budget | synthetic + real-call outcome |
| Media node | route new calls elsewhere | anchored calls likely drop | terminal outcome + recording gap | media inventory and customer impact |
| Recording control/storage | policy-specific block/degrade | follow mandatory/optional policy | no false complete artifact | segment manifest reconciliation |
| Transcription | queue bounded jobs | calls unaffected | partial/failed status, consent preserved | backlog age + DLQ replay |
| Event backbone | bounded outbox/buffer or pause if full | media can continue within policy | durable terminal facts and no silent loss | producer/consumer offset reconciliation |
| Reporting/WFM projection | stale views labeled | calls unaffected | no mutation from stale read model | watermark catch-up |
| Region partition | ownership-dependent admission pause | local media where alive | single writer/lease fencing | split-brain drill |

If a buffer fills, state what is shed first and whether call admission stops to preserve legally required records. A generic “fail open” rule is unsafe; tenant/regulatory policy selects the behavior.

## Regional design

Give each interaction and reservation a home region/owner epoch. Global ingress routes new calls to an eligible region with capacity; in-flight calls stay media-local. On partition, only the region holding valid authority may create new offers for an owned queue/agent shard. Fence old owners after failover. Replicate immutable configuration and durable events with measured lag; do not pretend asynchronous replication offers zero RPO. Design phone-number carrier reroute explicitly; DNS change alone may not move an inbound DID.

## Recovery objectives and runbook

Specify per capability: maximum new-call interruption, queue recovery, interaction event RPO, recording segment RPO, config promotion RTO, supervisor dashboard lag and historical reporting restore. Values remain deployment-specific until measured. A game day covers detect → declare → freeze changes → withdraw unhealthy routes → admit in surviving capacity → reconcile queue/agent/leg/recording state → validate synthetics → progressive failback → reconcile reporting and audit. Capture timestamps and customer impact; a successful process restart is not proof of call recovery.

## Capacity and release gate

Protect load at the failure size being promised (node, AZ or region) using actual codec/transcoding, recording, IVR, digital and event workloads. Canary a release with synthetic calls across carrier, IVR, queue, agent answer, media receipt, recording finalization and data projection. Roll back on customer-visible thresholds, not only CPU. Drain stateful media for planned maintenance and preserve config/schema compatibility during rolling updates.
