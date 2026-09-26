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
