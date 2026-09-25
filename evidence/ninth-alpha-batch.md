# Ninth alpha research batch — 2026-09-25

Research reviewed current first-party documentation for browser analytics and data-collection services. No hostname met the project's strict low-false-positive promotion threshold in this pass.

## Adobe Experience Platform

`edge.adobedc.net` is documented by Adobe as an Edge Network endpoint used for data collection. The same platform supports personalization, advertising, marketing, Analytics, and other Experience Cloud services. Because the hostname is mixed-purpose, it is not suitable for Standard promotion.

Evidence: https://developer.adobe.com/data-collection-apis/docs/endpoints/

## PostHog

`us.i.posthog.com` appears as the SDK `api_host` in official PostHog no-code web experiment documentation. The same host can serve feature-flag and experiment functionality alongside event analytics, so DNS-level blocking is mixed-purpose and risks application behavior. Staged on HOLD, not a Standard candidate. DNS health and application compatibility are not yet independently verified.

Evidence: https://posthog.com/docs/experiments/no-code-web-experiments

## Sentry

`o0.ingest.sentry.io` appears as an illustrative DSN ingestion hostname in Sentry's official SDK documentation. It is not proof of a universally active endpoint, and Sentry ingestion may carry essential error and crash diagnostics. Staged on HOLD; no promotion without resolving-host verification and compatibility testing.

Evidence: https://docs.sentry.io/platforms/javascript/enriching-events/attachments/

## Decision

- Newly staged candidates: 2 (both HOLD; PostHog mixed-purpose, Sentry diagnostics/illustrative endpoint)
- Standard promotions: 0
- Release-candidate PR: not created
- Main branch remains unchanged

This pass intentionally prioritizes false-positive safety rather than filling the research cap with weak candidates.
