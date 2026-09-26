# Automated public-site compatibility tests

This workflow is an **early smoke test**, not evidence of universal site/app compatibility. It never changes `rules/rules.csv`, the published blocklist, a user's router, or the user's DNS provider.

## When it runs

- On pull requests that change `rules/rules.csv`, `blocklists/standard.txt`, the browser runner, the case registry, or the workflow.
- Every Tuesday at 03:37 UTC as a regression check for existing examples.
- Manually via GitHub Actions → Live public-site A/B smoke → Run workflow.

Workflow: `.github/workflows/real-site-smoke.yml`; runner: `scripts/real_site_smoke.py`.

## Adding a new approved hostname

Before proposing a domain for Standard, find at least one **public, login-free real site** that naturally requests that exact hostname in the browser's baseline mode. Do not count synthetic test code that artificially requests the tracking hostname. Add its vendor, exact hostname, short wait window and public page URL(s) to `tests/live-site-cases.json`; do not use cookies, account pages, credentials or URLs containing query tokens.

When a PR introduces an approved hostname to `rules/rules.csv`, CI compares that PR's approved rules with the base commit. Any newly approved host missing from the test registry is reported and the workflow exits unsuccessfully. A mapping alone is not enough: the baseline must **actually request** the exact host, and the blocked mode must intercept it while the public page keeps its basic title, body, header and link presence. A new rule without a safe natural public example should remain HOLD pending human review and a documented alternative compatibility method; do not fabricate a passing fixture.

Existing rules without a public-page fixture are **not retroactively cleared** by this workflow. The original 88 pre-expansion rules have their own incomplete coverage noted in `docs/application-testing.md`. The first registered hosts are `ping.chartbeat.net` and `queue.simpleanalyticscdn.com` only.

## What the comparison can and cannot establish

The test opens each public URL in a fresh normal browser context and, only after seeing actual baseline requests to the host, repeats it with requests to **that exact host alone** intercepted and failed with a DNS-like error. It measures basic page rendering and link presence, not whether analytics collection is successful or whether a site is fully usable. It cannot validate sign-in, private app functionality, payment, personalized sessions, account settings, media, or real DNS-provider subscription refreshes.

Each run emits a sanitized `live-site-browser-smoke` artifact with JSON and Markdown reports and a GitHub job summary. No cookies, request query strings, account identifiers or private URLs should enter test fixtures or reports.

A result is either `preliminary-pass` (host naturally exercised, basic render retained), `fail` (observed basic breakage), or `inconclusive` (the host was not naturally exercised or the page could not be evaluated). **Inconclusive is not a pass**, including when a site blocks browser automation, moves its tracker or temporarily fails to load. The workflow returns a nonzero status if any case fails or remains inconclusive.

A weekly failure or drift alert requires human investigation; do not automatically remove, add, promote or publish a rule based only on a browser smoke result. Use the false-positive testing protocol for suspected app breakage.
