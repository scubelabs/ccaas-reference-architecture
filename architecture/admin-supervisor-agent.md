# Administration, supervisor and agent experiences

The three workspaces share identity and interaction APIs, but have different authority. A UI is never the authoritative agent, queue or call state. Server-side policies evaluate tenant, business unit, resource, purpose, geography and action at every command boundary.

## Administrative domain

| Capability | Authority and service | Controls and lifecycle |
|---|---|---|
| Tenant hierarchy | tenant/organization | tenant → business unit → site/team; inheritance rules, scoped delegation, quotas |
| Users and service principals | identity/provisioning | SSO/SCIM where applicable, MFA, role grants, joiner/mover/leaver, break-glass |
| Queues/skills/capacity | configuration + agent state | versioned queue membership, skill proficiency, concurrency and overflow |
| Routing policy | configuration/router | eligibility then ranking, priority aging, time zones, holiday, language, SLA, safe fallback |
| Number/carrier | inventory/edge | DID ownership, port state, trunk route, caller ID permissions, emergency rules |
| IVR and prompts | flow runtime/config | typed graph, bounded loops, prompt version, DTMF/ASR, external API budget, fallback |
| Digital channels | channel config | provider credentials, templates, consent, working hours, attachment policy |
| Recording/transcript | policy/control | jurisdiction/consent, pause/resume, retention, access, redaction, legal hold |
| Outbound/callback | campaign/callback | list/consent, pacing, quiet hours, retry/abandonment controls by jurisdiction |
| Integrations | integration service | scoped credentials, schema mapping, egress policy, signed webhook delivery |
| Workforce and QM | WFM/QM | calendars, schedule rules, evaluation forms, sampling and dispute permissions |

A draft cannot affect live traffic. Validation checks references (queue/skill/flow/number), graph reachability, policy cycles, missing prompts, unauthorized recording changes, route capacity and incompatible schema. Publication is an atomic pointer to an immutable version, with scope (tenant/site/percentage), activation time, approval policy, audit and runtime acknowledgments. A new interaction pins the version; in-flight calls do not silently change routing or IVR behavior. Rollback creates a new publication event pointing at a prior validated snapshot; keep history intact. Run synthetic calls and shadow policy evaluation before broad rollout.

## Agent workspace

Login establishes application identity and an agent session, not automatic routability. Readiness additionally requires assigned queues, schedule/policy eligibility, endpoint reachability and available capacity. The workspace shows independent connection, registration, media and routing states. On reconnect it requests a snapshot, then applies sequenced events; gaps trigger another snapshot. Commands are idempotent and display pending/acknowledged/failed states.

An agent can receive voice, digital and callback tasks; perform answer/reject/hold/mute/DTMF/consult/transfer/conference only if media and role capabilities permit; access customer context through scoped integrations; set disposition/notes; enter wrap-up; select devices; view recording/consent indicators; and report a technical issue with correlation id. Browser closure is not authoritative hangup or disposition. Accessibility covers keyboard navigation, readable live state, screen-reader announcements and device failure guidance.

## Supervisor workspace

Live queue and agent dashboards show **as-of time, ingestion watermark and stale-state indicator**. Metrics include waiting count/age, offers, accepts, abandonments, service level, occupancy and agent capacity by channel. Supervisor actions (change agent state, requeue, priority override, monitor/whisper/barge, takeover, schedule exception) require scoped permission, reason, interaction/agent id, optimistic concurrency and attributable audit. Media interventions require consent and jurisdiction policy; monitoring is a media action, not a flag toggled only in the UI.

Quality review offers consent-eligible playback, transcript version, evaluation form and coaching with dispute workflow. WFM provides forecast, published schedule, adherence and intraday adjustments. Historical reports are separate from live projections so late events can be reconciled without rewriting what the supervisor saw at the time.

## Privilege and approval matrix

| Action | Agent | Supervisor | Tenant admin | Compliance / security |
|---|---|---|---|---|
| Own call control/disposition | own active task | intervention per policy | no implicit media access | no implicit media access |
| Queue/skill draft | no | proposed change if delegated | edit | review if sensitive |
| Publish routing/IVR | no | no by default | approved publisher | audit access |
| Recording playback | limited case/purpose | assigned QA scope | no implicit access | explicit authorized scope |
| Export raw transcript/recording | no by default | no by default | no by default | purpose-scoped, audited |
| Change retention/consent | no | no | draft | approval/dual control where required |
| Break-glass | no | no | restricted | time-limited, reviewed, alerted |

A tenant admin is not automatically entitled to customer audio or PHI. All list/search/export paths enforce the same row and field rules as single-item reads. Integration service accounts get scoped rights and rotation, not a shared superuser token.

## Key failure cases

- Config published but one region does not acknowledge: stop ramp, keep its last-known-good version, surface drift; do not claim global activation.
- Supervisor sees a stale projection: disable or revalidate high-risk intervention against the authoritative owner.
- Agent desktop reconnects with a pending offer: server returns authoritative leg/offer state; stale button clicks fail by version/fence.
- Identity provider outage: existing short-lived sessions may continue per policy; new privileged changes fail closed.
- Audit sink outage: sensitive administrative mutation may be blocked; read-only and established media behavior is separately defined.
