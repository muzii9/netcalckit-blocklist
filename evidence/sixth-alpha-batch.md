# Sixth alpha candidate review — Cloudflare Web Analytics, Heap, Contentsquare

Reviewed: 2026-09-24

This record documents candidate research before any promotion into the published Standard list. Candidate triage scores are research-priority signals only; they do not auto-approve rules.

## Primary sources

### Cloudflare Web Analytics

Cloudflare documents the Web Analytics performance beacon at:

- https://static.cloudflareinsights.com/beacon.min.js

For sites not proxied through Cloudflare, beacon data is sent to:

- https://cloudflareinsights.com/cdn-cgi/rum

Sources:

- https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/
- https://developers.cloudflare.com/web-analytics/faq/

Assessment: both hostnames are dedicated to Web Analytics script delivery or beacon collection. Blocking can disable Cloudflare Web Analytics measurements but is not expected to be required for a site's core content. False-positive risk: low-moderate.

### Heap

Heap's current Web SDK documentation identifies:

- cdn.us.heap-api.com — US configuration/SDK script delivery
- cdn.eu.heap-api.com — EU SDK script delivery
- c.us.heap-api.com — US event collection
- c.eu.heap-api.com — EU telemetry/event collection

Heap Classic documentation also identifies:

- cdn.heapanalytics.com — Classic Heap.js and session-replay script delivery

The broader heapanalytics.com / eu.heapanalytics.com hosts also serve Visual Labeler resources and environment settings used by Heap customers.

Sources:

- https://developers.heap.io/docs/web
- https://developers.heap.io/docs/install-heapjs

Assessment:

- c.us.heap-api.com, c.eu.heap-api.com, cdn.us.heap-api.com, cdn.eu.heap-api.com, and cdn.heapanalytics.com are narrow SDK/collection hosts and remain promotion candidates.
- heapanalytics.com is held because it is a broad apex and also supports legitimate Heap tooling.
- eu.heapanalytics.com is held because blocking can affect Heap's Visual Labeler/admin workflow even though the host is vendor documented.

### Contentsquare

Contentsquare documents HTTP requests used for pageviews, events, cross-domain tracking, quota checks, Session Replay recording, and non-public resource collection.

Reviewed hosts:

- c.contentsquare.net — pageview and event collection
- t.contentsquare.net — main tracking tag
- csxd.contentsquare.net — Contentsquare-hosted cross-domain tracking iframe
- k-aeu1.contentsquare.net — Europe quota / advanced Session Replay collection
- k-aus1.contentsquare.net — US advanced Session Replay collection
- q-aus1.contentsquare.net — documented US quota endpoint
- srm.aa.contentsquare.net — Europe/Azure non-public resource collection
- srm.ba.contentsquare.net — Europe/AWS non-public resource collection

Sources:

- https://docs.contentsquare.com/en/web/
- https://docs.contentsquare.com/en/web/requests/
- https://docs.contentsquare.com/en/web/content-security-policy/

Assessment: these are dedicated analytics/session-replay infrastructure rather than broad vendor apex domains. Script and cross-domain hosts carry moderate breakage risk because poorly integrated sites may assume tracking code is present; collector-only hosts are lower risk.

## Automated candidate checks

GitHub Actions candidate review run:

- Run: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36039247526
- Candidate count: 17
- DNS health: 16 resolving, 1 no-address, 0 transport errors

The only no-address candidate in that run was:

- q-aus1.contentsquare.net

Because vendor documentation names q-aus1.contentsquare.net but current A/AAAA checks returned no address, it remains on hold rather than being promoted.

## Promotion set

Eligible for the next isolated enforcement / false-positive pass:

- c.contentsquare.net
- c.eu.heap-api.com
- c.us.heap-api.com
- cdn.eu.heap-api.com
- cdn.heapanalytics.com
- cdn.us.heap-api.com
- cloudflareinsights.com
- csxd.contentsquare.net
- k-aeu1.contentsquare.net
- k-aus1.contentsquare.net
- srm.aa.contentsquare.net
- srm.ba.contentsquare.net
- static.cloudflareinsights.com
- t.contentsquare.net

Held:

- eu.heapanalytics.com — legitimate Heap Visual Labeler/admin tooling risk
- heapanalytics.com — broad apex / mixed legitimate tooling
- q-aus1.contentsquare.net — vendor documented, but currently no A/AAAA address in CI

## False-positive policy

Promotion does not claim universal application compatibility. Exact hostnames are preferred, broad vendor apex domains remain excluded, and any credible report of login, payment, update, security, recovery, or core-site breakage takes priority over list growth.
