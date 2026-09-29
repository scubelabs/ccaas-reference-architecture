# Cross-channel customer journey and case continuity

Scenario: a customer starts in self-service chat, fails an account action, requests a callback, talks to an agent, receives follow-up and submits feedback. This is a linked **journey**, not one long SIP call. IDs: journey `J1`, profile `P1` (only after verification), case `K1`, digital interaction `I1`, callback promise `CB1`, voice interaction `I2`, customer/agent legs `C2/A2`.

```mermaid
sequenceDiagram
  participant U as Customer
  participant D as Digital/bot
  participant P as Profile/consent
  participant K as Case/journey
  participant Q as Queue/callback
  participant M as Media/agent
  U->>D: Chat request
  D->>P: Verify identity and contact permission
  P-->>D: Verified scope + preferences
  D->>K: Create/update case K1 and journey J1
  D->>Q: Request callback CB1 in allowed window
  Q->>M: Reserve capacity + dial C2/A2
  M-->>K: Connected I2; link K1/J1
  M-->>K: Disposition and follow-up task
  K->>D: Eligible follow-up and survey
  D-->>U: Delivery receipt or unknown
```

## Authority and semantics

Digital adapter owns provider receipt and I1 conversation messages; profile service owns identity/consent; case service owns K1 state/SLA; journey service owns step ledger/suppression; callback service owns CB1 promise and attempts; interaction service owns I2; media owns C2/A2 and bridge; agent state owns reservation; survey owns eligibility/delivery. A case link does not grant the bot access to all profile fields. Handoff context includes verified identity level, last successful action, failed step, consent and cited knowledge source, with field-level authorization.

## Failure tests

- Bot times out after case creation: retry with same idempotency key; no second K1.
- Customer revokes phone consent before callback: cancel CB1 and suppress dial, even if scheduled earlier.
- Callback customer answers but agent does not: bounded retry, no “handled” metric, release capacity.
- Agent transfers I2: preserve K1/J1/I2 and add queue/assignment episodes and recording segments.
- Follow-up provider ACK is lost: reconcile by provider message id before resend.
- Profile match later proves incorrect: unlink with provenance and repair derived case/journey access without rewriting historical events.
- Recording is required but incomplete: case can remain open, recording status partial, survey policy evaluates separately.

## Reporting

Count unique I1 and I2 by channel; do not add them as one contact. Journey resolution can span both; case resolution follows K1's authoritative state. Callback promise completion requires connected customer-agent media, not a scheduled or attempted call. Report containment only if the bot completed the customer's goal without hidden human work; show denominator and sample definition. Survey response rate and operational SLA use their own clocks and watermarks.
