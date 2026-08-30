# Fourth alpha batch

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-08-30

This batch adds 50 exact analytics and observability hosts. Each group is supported by current vendor documentation. Every hostname returned active DNS through both the workstation resolver and the public Cloudflare resolver on 2026-08-30. No third-party blocklist was used as a source.

DNS resolution confirms that a documented host is active; it does not prove application compatibility. Remove or allowlist any rule if a material false positive is reproduced.

## Microsoft Clarity collection shards

Source: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-csp

Microsoft documents `a.clarity.ms` through `z.clarity.ms` as individual load-balanced hosts required when a site cannot allow `*.clarity.ms` in Content Security Policy.

| Hostname | Category and evidence | False-positive note |
| --- | --- | --- |
| `a.clarity.ms` | Documented Clarity analytics shard | Moderate: prevents Clarity collection routed to this shard; an incorrect hard analytics dependency could misbehave |
| `b.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `c.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `d.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `e.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `f.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `g.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `h.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `i.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `j.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `k.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `l.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `m.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `n.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `o.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `p.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `q.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `r.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `s.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `t.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `u.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `v.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `w.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `x.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `y.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |
| `z.clarity.ms` | Documented Clarity analytics shard | Moderate: same collection-only impact and hard-dependency caveat |

## Datadog browser monitoring regions

Source: https://docs.datadoghq.com/real_user_monitoring/

Datadog documents the regional Browser RUM intake hosts and the `quota.` hosts used only by Browser Profiling to check whether profiling is permitted.

| Hostname | Category and evidence | False-positive note |
| --- | --- | --- |
| `browser-intake-ap1-datadoghq.com` | AP1 browser RUM/replay/log intake | Moderate: disables Datadog browser observability for AP1 |
| `browser-intake-ap2-datadoghq.com` | AP2 browser RUM/replay/log intake | Moderate: disables Datadog browser observability for AP2 |
| `browser-intake-ddog-gov.com` | US1-FED browser RUM intake | Moderate: disables federal-region browser observability |
| `browser-intake-uk1-datadoghq.com` | UK1 browser RUM intake | Moderate: disables UK browser observability |
| `browser-intake-us2-ddog-gov.com` | US2-FED browser RUM intake | Moderate: disables federal-region browser observability |
| `browser-intake-us3-datadoghq.com` | US3 browser RUM intake | Moderate: disables US3 browser observability |
| `browser-intake-us5-datadoghq.com` | US5 browser RUM intake | Moderate: disables US5 browser observability |
| `quota.browser-intake-ap1-datadoghq.com` | AP1 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-ap2-datadoghq.com` | AP2 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-datadoghq.com` | US1 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-datadoghq.eu` | EU1 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-uk1-datadoghq.com` | UK1 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-us3-datadoghq.com` | US3 profiling quota check | Low to moderate: profiling may not start |
| `quota.browser-intake-us5-datadoghq.com` | US5 profiling quota check | Low to moderate: profiling may not start |

The documented government `quota.` candidates were excluded because they returned no active DNS during review.

## FullStory capture hosts

Source: https://help.fullstory.com/hc/en-us/articles/360020622854-Can-I-use-Content-Security-Policy-CSP-with-Fullstory

| Hostname | Category and evidence | False-positive note |
| --- | --- | --- |
| `edge.fullstory.com` | US capture script and connection host | Moderate: disables FullStory capture; hard agent dependencies still require testing |
| `rs.fullstory.com` | US event-reporting and image host | Moderate: disables reporting and related capture resources |
| `edge.eu1.fullstory.com` | EU capture script and connection host | Moderate: disables EU FullStory capture |
| `rs.eu1.fullstory.com` | EU event-reporting and image host | Moderate: disables EU reporting and related resources |

## Microsoft Application Insights telemetry

Source: https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/azure-monitor-network-access

| Hostname | Category and evidence | False-positive note |
| --- | --- | --- |
| `dc.applicationinsights.azure.com` | Global telemetry ingestion | Moderate: stops observability data; hard telemetry dependencies require testing |
| `dc.applicationinsights.microsoft.com` | Global telemetry alias | Moderate: stops telemetry using this alias |
| `dc.services.visualstudio.com` | Public-cloud agent telemetry | Moderate: stops agent telemetry; no Visual Studio apex is blocked |
| `live.applicationinsights.azure.com` | Live Metrics endpoint | Low to moderate: disables Live Metrics |
| `rt.applicationinsights.microsoft.com` | Live Metrics alias | Low to moderate: disables Live Metrics using this alias |
| `rt.services.visualstudio.com` | Live Metrics service alias | Low to moderate: disables Live Metrics using this alias |

## Scope and exclusions

- No wildcard rule, vendor apex, dashboard, login, payment, update, or management hostname is included.
- PostHog hosts were reviewed but excluded because the infrastructure can participate in feature-flag delivery.
- The moving `main` and immutable release subscription URLs are unchanged.
- These additions expand coverage; they do not establish universal application compatibility.
