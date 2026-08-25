# Domain Inclusion Policy

NetCalcKit is independently curated. Presence on another blocklist is a research signal, not sufficient evidence for inclusion.

## Inclusion requirements

A proposed domain must:

1. be dedicated primarily to advertising, tracking, analytics, metrics, or telemetry;
2. have independently reviewable evidence from network behavior, vendor documentation, application code, DNS observations, or another primary source;
3. include a concise explanation of what is collected or served;
4. be checked for shared hosting and essential user-facing functionality;
5. be reviewed for likely false positives;
6. be recorded as a lowercase registrable domain or justified subdomain.

## Evidence record

Each proposal or pull request should record:

- domain;
- category;
- evidence URL or reproducible observation;
- observation date;
- affected product or platform;
- false-positive assessment;
- submitter's relationship to the domain, if any.

Third-party blocklists may help discover candidates, but they must not be copied, imported, or used as sole evidence.

## Exclusions

Do not block:

- apex domains that also provide essential user-facing services;
- authentication, payments, updates, security, or recovery infrastructure;
- shared CDNs or hosting platforms without a narrowly justified subdomain;
- domains supported only by reputation, guesswork, or another blocklist;
- inactive domains without a current risk justification.

## Removal and allowlisting

A credible false-positive report takes priority over list size. Temporarily allowlist a disputed domain when necessary to prevent breakage, investigate it, and document the final decision.
