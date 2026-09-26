# First collector expansion — exact-host research (2026-09-26)

These two exact hosts are proposed for the Standard tier **in an unmerged draft release-candidate PR**, not yet published. First-party vendor documentation only; no third-party blocklist sourcing. Do not merge before the remaining compatibility review and explicit human approval.

## ping.chartbeat.net — Chartbeat web analytics collection

Primary documentation: https://docs.chartbeat.com/cbp/tracking/standard-websites/our-javascript

Chartbeat explicitly documents periodic requests to `ping.chartbeat.net` immediately after loading the independently hosted Chartbeat web tracker. Its pings register pageviews and send engagement, device, referrer, scroll-depth and click information. This exact host has a data-collection role distinct from `static.chartbeat.com` script delivery and `api.chartbeat.com` analytics dashboards/API.

Proposed scope: exact `ping.chartbeat.net` only (no apex or wildcard). Risk **moderate**: blocking intentionally disables Chartbeat analytics and can impair publisher-owned monitoring or analytics-dependent integrations; do not assume all Chartbeat-enhanced pages remain feature-equivalent. Core page-function smoke test is still required before publishing.

## queue.simpleanalyticscdn.com — Simple Analytics event intake

Primary documentation: https://docs.simpleanalytics.com/events/server-side

Simple Analytics documents `https://queue.simpleanalyticscdn.com/events` for pageviews and custom event submission by server-side/mobile integrations; same event-queue hostname is referenced in its browser/proxy documentation: https://docs.simpleanalytics.com/events and https://docs.simpleanalytics.com/proxy .

Proposed scope: exact `queue.simpleanalyticscdn.com` only. Do **not** block the separate `scripts.simpleanalyticscdn.com` delivery host, custom first-party proxy domains, or the vendor's dashboard. Risk **low-moderate**: blocking intentionally prevents customer analytics and custom events; sites that make application logic depend on tracking acknowledgements could misbehave. Core page-function smoke test is still required.

## Review evidence and publication gate

Both exact hostnames resolved to IPv4 addresses in GitHub's 2026-09-26 Candidate review workflow. The workflow and downloadable DNS report are at https://github.com/muzii9/netcalckit-blocklist/actions/runs/36259640757 . Both candidate CI and repository validation passed on the HOLD staging commit `4eca4eef8913a7a7750a75e8cb9122fe7fea7e74`.

After those results, a draft PR now proposes exactly the two reviewed hostnames as Standard rules and regenerates the list from `rules/rules.csv`. This is a release candidate, not publication. The new commit must pass rule validation and isolated AdGuard Home enforcement CI.

**Compatibility limitation:** vendor documentation and DNS health do not prove that every customer website remains unaffected when analytics are blocked. Before merging, review the remaining real-site/core-render smoke-test requirement or consciously document the unresolved moderate/low-moderate compatibility risk; investigate credible false-positive reports promptly.

Only the human maintainer may approve the draft release-candidate merge to `main`. The immutable tagged v0.2.0-alpha release remains unchanged.
