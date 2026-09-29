# Quality, workforce, performance and voice of customer

The platform must distinguish coaching and improvement from surveillance and metric gaming. WFM schedules, QM evaluation, customer feedback and performance scorecards use governed definitions with provenance, access policy and dispute/appeal workflow.

## Quality management lifecycle

`sampling policy → eligible interaction set → evaluation assignment → evidence review → scored rubric → calibration → agent acknowledgement/dispute → coaching action → follow-up`.

Sampling is versioned and stratified by queue, channel, agent cohort, risk and consent/recording eligibility. A rubric has criteria, weights, applicability, critical-fail rules and version. Evaluations reference recording/transcript revisions and evidence spans; corrections append revisions. Supervisors can review team-scoped interactions, while compliance access to sensitive recordings is separately granted. AI-generated scores are suggestions until validated and policy-authorized; record model version/confidence and human override. Calibration measures inter-rater disagreement and rubric drift.

## Workforce planning and intraday

Forecast volume and handle-time distributions by channel/queue/interval with cutoff, scenario assumptions, confidence and planner override. Translate demand into staffing while accounting for service objective, shrinkage, concurrency, skills/proficiency, breaks, labor rules and site constraints. A schedule is drafted, approved and published by version; time-off, shift trade and overtime are workflows with explicit ownership. Intraday management compares demand and staffing to the frozen plan, proposes changes and records agent/supervisor decisions. Adherence uses authoritative agent-state events and a watermark; a delayed event or technical disconnect must not become an unchallengeable employee violation.

## Performance scorecard and coaching

Scorecards can combine service, quality, customer outcome and operational metrics, but each metric shows definition, denominator, exclusion, data cutoff and sample size. Avoid ranking agents on a metric they cannot control, such as carrier one-way audio or a small survey sample. Goals are versioned and time-bounded. Coaching plans assign action, owner, due date and follow-up evidence. Optional recognition/gamification must not encourage unsafe speed, suppressed dispositions or skipped consent; permit opt-out where policy requires.

## Surveys and customer feedback

A survey policy chooses channel, eligibility, sampling, language, contact cap, consent and send window after the correct terminal event. Transfers and repeat contacts do not automatically trigger duplicates. Responses link to an interaction/case with explicit permission and anonymization options. Report response rate, non-response bias and confidence, not a single unqualified sentiment score. Negative feedback may create a case or supervisor task with deduplication and privacy controls.

## Interfaces and failure behavior

`GET /v1/qm/eligible-samples`, `POST /v1/qm/evaluations`, `POST /v1/qm/evaluations/{id}/disputes`, `POST /v1/wfm/forecasts/{id}/publish`, `POST /v1/wfm/schedules/{id}/publish`, `POST /v1/wfm/time-off`, `GET /v1/performance/scorecards?as_of=...`, `POST /v1/surveys/dispatch`. Every mutation is versioned/audited; reports include event watermark. If recording is partial, sampling excludes or labels it by policy. If WFM projection lags, adherence becomes provisional. If survey provider is down, delivery remains unknown until receipt/reconciliation; no duplicate retry without an idempotency key.
