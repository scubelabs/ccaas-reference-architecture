# Programmable voice and media-stream adapters

This extends the [SIP-centered topology](logical-architecture.md) with two optional connection classes. A **media-stream fork** exports live audio from an externally anchored call for observation or bidirectional bot audio. A **programmable voice controller** receives call events, returns call-control instructions and may create, bridge, transfer, conference, record and stream calls on external infrastructure. Capabilities vary by provider/account/region and must be discovered, versioned and proven; neither class replaces the canonical interaction, routing, reservation, reporting or consent authorities.

No external voice platform is assumed to host our ACD. The platform chooses per tenant, number and route whether a call is SIP-anchored locally, externally anchored with programmable control, or locally anchored with an auxiliary audio fork. Never bridge a single interaction through both media anchors without an explicit leg topology and cost/recording review.

## Capability contract and boundaries

| Capability | SIP/local media adapter | External call-control adapter | Stream-only adapter |
|---|---|---|---|
| Customer leg signaling | local B2BUA owns dialog | external voice service owns leg; local adapter holds provider reference and observed state | underlying call owner retains signaling |
| Agent leg, transfer, conference | local B2BUA/bridge | external instruction/API if supported and proven; otherwise connect to local SIP ingress with a declared boundary | cannot claim call control from audio frames |
| Audio to observer | local media fork | provider stream/recording feature if supported | receives selected tracks, timestamps and stream status |
| Audio back to caller | local mixer/IVR | provider bidirectional stream or playback instruction if supported | only when session explicitly supports bidirectional audio; format and playback ACK contract |
| Routing/agent reservation | central router and offer authority | same central router and offer authority; provider is executor | no assignment authority |
| Recording/consent | platform recording policy plus local media | platform policy mapped to provider recording controls; reconcile manifest/download and hold | stream capture is not automatically compliant recording |
| Diagnostics | SIP/SDP/RTP plus media telemetry | provider events/API results and stream metrics; SIP internals may be unavailable | sequence gaps, jitter, timing, codec and stream disconnect only |

Suggested typed ports (illustrative): `VoiceIngressAdapter.admit(externalEvent, idempotencyKey)`, `VoiceControlAdapter.originate|answer|connect|hold|resume|transfer|conference|terminate`, `MediaStreamAdapter.start|stop|sendAudio|observe`, `RecordingAdapter.start|pause|resume|finalize`, and `ProviderCapabilityRegistry.resolve(tenant, region, operation)`. Commands return `pending` with `operation_id`; a correlated callback/leg observation advances actual state. An HTTP success, WebSocket upgrade or streamed audio frame is not proof that customer and agent are connected. The canonical model keeps `interaction_id`, `leg_id`, `attempt_id`, `provider_call_id`, `provider_stream_id`, `operation_id` and provider event ID separate.

## Flow A: audio fork alongside existing call control

1. Ingress admits call and creates interaction; SIP/local or external call controller remains responsible for customer leg and its lifetime.
2. Consent/recording policy and resource budget authorize a stream by purpose (`transcription`, `assist`, `bot`, `diagnostics`) and permitted direction/tracks. Start with the provider's track/codec constraints and a bounded WebSocket establishment deadline.
3. Stream gateway authenticates the handshake, binds a one-time token to tenant/interaction/leg/purpose, validates format, sequence and payload size, and publishes sanitized stream status. A media worker decodes/resamples for ASR or sends explicitly authorized audio back; keep generic event buses free of raw audio.
4. On disconnect, distinguish `stream_failed` from `call_ended`. Observation-only stream loss may degrade transcript/assist without dropping the call. If a bot is the sole audio path, call control applies a predeclared prompt/IVR/agent fallback, with a timeout. Required recording follows its separate fail-open/closed policy.
5. Stop/revoke stream on hangup, consent withdrawal, transfer policy boundary or region change. Reconcile late provider callbacks and byte/frame counts; do not mark transcript or recording complete because the socket closed normally.

## Flow B: external programmable call control

1. Signed/authorized inbound callback or an outbound originate request arrives at the provider adapter. Persist an inbox dedupe key and external account/application/leg mapping. Validate tenant and number/route before asking the interaction service to create a canonical contact. Return a safe, bounded provider instruction (for example, wait/prompt) while routing proceeds.
2. Flow/IVR may instruct gather, playback or stream; the provider owns the executing call leg. The queue and router still own episode and decision, and agent-state authority still atomically reserves capacity.
3. After a winning offer, call control requests a provider bridge/transfer/conference or connects the provider leg to a local SIP ingress, depending on capability. Maintain one explicit controller for each leg; a provider-hosted conference is not a locally owned RTP bridge. A customer-to-agent media observation, not an instruction response, marks the assignment connected.
4. Webhook/operation results update leg state idempotently; provider call IDs map to stable platform IDs. On transfer and consult, record each new provider/local leg and conference participant. Recording-policy changes at every participant/jurisdiction boundary; both native-provider and platform artifacts require manifest and access reconciliation.
5. End command and final callback may arrive in either order. Query ambiguous operations before retry; terminalize canonical interaction only after channel truth or an explicit reconciliation timeout/outcome. Continue callback/dialer, QM and reporting from canonical facts.

