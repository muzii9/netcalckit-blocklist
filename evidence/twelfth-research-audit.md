# Batch 012 — vendor endpoint review (2026-09-26)

Research-only. No new rules or automatic promotion. These observations use vendor primary documentation and require independent DNS/compatibility verification before any release candidate.

## Datadog — already covered; no duplicate

Vendor RUM documentation: https://docs.datadoghq.com/real_user_monitoring/

Official documentation lists regional browser-intake endpoints and additional `quota.browser-intake-*` Browser Profiling quota API hosts. All listed regional intake and quota hosts checked against main's rules database are already present. Do not stage duplicates. Note that browser-intake also carries server-side Product Analytics events: https://docs.datadoghq.com/api/latest/product-analytics/send-server-side-events/ . Existing approved rules should retain their documented false-positive risk and may warrant future compatibility audits.

## PostHog — HOLD, no new exact-host rule

Official documentation: https://posthog.com/docs/product-analytics/group-analytics and https://posthog.com/docs/experiments/no-code-web-experiments

The vendor documents `us.i.posthog.com` for event capture and SDK initialization, but also group identity/profile changes and experiments/feature flags. This is mixed-purpose; no safe dedicated tracking-only hostname identified. Existing batch 009 already researches PostHog; do not stage a duplicate.

## Sentry — HOLD, no new exact-host rule

Official docs: https://docs.sentry.io/api/projects/create-a-new-client-key/

Sentry's SDK DSNs use per-organization `o<id>.ingest.sentry.io` hosts, and the documented endpoint examples include errors, attachments, security reports, monitoring, and OTLP logs/traces. The DNS role is mixed-purpose and customer-specific; do not generate wildcard or synthetic exact hosts. Existing batch 009 researches Sentry; do not stage a duplicate.

## Result

0 newly staged candidates; 0 Standard promotions; 0 published-rule changes. Continue discovery for truly dedicated vendor-documented exact-host collectors and separately verify DNS, essential functionality, and compatibility. Research volume is not a reason to weaken the false-positive threshold.
