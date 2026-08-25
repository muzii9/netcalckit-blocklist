# Initial alpha evidence record

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-08-25

This record documents the first independently researched NetCalcKit rules. Official vendor documentation is used as evidence; no third-party blocklist was consulted as a source. Inclusion indicates an analytics or telemetry function, not maliciousness.

## Google Analytics

Official evidence: https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference

The Google Analytics 4 Measurement Protocol documents `https://www.google-analytics.com/mp/collect` as its standard collection endpoint and `https://region1.google-analytics.com/mp/collect` for EU collection.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `www.google-analytics.com` | Analytics/telemetry | Exact GA4 event-collection host documented by Google | Low to moderate: blocks analytics measurement; does not block a broad Google apex domain | Include |
| `region1.google-analytics.com` | Analytics/telemetry | Exact GA4 EU event-collection host documented by Google | Low to moderate: blocks EU analytics measurement; exact service host only | Include |

## Microsoft Clarity

Official evidence: https://learn.microsoft.com/en-au/clarity/setup-and-installation/clarity-setup

Microsoft's Clarity setup documentation identifies `https://www.clarity.ms/collect` as a POST collection endpoint used by Clarity.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `www.clarity.ms` | Behavioral analytics/telemetry | Exact Clarity collection hostname documented by Microsoft | Moderate: blocks Clarity collection and may also prevent resources served from the same exact service host | Include for alpha testing |

## Hotjar

Official evidence: https://help.hotjar.com/hc/en-us/articles/36820026388881-Content-Security-Policies

Hotjar's Content Security Policy documentation identifies `https://static.hotjar.com` and `https://script.hotjar.com` as script sources required for Hotjar.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `static.hotjar.com` | Behavioral analytics | Exact Hotjar script host documented by Hotjar | Low to moderate: prevents Hotjar loading; exact service host only | Include |
| `script.hotjar.com` | Behavioral analytics | Exact Hotjar script host documented by Hotjar | Low to moderate: prevents Hotjar loading; exact service host only | Include |

## Amplitude

Official evidence: https://amplitude.com/docs/apis/analytics/http-v2

Amplitude's HTTP V2 API documentation identifies `api2.amplitude.com` as its default event-ingestion host and `api.eu.amplitude.com` as its EU event-ingestion host. The user-facing `analytics.amplitude.com` host is deliberately excluded.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `api2.amplitude.com` | Product analytics/telemetry | Exact default event-ingestion host documented by Amplitude | Moderate: blocks event ingestion; applications that incorrectly depend on successful analytics delivery require testing | Include for alpha testing |
| `api.eu.amplitude.com` | Product analytics/telemetry | Exact EU event-ingestion host documented by Amplitude | Moderate: blocks EU event ingestion; exact service host only | Include for alpha testing |

## Scope controls

- No vendor apex domain is included.
- No wildcard rule is included.
- No third-party aggregate list is imported.
- User-facing Amplitude dashboard host `analytics.amplitude.com` is excluded.
- Each rule remains subject to live compatibility testing and immediate removal if a material false positive is confirmed.