## Placement and fallback rules

| Option | Appropriate use | Operational limit |
|---|---|---|
| Local SIP/B2BUA anchor with observation stream | keep SIP/media leg and transfer authority while adding real-time transcription/assist | added egress, buffering and stream cost; stream outage should not silently end call |
| Externally anchored programmable call | rapid regional ingress, outbound/callback or external IVR/conference, with platform ACD ownership | provider controls actual legs/media; feature parity, detailed RTP diagnostics, failover and export need verification |
| Bidirectional bot stream | speech interaction before queue or during self-service | audio format/latency/interrupt handling and stream loss become customer-path dependencies |
| Provider leg to local SIP bridge | retain local agent/conference/recording features for selected calls | extra PSTN/SIP hop, codec/transcoding, consent and recording ownership must be explicit |

This is a per-route strategy, not an automatic live-call migration scheme. A failed external media anchor normally cannot be moved mid-call to a SIP anchor. Multi-carrier resilience concerns **new-call admission** and DID reachability, not guaranteed survival of established sessions. Do not replay an outbound originate merely because the API response timed out: query the provider mapping and reconcile first.

## Webhook, stream and data controls

- Authenticate inbound webhook and WebSocket handshake using the configured provider mechanism, scoped account and tenant mapping; use TLS/WSS, secret rotation, replay window, ingress rate limits and one-time correlation tokens. Do not assume the same signature scheme applies to every webhook family.
- Store raw inbound payload in a restricted, bounded retention diagnostic store only when policy permits; normalized event inbox is keyed by provider/account/event ID or a stable derived key. Handle retry, duplicate, late and out-of-order callbacks. Never trust a call ID supplied only by an audio message for privileged control.
- Negotiate permitted codec/sample rate and direction per adapter. Enforce frame/queue memory bounds, backpressure, audio pacing, playout acknowledgment, barge-in/clear semantics and max concurrent streams. Account for both observer tracks and outbound audio separately.
- Separate stream audio from durable recording. Policy determines consent, pause for sensitive segments, track labeling, redaction, retention, export and deletion. A transcript revision includes source stream/leg, gaps, model version and timestamps. Provider recordings require availability callback, checksum, encrypted ingestion and an incomplete state until verified.
- Isolate external API/webhook/stream pools from routing transaction pools. Meter connection attempts, stream minutes, ingress/egress bytes, ASR minutes, provider calls and duplicate delivery. Cap per tenant/region and shed optional observation streams before core call control.

## Event, store and failure contract

| Fact or state | Authority | Persistence and recovery |
|---|---|---|
| Provider account, route, capabilities and secret references | tenant/config and secret owners | versioned relational config; capability test results per region, never a global boolean |
| External callback/instruction result | provider adapter inbox/outbox | relational dedupe, raw reference, operation status; retry with same idempotency identity |
| Customer/agent leg status | executing local media or external provider, normalized by adapter | leg evidence event plus external ID mapping; reconcile against provider query if available |
| Stream connection and quality | stream gateway/worker | short-lived active socket state, bounded telemetry; append status/gap facts, never use Redis as sole call truth |
| Interaction/queue/offer/assignment | existing platform owners | unchanged authorities and transactional stores; provider never writes reservation or reporting aggregates |
| Recording/transcript/reporting | policy/ingest, transcription and governed metrics | verified object manifest and derived facts, provider IDs as provenance |

Provider outage cases: callback delivery failure uses bounded provider-specific response/fallback; API timeout is unknown outcome; WebSocket setup failure invokes purpose-specific degradation; delayed final event leaves `pending_reconciliation` with alarm; rate-limit/concurrency exhaustion stops new admission or sheds optional streams; event gaps mark diagnostics incomplete. Do not report external RTP metrics that are not actually exposed. A route health check must exercise ingress webhook, instruction response, endpoint bridge, two-way audio and teardown, not just HTTPS reachability.

## Adoption gates

1. Build a provider-neutral contract simulator with duplicate/out-of-order webhooks, hung API calls, stream stop, invalid signature, codec mismatch, rate limit and late hangup. Verify one canonical interaction and no duplicate originate/offer.
2. Implement one external call-control adapter or one observation stream adapter behind the port, with feature flags and per-tenant routing. Prove number admission, queue/reservation, agent connection, teardown and diagnostic timeline in a controlled test environment.
3. Add bidirectional audio only after latency, playout/clear, DTMF behavior, consent and fallback tests. Add transfer/conference/recording only when each leg and artifact reconciliation is verified.
4. Run load and failure drills, compare local and external route cost/quality/observability, document provider capability/version gaps and measured limits. A provider API document is design input, not interoperability evidence.

See [interaction ownership](interaction-ownership.md), [call-leg ownership](call-leg-ownership.md), [data stores](data-store-topology.md), [multi-carrier routing](multi-carrier-routing.md) and [service contracts](service-contracts.md).
