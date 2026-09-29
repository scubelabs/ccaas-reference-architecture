# Digital channels, outbound and callbacks

A common `interaction_id` and routing policy do not erase channel semantics. Voice has real-time media and exclusive capacity; email is durable and asynchronous; chat/messaging may be concurrent, ordered within a conversation and subject to provider delivery limits. Keep channel-specific receipt/consent/identity metadata in adapters and use a shared interaction envelope for queueing, agent assignment, history and analytics.

## Channel intake and identity

`Provider webhook/poll → authenticate/validate → dedupe provider_event_id → normalize tenant/channel/customer/conversation → policy/consent → interaction → queue → reservation → agent task → reply → delivery receipt → close/reopen`.

Each adapter verifies signatures or mutual trust, bounds payload/attachment size, scans content, stores opaque provider ids, handles provider retry semantics and maps delivery states without inventing ordering across providers. A conversation can span multiple interactions; a customer identity link is an explicit, reviewable match, not a phone-number equality assumption. Maintain suppression/opt-out and channel-specific retention. Email threading, chat inactivity timeout and SMS delivery failure need distinct state machines.

## Routing and concurrency

Eligibility uses tenant, queue, skill, language, schedule, capacity, channel and compliance. A voice offer may reserve exclusive voice capacity while the agent holds multiple chat tasks according to policy. A task assignment is versioned and fenced. For digital work, acknowledgement is distinct from customer delivery; reopening after agent timeout must not create two simultaneous agents replying without ownership transfer.

## Outbound voice

A campaign service owns list import/version, lawful basis/consent and suppression status, audience segmentation, time-zone/quiet-hour evaluation, pacing budget, agent availability, dial attempt and terminal result. The carrier edge owns SIP execution; the dialer does not bypass number and fraud policy. Preview, progressive and predictive modes require different pacing/abandonment controls; do not enable predictive dialing without jurisdiction-specific legal review and measurement. Caller ID authorization, emergency behavior and country rules must be deployment-specific.

An attempt key is `campaign_id + contact_id + attempt_number`; persist the outcome before retry. Unknown outcome after timeout requires reconciliation with media/carrier evidence before a redial. Maintain per-carrier CPS/concurrency, tenant budgets, retry delay, daily cap, exclusion and revocation of consent. Answering-machine detection and AI scoring are optional, measured capabilities, never assumed truth.

## Virtual queue and callback

A callback promise records customer number/verification, consent, requested window, timezone, queue/policy version, priority, max attempts and expiration. The callback worker reserves capacity or queues a callback interaction before dialing as policy specifies. Customer answer, agent answer and media bridge are separate events. If one party does not answer, release reservations, apply a bounded retry and disclose the final outcome. Duplicate event/retry must not create duplicate calls.

## Failure and reporting

Provider down: buffer within contractual limits, show delivery unknown, replay by provider id. Agent gateway down: task remains owned by queue/lease until reconciliation. Campaign pause: stop new admission and honor in-flight attempts. Reporting distinguishes initiated, delivered, accepted, connected, abandoned, failed and unknown; use event-time corrections and explicit denominators.

## Rich collaboration channels

Video, screen share and co-browse are separate media/collaboration adapters with participant consent, device permissions, session-scoped authorization and explicit capture policy. Co-browse should mask sensitive fields and restrict remote control; screen recording is a different data class from call audio and has its own retention and access. A transition from chat/voice to video preserves interaction/case correlation, but creates new media participants and quality metrics. These capabilities are conditional, not implied by the base voice topology.
