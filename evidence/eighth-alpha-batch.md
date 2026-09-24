# Eighth alpha candidate review — Fathom Analytics

Reviewed: 2026-09-24

This batch starts with the exact Fathom Analytics client-script hostname documented by Fathom. It is staged for research only and is not automatically approved for Standard.

## Primary vendor evidence

Fathom's installation documentation tells customers to load its analytics script from:

- `cdn.usefathom.com/script.js`

Fathom's advanced script documentation states that the script collects page views by default and exposes client-side functions for tracking page views and custom events.

Sources:

- https://usefathom.com/docs/script/embed
- https://usefathom.com/docs/script/script-advanced
- https://usefathom.com/docs/start/install

## Candidate

- `cdn.usefathom.com`

Assessment:

- Dedicated service: yes
- Shared infrastructure: no evidence of unrelated third-party use
- Essential site function: no; the documented purpose is analytics collection
- False-positive risk: low-moderate
- Initial status: research

The hostname serves the analytics client script rather than Fathom's customer dashboard or billing/account services. Blocking it is expected to prevent Fathom analytics from loading on a site, but the batch still requires DNS-health and isolated enforcement checks before promotion.

## Exclusions

This batch does not add:

- Fathom dashboard/account/API hosts
- broad `usefathom.com` or wildcard rules
- any inferred collector hostname that is not explicitly supported by reviewed first-party documentation

## Automated review

GitHub Actions candidate review passed on 2026-09-24:

- Candidate triage: HIGH 1, REVIEW 0, HOLD 13
- `cdn.usefathom.com`: HIGH, score 9
- DNS health: 13 resolving, 1 no-address, 0 errors

The no-address result belongs to a previously held candidate, not the Fathom hostname.

## Promotion gate

The Fathom candidate passed schema validation, deterministic scoring, and DNS-health checks. Before publication it still requires:

1. isolated AdGuard Home enforcement testing,
2. a control-domain check,
3. final false-positive review.

Automation scores are research-priority signals only and do not auto-approve the rule.

## Isolated AdGuard Home enforcement test

Tested: 2026-09-24

The immutable 88-rule release candidate was loaded into the isolated AdGuard Home test instance and verified against the DNS endpoint on port 5053.

Control result:

- `example.com` resolved normally to public IP addresses.

New-rule result:

- `cdn.usefathom.com` was blocked successfully.

Full verifier result:

- Total rules tested: 88
- Immediate PASS: 84
- Retry PASS: 4
- Confirmed blocked: 88
- Real FAIL: 0
- DNS errors: 0
- Confirmed pass rate: 100.00%
- Final result: `ALL RULES VERIFIED`

The four retry passes were temporary first-attempt UDP misses that succeeded on the verifier's retry path. They were not counted as rule failures.

This confirms DNS enforcement for the 88-rule release candidate in the isolated AdGuard Home lab. It does not prove universal application compatibility.

