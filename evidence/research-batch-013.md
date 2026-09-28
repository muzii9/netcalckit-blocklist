# Batch 013 — first-party conversion endpoint discovery (2026-09-26)

Research only. Microsoft UET remains **HOLD** in this PR; Pinterest is separately proposed in unmerged draft Standard release candidate [PR #21](https://github.com/muzii9/netcalckit-blocklist/pull/21). Neither is published by this research PR. They are absent from the 90-rule Standard list and existing 13-row main candidate queue at discovery time. No apex domain, wildcard, script CDN, payment, login, dashboard, or unrelated service is proposed.

## ct.pinterest.com — Pinterest conversion event endpoint

**First-party evidence:** https://developers.pinterest.com/docs/track-conversions/pinterest-tag/

Pinterest's developer guide documents the Pinterest Tag with its event-specific `https://ct.pinterest.com/v3/` image pixel endpoint for page visits, signups, leads, search, conversions, and other advertising measurement actions. Its browser-side script is separately hosted at `s.pinimg.com/ct/core.js`. These are distinct exact hosts. The former is a reasonable advertising/conversion-collection candidate; do **not** infer that blocking the pixel endpoint alone disables all Pinterest tracking methods, including customer-managed server-side conversion reporting or first-party relays.

**Risk:** low-moderate **provisional**, not proof of safe blocking. A site might hard-depend on tracking acknowledgments; blocking also deliberately prevents advertiser conversion measurement. Dedicated_service=yes (according to current documented role), shared_infrastructure=unknown (needs investigation), essential_function=unknown (needs browser confirmation). Hold for independent DNS and real public-site A/B evidence.

## bat.bing.com — Microsoft Advertising UET host

**First-party evidence:** https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_uet_img_tag

Microsoft's UET documentation confirms `https://bat.bing.com/action/0` receives Microsoft Advertising page-load and conversion events. **Critical DNS granularity limitation:** vendor examples also load its JavaScript UET library from `bat.bing.com/bat.js`, so blocking this hostname cuts both event collection **and** the analytics tag loader, not just an individual path. This host may also serve other Microsoft advertising/measurement scripts. No path-specific exception is possible with a DNS blocklist.

**Risk:** moderate to high until verified. HOLD rather than auto-promote. Test basic site rendering and any declared site behavior that depends on the UET SDK; do not promote solely because the event path is dedicated. The entire exact host must be evaluated, not merely `/action/0`.

## Automated verification — GitHub candidate review (2026-09-26)

Workflow: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36262294829
Validation: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36262294833

The candidate queue and repository validation passed. GitHub-hosted `dig` returned active A/AAAA resolution for both exact hostnames:
- `bat.bing.com` resolved through Microsoft edge host aliases and returned addresses. This only confirms live DNS, not that blocking the entire host is safe.
- `ct.pinterest.com` resolved through a CNAME chain containing `www.pinterest.com` and Akamai edge names. This **does not mean a DNS rule for `ct.pinterest.com` also blocks `www.pinterest.com`**, but means that the event-only role documented for the `ct` virtual host must be confirmed independently; it does not prove that the underlying infrastructure is isolated.

The CI-generated priority table classified both candidates as **HOLD**: `ct.pinterest.com` has a stronger dedicated-collection claim but unresolved essential-function/shared-infrastructure questions; `bat.bing.com` is high risk for a Standard promotion because SDK scripts and event ingestion share a DNS hostname. Neither may be published from this evidence alone.

## Public real-site reconnaissance and split review (2026-09-26)

Follow-up baseline and exact-host-blocked report: https://github.com/muzii9/netcalckit-blocklist/actions/runs/36262556724 .

- `ct.pinterest.com` was naturally requested 3 times each by two public Pinterest advertiser websites, `oddmuse.co.uk` and `bydeeaus.com`. The basic page body stayed unchanged in the blocked comparison. But **32 requests were intercepted during blocked mode** on each site, versus 3 baseline requests. Repeated retries/network overhead and broader application impact are not cleared; full risk analysis is documented in `evidence/pinterest-conversion-rc.md` on **draft** PR #21. This exact host is **not** staged in this research branch's candidate queue, to prevent duplicate rule/candidate conflicts if the separately reviewed RC later merges.
- `bat.bing.com` was naturally requested 3 times on `newegg.com`; the separate repeat baseline saw 3 requests, and the blocked mode intercepted 1 request while basic readable page content remained similar. This narrow public-page smoke check does **not** establish that disabling the UET SDK is safe across ecommerce sites. `bat.bing.com` remains the **sole newly staged HOLD** in this research PR due to high false-positive uncertainty.

No publication, no automatic merge and no claim of universal app compatibility follow from these results.

## Non-promotion and testing gates

1. Confirm both exact hosts resolve from independent DNS vantage points and have no allowlist conflicts. Resolving proves availability, not block safety.
2. Inspect current vendor docs and network behavior for hidden shared/essential functionality or false-positive concerns.
3. Seek **public login-free pages that naturally request the exact host** for baseline-vs-exact-host-blocked real-site tests. An unexercised or automation-blocked page is inconclusive. Do not create fake traffic to manufacture a passing test.
4. If a candidate qualifies, propose it in a **separate draft Standard release-candidate PR** with an actual tested case in `tests/live-site-cases.json`; wait for Python CI, candidate/DNS checks, AdGuard Home lab, real-site smoke and explicit maintainer merge approval.
5. Existing tagged `v0.2.0-alpha` is immutable, and none of this research touches the already-published 90-host list.

Discovery volume is not an excuse to lower the false-positive threshold.
