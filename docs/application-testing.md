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
