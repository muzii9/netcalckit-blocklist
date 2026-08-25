# Application compatibility test record

This document records controlled application-level comparisons. A passing row is evidence only for the exact application behavior and list hostnames actually exercised during that run.

## 2026-08-25 — Vendor-owned public-page batch

### Environment

- Six login-free, vendor-owned documentation or product pages
- Isolated headless Chromium on Ubuntu
- Comparison: normal resolver behavior versus a separate browser process mapping all 13 current NetCalcKit hostnames to `0.0.0.0`
- Seven-second observation window after each page load
- Host, router, normal client DNS, AdGuard Home, and Portainer settings: unchanged

### Results

| Public page | Current-list hosts requested in baseline | Comparison result |
| --- | --- | --- |
| New Relic Documentation | `js-agent.newrelic.com` | Title, heading, readable body, and internal-link threshold matched; preliminary core-render smoke pass. |
| Amplitude Documentation | `api2.amplitude.com` | Title, heading, readable body, and internal-link threshold matched; preliminary core-render smoke pass. |
| Google Analytics for Developers | `www.google-analytics.com` | Title, headings, readable body, and internal-link threshold matched; preliminary core-render smoke pass. |
| Hotjar product page (redirected to Contentsquare) | `static.hotjar.com` | Final URL, title, heading, readable body, and internal-link threshold matched; preliminary core-render smoke pass. |
| Datadog Documentation | `browser-intake-datadoghq.com`, `static.hotjar.com`, `www.clarity.ms`, `www.google-analytics.com` | Title, heading, and readable-body length matched. The generic internal-link threshold failed in both baseline and blocked modes, so this row is render-only evidence rather than a full core-render pass. |
| Microsoft Clarity Documentation | none | Page checks passed, but the run exercised no current rule and provides no rule-level evidence. |

The blocked comparison produced the same titles, headings, and body-character counts as baseline for all six pages. Expected severe browser-console network errors increased on pages that requested mapped telemetry hosts; no claim is made that every console error was caused by NetCalcKit.

### Coverage classification

Six of the 13 rules were observed in baseline network logs:

- `api2.amplitude.com`
- `browser-intake-datadoghq.com`
- `js-agent.newrelic.com`
- `static.hotjar.com`
- `www.clarity.ms`
- `www.google-analytics.com`

Four rules have a **preliminary core-render smoke pass** from a page that exercised the hostname:

- `api2.amplitude.com`
- `js-agent.newrelic.com`
- `static.hotjar.com`
- `www.google-analytics.com`

Two rules are **render-only exercised**, not passed:

- `browser-intake-datadoghq.com`
- `www.clarity.ms`

Seven rules remain unexercised in application-level testing:

- `api.eu.amplitude.com`
- `bam-cell.nr-data.net`
- `bam.eu01.nr-data.net`
- `bam.nr-data.net`
- `browser-intake-datadoghq.eu`
- `region1.google-analytics.com`
- `script.hotjar.com`

A preliminary smoke pass is not broad compatibility clearance. It covers public-page rendering and basic navigation presence only; it does not cover authentication, dashboards, forms, payments, media, account settings, or private applications.

## 2026-08-25 — NetCalcKit website smoke test

### Environment

- Public site: `https://netcalckit.com/`
- Browser: isolated headless Chromium on Ubuntu
- Comparison: baseline resolver behavior versus a separate browser process mapping all 13 current NetCalcKit hostnames to `0.0.0.0`
- Host, router, and normal client DNS settings: unchanged

### Results

| Check | Baseline | 13-host blocked mode |
| --- | --- | --- |
| Page title and main heading | Pass | Pass |
| Featured calculator: 1 GB at 100 Mbps | Pass — 1m 20s | Pass — 1m 20s |
| Calculator search for IPv4 | Pass | Pass |
| Severe browser-console errors | None observed | None observed |

### Rule coverage

The browser network log did not show a request to any of the 13 current list hostnames during this run. Therefore:

- the application smoke test passed;
- no false positive was observed;
- zero rules received rule-level evidence from this run.

A site loading successfully while it does not exercise a listed hostname cannot prove that blocking that hostname is safe.

## Next coverage targets

Future runs should prioritize the seven unexercised regional or collector-specific hostnames and deeper feature tests for the six exercised rules. Authentication, private user data, payments, and destructive actions must not be used merely to increase coverage.


## 2026-08-25 — Regional collector testability review

Official vendor documentation confirms that the seven currently unexercised hostnames are specialized analytics resources rather than general application backends:

| Hostname | Officially documented role | Why public-page coverage is limited |
| --- | --- | --- |
| `api.eu.amplitude.com` | Amplitude EU event ingestion | Requires an Amplitude project configured for EU data residency. |
| `bam.nr-data.net` | New Relic standard US browser payload collector | Collector selection depends on an instrumented application's New Relic account and agent configuration. |
| `bam-cell.nr-data.net` | New Relic US cellular-account browser payload collector | Account-specific collector; a generic public page cannot reliably force selection. |
| `bam.eu01.nr-data.net` | New Relic EU browser payload collector | Requires an EU New Relic browser-monitoring configuration. |
| `browser-intake-datadoghq.eu` | Datadog EU1 RUM/browser intake | Requires a Datadog RUM application configured for the EU1 site. |
| `region1.google-analytics.com` | Google Analytics EU collection endpoint | Requires an implementation explicitly using the regional collection URL. |
| `script.hotjar.com` | Hotjar script/font/style resource host | Vendor pages observed `static.hotjar.com`, but did not naturally request this second resource host during the test window. |

Sources:

- [Amplitude HTTP V2 regions](https://amplitude.com/docs/apis/analytics/http-v2)
- [New Relic browser compatibility and collector endpoints](https://docs.newrelic.com/docs/browser/new-relic-browser/getting-started/compatibility-requirements-browser-monitoring/)
- [Datadog RUM supported endpoints](https://docs.datadoghq.com/real_user_monitoring/)
- [Google Analytics regional validation endpoint](https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events)
- [Hotjar Content Security Policy requirements](https://help.hotjar.com/hc/en-us/articles/36820026388881-Content-Security-Policies)

### Required evidence for promotion

These rules must not be described as application-cleared merely because direct DNS and HTTPS tests succeed. Promotion beyond provisional alpha status requires at least one of:

1. a controlled application with the correct vendor region/account configuration that requests the exact hostname in baseline and retains its core function while blocked;
2. a reproducible, sanitized community report meeting the false-positive testing protocol; or
3. removal of the rule if material breakage is confirmed or the exact-host evidence becomes ambiguous.

A synthetic page that directly requests a collector can prove enforcement but cannot prove real application compatibility, so it is not counted as an application test.
