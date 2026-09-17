# CCaaS Failure Matrix

A production architecture should define behavior under failure before failure occurs. "Highly available" is not a component property; it is an end-to-end behavior produced by redundancy, failure detection, state design, routing policy, capacity headroom, and recovery procedures.

## Initial failure matrix

| Failure | New interactions | Established interactions | Primary detection | Architectural response |
|---|---|---|---|---|
| Carrier A unavailable | route via eligible alternate carrier where possible | typically carrier/path dependent | SIP failures, synthetic probes, carrier telemetry | withdraw/deprioritize carrier path |
| SIP edge node fails | other edge nodes accept traffic | depends on dialog routing/topology | health checks + traffic metrics | load balancer/DNS/routing removes node |
| SIP routing node fails | alternate signaling node handles new requests | established dialogs depend on Record-Route/state/topology | active probes + SIP metrics | health-aware dispatch / redundant route |
| Media node fails before answer | retry/reroute if transaction semantics permit | n/a | health checks, failed call setup | remove node; bounded retry |
| Media node fails during call | unaffected calls on other nodes continue | calls anchored on failed node generally lose media/session | node/media telemetry | isolate failure; customer recovery policy |
| ACD routing worker fails | another worker processes eligible work | established media should ideally not depend on worker liveness | worker health/queue lag | stateless/recoverable workers + durable/leased work |
| Agent-state store unavailable | routing may degrade/stop depending on consistency policy | connected calls should continue where possible | dependency health + latency/error metrics | fail safe; avoid routing from stale state |
| Durable DB unavailable | real-time routing may continue for bounded period if decoupled | established calls should continue | DB health + event backlog | buffer/event queue; reconcile later |
| Event backbone unavailable | call processing should degrade independently where designed | established calls continue | producer errors/backlog | local/bounded buffering or degraded mode |
| Observability stack unavailable | traffic should continue | calls continue | meta-monitoring | restore telemetry without coupling call path |
| Agent desktop disconnects | agent becomes ineligible after detection/lease expiry | active call behavior depends on media/device separation | heartbeat/WebSocket/device state | grace period, reconcile state, recovery UX |
| Availability zone loss | remaining zones absorb traffic if capacity permits | sessions on lost stateful/media nodes affected | infrastructure + synthetic telemetry | zone-aware placement/routing |
| Region loss | direct new traffic to surviving region if designed | active sessions in lost region generally cannot be transparently preserved | regional probes | DR/failover policy + capacity reserve |

## Important distinction: new vs established calls

A common architecture mistake is to say a component is "HA" because new calls can use another node. That does not imply established sessions survive failure.

For example, if FreeSWITCH anchors RTP and the process/node disappears, another FreeSWITCH instance cannot normally reconstruct the live RTP session simply because it has access to the same database.

Therefore each component must be evaluated separately for:

- **admission continuity** — can new work continue?
- **session continuity** — can existing work continue?
- **state recovery** — can control/data state be reconstructed?
- **customer recovery** — what does the user experience after loss?

## Retry safety

Retries are not universally safe. Before retrying a routing or call-control operation, define whether the operation is idempotent and whether the original attempt may have succeeded despite a lost response.

Example ambiguity:

```text
Routing Worker → reserve Agent 1001
                 reservation succeeds
                 response is lost
Routing Worker → timeout
Routing Worker → ??? retry ???
```

Without an idempotency key such as `interaction-id + routing-attempt`, a retry can create duplicate reservations or delivery attempts.

## Capacity implication

Failover is useful only if surviving infrastructure has enough capacity to absorb displaced traffic. Capacity planning should therefore model at least N-1 node/AZ conditions and, where required, regional DR load rather than only steady-state utilization.

## Next expansion

Each row will evolve into a failure scenario containing detection thresholds, state implications, recovery sequence, customer impact, observability signals, and test procedure.
