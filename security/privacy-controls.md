# Security, privacy and trust-boundary design

This is an engineering control model, not legal or certification advice. Apply current jurisdiction/contract requirements with counsel, security and compliance owners. A CCaaS deployment processing PHI, payment data, customer audio and employee performance data has different access and retention obligations per data class.

## Trust boundaries and control ownership

| Boundary | Risk | Required design control |
|---|---|---|
| Carrier/PSTN ↔ SBC | spoofing, malformed SIP, toll fraud, overload | carrier identity/allowlist or mutual auth, parser normalization, rate/CPS, route policy, fraud limits |
| Browser ↔ agent gateway | stolen session, cross-tenant data, untrusted device | SSO/MFA, short-lived token, tenant/resource authorization, CSRF/CORS policy, device posture per deployment |
| Browser ↔ media/TURN | ICE abuse, media interception | DTLS-SRTP for WebRTC, short-lived TURN credentials, egress rules, candidate privacy, media metrics |
| Service ↔ service | lateral movement, forged events | workload identity, scoped mTLS/token, network segmentation, event provenance |
| Media ↔ recording/ASR | unauthorized audio fork, vendor egress | policy/consent token, regional placement, encryption, immutable manifest, explicit vendor boundary |
| Data ↔ report/export | bulk PII exfiltration | row/field ABAC, purpose, watermark, export limits, audit, retention |
| Admin ↔ configuration | malicious/accidental route change | draft/validate/approve/publish, dual control for sensitive changes, rollback, audit |

Security properties are end-to-end claims only when every boundary is tested. TLS at the edge does not mean SRTP remains encrypted through a PSTN gateway. Key ownership, termination points and lawful interception requirements are deployment choices.

## Data classes and treatment

Phone number/customer id, SIP/SDP, audio, recording, transcript, screen capture, payment, PHI, agent evaluation, secrets and packet capture have separate access and retention. Minimize raw payload in operational events and traces. Log hashed/tokenized identifiers when full values are unnecessary. Isolate raw packet capture and recording under purpose-scoped grants, short lifetime and access review. Secret references in config point to a secret manager; never deliver material through the admin read API. Define deletion across projections, search, analytics, vendor copies and backups with legal hold precedence and evidence.

The PCI SSC states that VoIP traffic containing payment account data is within applicable PCI DSS scope ([FAQ 1153](https://www.pcisecuritystandards.org/faqs/1153/)), and card validation values retained in digital audio after authorization violate its requirement ([FAQ 1210](https://www.pcisecuritystandards.org/faqs/1210/)). Use payment isolation, pause/resume verification and assessment with the responsible compliance team. A “pause requested” event is not proof sensitive audio was excluded.

## Recording and privacy

Consent/notice rules vary by location and participant; policy evaluates context at call start and after transfer/conference. Playback, transcript search and AI enrichment are separate purposes. Access grants should expire and be auditable. Do not use recording/transcript data to train external models absent explicit policy and contractual basis. Supervisor monitoring/whisper/barge has separate permissions and consent. Agent screen capture should be separately classified from voice recording.

## Fraud and abuse

Rate-limit auth, registration, dialing and API calls per tenant/user/carrier. Detect high-cost destinations, abnormal CPS/ASR/ACD, repeated short calls, answer-seizure anomalies, call pumping, spoofed caller ID and suspicious config changes. Emergency traffic and fraud blocking need carefully tested precedence. An automated block must have an override/escalation workflow and audit trail; no single heuristic is authoritative proof of fraud.

## Security verification

Threat model each call flow and external integration; test tenant isolation through list/search/export, privilege escalation, webhook signature replay, SIP malformed input, TURN credential expiry, recording grant revocation, key rotation, redaction leakage, retention/hold and emergency route policy. Pin supply-chain provenance and signed releases; scan dependencies and images; rehearse incident response and access revocation. Document evidence and exceptions rather than labeling the platform “compliant” by design.
