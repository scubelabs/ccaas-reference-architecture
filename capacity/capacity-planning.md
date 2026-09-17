# Voice Capacity Planning

## Capacity is multi-dimensional

A CCaaS platform cannot be sized from concurrent calls alone. Signaling, media, routing and data services have different bottlenecks.

## Workload dimensions

| Dimension | Examples of affected systems |
|---|---|
| Calls per second (CPS) | SBC, Kamailio, FreeSWITCH call setup, routing |
| Concurrent dialogs | signaling state, memory |
| Concurrent RTP sessions | media tier, network |
| Codec/transcoding mix | CPU/media resources |
| Recording concurrency | storage/network/media |
| IVR complexity | media + external APIs |
| Concurrent agents | presence/state/WebSocket tier |
| Queue depth | ACD/state services |
| Routing decisions/sec | routing workers/state store |
| Events/sec | event backbone/consumers |
| Reporting queries | analytical/data systems |

## Erlang inputs

Traditional contact-center planning often uses offered load expressed in Erlangs:

```text
A = λ × h
```

where `λ` is arrival rate and `h` is average handling time in consistent units. Queueing models such as Erlang C can help estimate staffing/wait behavior under their assumptions, but infrastructure sizing still requires empirical component benchmarks and realistic traffic distributions.

## Burst behavior

Average CPS hides the conditions that break systems. Model busy-hour load, short bursts, retry storms, reconnect storms, campaign events, carrier reroutes and post-outage recovery.

## N-1 planning

If a pool has `N` nodes but must survive one node loss, target capacity must be evaluated against `N-1`, not `N`.

```text
required surviving capacity >= peak protected workload
```

For availability-zone or region failure, apply the same principle at the relevant failure-domain level.

## Media-specific constraints

Media nodes can be limited by CPU, NIC bandwidth, packets per second, file I/O, transcoding, recording, conferencing, encryption, kernel/network configuration, or external media services. Benchmark the actual feature mix; a pass-through call and a transcoded/recorded/conferenced call are not equivalent units of work.

## Headroom

Headroom is not wasted capacity. It absorbs traffic variance, node draining, rolling upgrades, autoscaling delay and failure displacement. The appropriate percentage is an engineering/business decision based on measured behavior and recovery targets; this repository does not invent a universal number.

## Load-test stages

1. Establish single-node baseline.
2. Identify first bottleneck and saturation signal.
3. Verify horizontal scaling behavior.
4. Test realistic codec/recording/IVR mix.
5. Test burst CPS separately from steady concurrency.
6. Remove a node under load.
7. Drain a node gracefully.
8. Test dependency degradation.
9. Test AZ/region failure assumptions where applicable.
10. Record safe operating envelope and alert thresholds.

## Output

Capacity planning should produce a documented envelope such as workload profile, protected peak, per-tier capacity, bottleneck, N-1 capacity, scaling trigger, scale-up time, operational headroom and tested failure mode—not merely a maximum-call marketing number.
