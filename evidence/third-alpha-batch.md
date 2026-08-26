# Third alpha batch evidence record

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-08-26

This record documents the third independently researched NetCalcKit batch. Official Twilio Segment documentation and vendor-maintained code are used as primary evidence; no third-party blocklist was consulted as a source. Inclusion indicates an analytics or telemetry function, not maliciousness.

## Twilio Segment event ingestion

Official evidence:

- https://segment.com/docs/connections/sources/catalog/libraries/server/http-api/
- https://segment.com/blog/twilio-segment-edge-sdk/
- https://segment.com/docs/guides/regional-segment/
- https://github.com/segmentio/analytics-php/blob/master/lib/Consumer/ForkCurl.php

Segment documents its HTTP Tracking API as an event-collection interface. Segment's Edge SDK documentation shows analytics events being sent to `https://api.segment.io/v1/[method]`, and its vendor-maintained PHP client sends batches to `api.segment.io/v1/batch`. Regional Segment documentation identifies `events.eu1.segmentapis.com` as the EU regional ingestion host.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `api.segment.io` | Customer-data analytics/telemetry | Exact standard Segment Tracking API event-ingestion host | Moderate: blocks Segment event delivery; an application that incorrectly treats analytics delivery as required could degrade, but Segment login and management hosts are not blocked | Include for alpha testing |
| `events.eu1.segmentapis.com` | Customer-data analytics/telemetry | Exact Segment EU regional event-ingestion host | Moderate: blocks EU regional event delivery; account management uses a separate host, but applications with a hard dependency on telemetry success still require testing | Include for alpha testing |

## Independent network verification

On 2026-08-26, both hostnames returned IPv4 DNS answers from the primary workstation and the separate Ubuntu host `my-home-server`. HTTPS root requests from the Ubuntu host reached both services and returned HTTP 404, which is consistent with reachable API hosts receiving requests without a valid ingestion path or payload.

These observations confirm current DNS resolution and service reachability only. They do not prove application compatibility or that every Segment customer uses these vendor endpoints; first-party proxy configurations can use customer-owned hostnames.

## Scope controls

- No Segment vendor apex, dashboard, login, CDN, settings, or public-management API hostname is included.
- No wildcard or customer-owned first-party collector is included.
- No third-party aggregate list was consulted or imported.
- The rules target exact vendor-documented ingestion hosts only.
- Both rules remain subject to isolated application testing and immediate removal if a material false positive is confirmed.
