# Flow authoring, automation, knowledge and AI governance

Automation is an orchestrated participant in an interaction, not a direct substitute for media, routing or customer consent. Deterministic IVR and workflow behavior should continue when a model or external tool is unavailable.

## Flow lifecycle and runtime

A flow authoring service owns a typed, versioned graph: entry conditions; prompt/message; collect DTMF/speech/text; branch; external tool; queue; callback; bot handoff; terminal outcome. The editor has draft, validation, simulation, approval, canary and rollback. Validation checks unreachable nodes, cycles without bounded exit, missing localized prompts, unhandled timeouts, secret references, tenant/resource permissions, emergency paths, data boundary and worst-case execution budget. New interactions pin a published flow version; existing interactions do not silently switch versions.

The runtime stores `flow_instance_id`, interaction id, current node, input provenance, retry counters, config version and pending external operation. External tool calls have a deadline, idempotency key, schema validation and fallback branch. Human handoff carries verified identity level, intent/confidence, collected fields with consent, conversation summary provenance and failure reason. The agent sees what automation actually did; do not mark a task complete because a bot generated a response.

## Bot and agent-assist boundaries

| Capability | Owner | Output authority |
|---|---|---|
| Deterministic IVR/workflow | flow runtime | can perform approved actions with explicit schema/policy |
| Conversational bot | bot orchestration | may propose/execute allowlisted tools within scoped consent and budget |
| Knowledge search | knowledge service | returns authorized article/version/citation, not operational truth |
| Agent assist | assist service | suggestions, summaries, next-best-action; agent or approved automation owns final action |
| Real-time transcription | transcription service | provisional/final utterance with timestamps and confidence |
| Post-contact analytics | insight service | derived categories, sentiment/topic/silence and evaluation candidates |
| Rules/alerts | insight rules | versioned conditions and audited notification/task creation |

A prompt can contain untrusted customer speech or retrieved text. Tool permissions are independent of model output; validate parameters server-side, restrict egress, reject prompt-injection attempts, log decision provenance and require human confirmation for high-impact actions such as refunds, identity changes, recordings or dialing. Use a tenant/region/model allowlist and budget for latency, tokens and costs. Sensitive data can be processed only in an approved boundary; no raw transcript is sent to an arbitrary provider by default.

## Knowledge management

Articles have owner, tenant/business scope, locale, effective/expiry time, review state, version, source and permission label. The authoring workflow is draft → review → publish → archive. Search enforces entitlements **before** retrieval; answer generation cites article id/version and acknowledges no-answer/conflict. Feedback identifies stale or harmful suggestions for human review. A retrieval result must not be treated as verified customer data or a policy override.

## Model evaluation and operations

Version prompts, model, tools, retrieval corpus and redaction policy together. Maintain offline evaluation sets for intent accuracy, containment, hallucination/unsupported answer, tool misuse, language/accessibility, PII leakage, escalation correctness and latency. Canary/holdout experiments compare customer outcomes and agent burden; measure by segment and human review. Monitor drift, cost, failure and fallback. A rollback restores a prior approved bundle without erasing audit. Training-data use, retention and vendor access are separate approvals.

## Example failure paths

- ASR confidence low: repeat/DTMF/human branch; do not guess a payment or identity value.
- Model/tool timeout: cancel or reconcile tool outcome before retry; continue deterministic fallback.
- Knowledge article unpublished mid-session: pinned version remains explainable, but new answers use current policy.
- Transcript partial or redaction failed: disable broad search/assist and mark derived output incomplete.
- Bot handoff fails: preserve customer leg/conversation and queue/callback fallback with context, not an endless loop.
- Automation proposes a transfer to an unauthorized destination: media/control authority rejects independently of the bot.

## APIs and events (illustrative)

`POST /v1/admin/flows/{version}/simulate|validate|publish`, `POST /internal/v1/flows/instances/{id}/advance`, `GET /v1/knowledge/search?context=...`, `POST /v1/assist/{interaction_id}/feedback`, `POST /v1/automation/tools/{tool}/invoke` through a scoped broker. Emit `flow.node_entered/completed/failed`, `bot.handoff_requested/completed`, `knowledge.article_published`, `assist.suggestion_shown/accepted/rejected` and `automation.tool_outcome`. Never expose raw model/system prompts or secrets to the general agent API.
