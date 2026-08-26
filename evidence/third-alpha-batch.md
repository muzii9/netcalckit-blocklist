# Third alpha batch

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-08-26

This batch adds two Twilio Segment ingestion hosts. The sources below are vendor documentation and vendor-maintained code. These rules target analytics/telemetry endpoints; they are not being labeled as malicious.

## Twilio Segment event ingestion

Sources:

- https://segment.com/docs/connections/sources/catalog/libraries/server/http-api/
- https://segment.com/blog/twilio-segment-edge-sdk/
- https://segment.com/docs/guides/regional-segment/
- https://github.com/segmentio/analytics-php/blob/master/lib/Consumer/ForkCurl.php

Segment documents its HTTP Tracking API as an event-collection interface. Its Edge SDK documentation shows analytics events going to `https://api.segment.io/v1/[method]`, and the vendor-maintained PHP client sends batches to `api.segment.io/v1/batch`. The regional documentation lists `events.eu1.segmentapis.com` as the EU ingestion host.

| Hostname | Category | Why it is included | False-positive risk | Decision |
| --- | --- | --- | --- | --- |
| `api.segment.io` | Customer-data analytics/telemetry | Standard Segment Tracking API ingestion host | Moderate: blocks Segment event delivery; apps that wrongly depend on analytics delivery could misbehave, while login and management hosts are not blocked | Include for alpha testing |
| `events.eu1.segmentapis.com` | Customer-data analytics/telemetry | Segment EU regional ingestion host | Moderate: blocks EU regional event delivery; account management is separate, but apps with a hard telemetry dependency still need testing | Include for alpha testing |

## Network check

On 2026-08-26, both hostnames returned IPv4 DNS answers from the primary workstation and the Ubuntu host `my-home-server`. HTTPS root requests from the Ubuntu host reached both services and returned HTTP 404, which is expected for reachable API hosts without a valid ingestion path or payload.

This only confirms that the hosts currently resolve and are reachable. It does not prove app compatibility, and some Segment customers may use first-party proxy hostnames instead.

## Scope

- No Segment apex, dashboard, login, CDN, settings, or public-management API hostname is included.
- No wildcard or customer-owned first-party collector is included.
- No third-party aggregate list was imported for this batch.
- The rules are limited to the vendor-documented ingestion hosts above.
- Remove either rule if testing shows a material false positive.
