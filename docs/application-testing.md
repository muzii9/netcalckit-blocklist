# Application compatibility test record

This document records controlled application-level comparisons. A passing row is evidence only for the exact application behavior and list hostnames actually exercised during that run.

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
- **zero rules received application-level clearance from this run**.

This distinction is intentional. A site loading successfully while it does not exercise a listed hostname cannot prove that blocking that hostname is safe. Rule-level status remains provisional until a controlled test observes the request in the baseline run, confirms it is blocked in the comparison run, and verifies that the relevant core feature still works.

### Next coverage targets

Future runs should select public, reproducible applications that actually request the Amplitude, Google Analytics, Hotjar, Microsoft Clarity, New Relic, or Datadog hostnames in the current list. Authentication, private user data, payments, and destructive actions must not be used merely to increase coverage.
