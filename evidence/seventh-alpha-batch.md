# Seventh alpha candidate review — Pendo

Reviewed: 2026-09-24

This batch evaluates exact Pendo Web SDK and data-service hosts from Pendo's current first-party network documentation. Nothing in this file is automatically approved for publication.

## Primary vendor evidence

Pendo's restricted-network documentation identifies:

- `data.pendo.io` as the Web SDK host used to retrieve guide metadata and send event data.
- `cdn.pendo.io` as the host that loads the Pendo Web SDK JavaScript and global CSS.

Pendo also documents regional equivalents for EU, US1, Japan, and Australia.

Sources:

- https://support.pendo.io/hc/en-us/articles/21338207825307-Host-name-list-for-Pendo-subscriptions-in-restricted-network-environments
- https://support.pendo.io/hc/en-us/articles/360032209131-Content-Security-Policy-CSP
- https://support.pendo.io/hc/en-us/articles/360032201071-Client-side-data-installation

## Data hosts staged for research

- data.pendo.io
- data.eu.pendo.io
- us1.data.pendo.io
- data.jpn.pendo.io
- data.au.pendo.io

These are dedicated Pendo service hosts, but Pendo documents a mixed purpose: event transmission plus guide-metadata retrieval. Because blocking may affect in-app guidance as well as analytics, `essential_function` is left `unknown` and false-positive risk is set to `moderate`.

They remain research candidates rather than automatic Standard additions.

## SDK hosts held

- cdn.pendo.io
- cdn.eu.pendo.io
- us1.cdn.pendo.io
- cdn.jpn.pendo.io
- cdn.au.pendo.io

Pendo documents these as Web SDK JavaScript/CSS delivery hosts. Blocking them can remove Pendo-powered guides, onboarding, or help UI from applications.

These are explicitly held even though they are vendor-documented and dedicated, because the breakage surface is larger than a collector-only endpoint.

## Exclusions

This batch does not stage:

- app/portal hosts used to access Pendo's own user-facing product.
- support, developer documentation, SSO, payment, feedback, SDK-download, or collaboration infrastructure.
- broad `*.pendo.io` wildcards.
- `stats.pendo.com` regional variants because the reviewed first-party source lists the hosts but does not provide enough purpose detail for a confident classification.

## Promotion gate

Before any Pendo data host can enter Standard it must pass:

1. candidate schema validation and deterministic triage,
2. DNS-health checks,
3. additional false-positive review focused on applications that use Pendo guides,
4. isolated AdGuard Home enforcement testing.

A high automation score is only a research-priority signal and never an approval decision.
