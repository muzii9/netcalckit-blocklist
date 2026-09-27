# Ninth research batch — PostHog and LogRocket

Date: 2026-09-27

## Scope
Exact-host research for analytics and session-replay services, with duplicate checks against published rules and held candidates.

## PostHog
- `us.i.posthog.com`
- Evidence: https://posthog.com/docs/experiments/no-code-web-experiments
- Official SDK configuration uses this as the PostHog `api_host`.
- It participates in analytics plus feature flags/session recording/experiments.
- Decision: **HOLD** because the endpoint is mixed-purpose and outside the low-false-positive automatic promotion gate.

## LogRocket
Evidence: https://docs.logrocket.com/docs/troubleshooting-sessions

Official CSP troubleshooting documentation names multiple script origins used by the recording SDK and wildcard connection origins. The evidence is strong for service attribution but not sufficient to infer every exact connection hostname from wildcard patterns.

Decision: **HOLD / further research**. Do not promote broad patterns or inferred hosts.

## Promotion decision
No newly reviewed candidate in this batch meets the strict automatic Standard promotion threshold. No release-candidate branch is prepared. Main remains unchanged pending human review.
