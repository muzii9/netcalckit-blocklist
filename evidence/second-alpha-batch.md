# Second alpha batch evidence record

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-08-25

This record documents the second independently researched NetCalcKit batch. Official vendor documentation is used as evidence; no third-party blocklist was consulted as a source. Inclusion indicates an analytics or telemetry function, not maliciousness.

## New Relic Browser monitoring

Official evidence:

- https://docs.newrelic.com/docs/browser/new-relic-browser/getting-started/compatibility-requirements-browser-monitoring/
- https://docs.newrelic.com/docs/browser/new-relic-browser/configuration/proxy-agent-requests/

New Relic documents `js-agent.newrelic.com` as the browser-agent script host. Its compatibility documentation lists `bam.nr-data.net`, `bam-cell.nr-data.net`, and `bam.eu01.nr-data.net` as exact browser payload destinations for US and EU account types.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `js-agent.newrelic.com` | Browser performance monitoring | Exact New Relic browser-agent script host | Moderate: prevents the monitoring agent from loading; exact service host only | Include for alpha testing |
| `bam.nr-data.net` | Browser telemetry | Exact standard US browser payload host | Low to moderate: blocks monitoring payloads; exact service host only | Include |
| `bam-cell.nr-data.net` | Browser telemetry | Exact US cellular-account payload host documented by New Relic | Low to moderate: blocks monitoring payloads; exact service host only | Include |
| `bam.eu01.nr-data.net` | Browser telemetry | Exact EU browser payload host documented by New Relic | Low to moderate: blocks monitoring payloads; exact service host only | Include |

## Datadog Real User Monitoring

Official evidence:

- https://docs.datadoghq.com/real_user_monitoring/
- https://docs.datadoghq.com/integrations/content_security_policy_logs/

Datadog documents its browser-intake domains as destinations for Real User Monitoring, Session Replay, browser logs, and Content Security Policy reports. This conservative batch includes the primary US1 and EU1 intake hosts only.

| Hostname | Category | Product and relationship | False-positive assessment | Decision |
| --- | --- | --- | --- | --- |
| `browser-intake-datadoghq.com` | Browser analytics/telemetry | Exact Datadog US1 browser-intake host | Moderate: blocks RUM, replay, browser logs, and related telemetry sent to this host | Include for alpha testing |
| `browser-intake-datadoghq.eu` | Browser analytics/telemetry | Exact Datadog EU1 browser-intake host | Moderate: blocks EU RUM, replay, browser logs, and related telemetry | Include for alpha testing |

## Independent network verification

All six candidates resolved successfully from both the primary workstation and the separate Ubuntu host `my-home-server`. HTTPS root-path responses were consistent across the two environments:

- New Relic: 200, 403, or 404 depending on the exact service host.
- Datadog browser-intake hosts: 403.

These root-path responses confirm reachable dedicated services, not application compatibility.

## Scope controls

- No vendor apex domain is included.
- No wildcard rule is included.
- No dashboard or account-management hostname is included.
- No third-party aggregate list is imported.
- Mixpanel, PostHog, Sentry, and customer-owned collector candidates remain excluded until an exact broadly applicable hostname passes the same evidence standard.
- Each rule remains subject to isolated DNS enforcement testing and immediate removal if a material false positive is confirmed.
