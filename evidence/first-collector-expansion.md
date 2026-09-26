# First collector expansion — exact-host research (2026-09-26)

Research candidates are **HOLD** until DNS health, false-positive/compatibility review, and human approval. First-party vendor documentation only; no third-party blocklist sourcing. Do not auto-publish.

## ping.chartbeat.net — Chartbeat web analytics collection

Primary documentation: https://docs.chartbeat.com/cbp/tracking/standard-websites/our-javascript

Chartbeat explicitly documents periodic requests to `ping.chartbeat.net` immediately after loading the independently hosted Chartbeat web tracker. Its pings register pageviews and send engagement, device, referrer, scroll-depth and click information. This exact host has a data-collection role distinct from `static.chartbeat.com` script delivery and `api.chartbeat.com` analytics dashboards/API.

Proposed scope: exact `ping.chartbeat.net` only (no apex or wildcard). Risk **moderate**: blocking intentionally disables Chartbeat analytics and can impair publisher-owned monitoring or analytics-dependent integrations; do not assume all Chartbeat-enhanced pages remain feature-equivalent. Core page-function smoke test and current DNS status still required before publishing.

## queue.simpleanalyticscdn.com — Simple Analytics event intake

Primary documentation: https://docs.simpleanalytics.com/events/server-side

Simple Analytics documents `https://queue.simpleanalyticscdn.com/events` for pageviews and custom event submission by server-side/mobile integrations; same event-queue hostname is referenced in its browser/proxy documentation: https://docs.simpleanalytics.com/events and https://docs.simpleanalytics.com/proxy .

Proposed scope: exact `queue.simpleanalyticscdn.com` only. Do **not** block the separate `scripts.simpleanalyticscdn.com` delivery host, custom first-party proxy domains, or the vendor's dashboard. Risk **low-moderate**: blocking intentionally prevents customer analytics and custom events; sites that make application logic depend on tracking acknowledgements could misbehave. Core page-function smoke test and current DNS status still required.

## Promotion gate

1. Confirm active DNS and absence from the allowlist and existing published rules.
2. Run candidate review, syntax/reproducibility validation and isolated DNS enforcement tests on a separate release-candidate commit.
3. Check likely customer-site breakage, document any exceptions and risk.
4. Only then propose `rules/rules.csv` entries and rebuild `blocklists/standard.txt` from the source database; publication requires explicit human merge approval.

Research alone does not establish universal app compatibility.
