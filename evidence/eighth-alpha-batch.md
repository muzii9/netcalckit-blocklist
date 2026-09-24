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

## Promotion gate

Before publication the candidate must pass:

1. candidate validation and deterministic scoring,
2. current DNS-health checks,
3. isolated AdGuard Home enforcement testing,
4. a control-domain check,
5. final false-positive review.

Automation scores are research-priority signals only and do not auto-approve the rule.
