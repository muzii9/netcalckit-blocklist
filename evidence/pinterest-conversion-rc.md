# Pinterest exact-host Standard release candidate — 2026-09-26

**Status: unmerged release candidate, awaiting independent CI and explicit maintainer approval.** No wildcard, vendor apex, SDK CDN, login, payment or dashboard host is included. Proposed rule: `ct.pinterest.com` only.

## First-party purpose evidence

- Primary source: https://developers.pinterest.com/docs/track-conversions/pinterest-tag/
- Pinterest documents `https://ct.pinterest.com/v3/` image-pixel events for conversion measurement, page visits, signups and other advertising actions.
- Its script is separately documented at `s.pinimg.com/ct/core.js`. Blocking `ct.pinterest.com` does **not** block that SDK hostname and is **not** expected to block Pinterest's core website.
- This is a narrowly named hostname rather than a broad `pinterest.com` rule. However DNS resolved through `www.pinterest.com` and Akamai aliases during GitHub CI. That DNS infrastructure overlap does not itself mean a rule also blocks `www.pinterest.com`, but requires conservative compatibility review.

## Live DNS and naturally exercised public-website evidence

- GitHub candidate/DNS review: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36262294829
- Follow-up live baseline and exact-host-only blocked comparison: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36262556724
- `https://oddmuse.co.uk/`: public HTTP 200, body length 6,266; 3 natural `ct.pinterest.com` baseline requests. During the follow-up test, exact-host blocking intercepted **32 requests**, and basic readable body length stayed 6,266.
- `https://bydeeaus.com/`: public HTTP 200, body length 5,796; 3 natural baseline requests. Exact-host blocking intercepted **32 requests**, and readable body length stayed 5,796.
- The probe uses an isolated headless Chrome browser in a public GitHub runner. It does not log in, submit forms, purchase anything, or send synthetic tracking events.

**Important risk finding:** The blocked-mode request count increased sharply (32 intercepted versus 3 baseline) on both websites, apparently because of repeat requests after blocked delivery. The automated test did **not** measure page-load latency, battery/network overhead, checkout performance or all possible SDK behavior. Do not claim universal compatibility based solely on retained body text. For this reason the rule's provisional false-positive classification is **moderate**, not low. A material performance regression or functional failure in representative real usage is grounds for re-review and removal or an allowlist exception.

## Publish criteria

The separate draft RC adds an exact entry to `rules/rules.csv` and regenerates published text *only on its branch*. To merge it, first require:
1. Python rules/reproducibility and candidate queue CI green on this RC commit.
2. Isolated AdGuard Home DNS enforcement CI green on this RC commit.
3. Real-site browser workflow triggered by the new Standard rule, with a registry case for the two observed public sites. Both should naturally request the endpoint and retain basic core rendering under blocking; classify absent host requests as inconclusive, not a pass.
4. Explicit human review of retry/network overhead and the remaining potential merchant-site false-positive risk. The release is not universally tested, and the evidence is limited to those tested sites.
5. Separate explicit maintainer authorization to merge. Until then the live `main/blocklists/standard.txt` has 90 rules and the immutable `v0.2.0-alpha` snapshot remains 13.

`bat.bing.com` is **excluded** from this RC; its shared UET script and events mean higher risk and it remains HOLD in separate research.

## Repeated public-browser performance follow-up (2026-09-26)

A more stringent A/B test repeated two normal and two exact-host-blocked, clean-browser visits per public merchant site, in alternating normal/blocked/blocked/normal order. Each visit observed browser network activity for 12 seconds after the page loaded. Source, test thresholds and retained reports: `scripts/pinterest_retry_audit.py`, `tests/test_pinterest_retry_audit.py`, and https://github.com/muzii9/netcalckit-blocklist/actions/runs/36263434244 (artifact `pinterest-retry-audit`). All six audit-logic unit tests passed.

| Public site | Natural exact-host requests (both baseline repeats) | Exact-host failed requests (both blocked repeats) | Basic public page and DOM timing |
| --- | ---: | ---: | --- |
| `oddmuse.co.uk` | 3, 3 | 32, 32 | HTTP 200 and readable body 6,266 characters in all four runs. Baseline DOM-loaded times: 2,438 and 1,474 ms; blocked: 1,639 and 1,633 ms. |
| `bydeeaus.com` | 3, 3 | 32, 32 | HTTP 200 and readable body 5,789 characters in all four runs. Baseline DOM-loaded times: 1,445 and 1,344 ms; blocked: 1,320 and 1,327 ms. |

All 32 intercepted attempts occurred in the initial observation period (none after the first six seconds in these runs). We **did not observe degraded basic content or slower DOM-loaded times** on these two public pages, but there was a reproducible **about 10.7× early request-attempt amplification**, from 3 to 32. Its cause has not been established independently: it may be retries or another failure-response reaction. The run is intentionally classified **review-required**, with a red performance workflow; do not treat the previous green basic-render workflow as full clearance.

**Publication status:** Keep this RC **draft and unmerged** while the early failed-request amplification is investigated or explicitly reviewed under the project's false-positive policy. This evidence does not demonstrate actual end-user harm, bandwidth consumption from *failed* requests, browser CPU/battery impact, checkout impact, or behavior with a real DNS provider. Independent actual-DNS or resource-usage checks would be needed for stronger assurances. Do not quietly override the red review signal to increase rule count.
