# v0.2.0-alpha release candidate

Target date: 2026-08-25

This candidate freezes the current 13-rule independently curated alpha list. It does not claim universal application compatibility.

## Included changes

- Six additional exact New Relic and Datadog browser-telemetry hostnames after official-vendor research.
- Isolated AdGuard Home v0.107.79 subscription, refresh, enforcement, and control-domain tests.
- AdGuard Home installation and rollback guide.
- False-positive protocol and severity model.
- Controlled browser comparisons on NetCalcKit and vendor-owned public pages.
- Application evidence for six rules: four preliminary core-render passes and two render-only observations.
- Explicit testability requirements for seven specialized regional or account-specific rules.

## Release gate

- [x] No third-party aggregate blocklist imported.
- [x] Every rule has official-vendor evidence and an exact-host scope assessment.
- [x] Broad vendor apex domains, wildcards, dashboards, and account-management hosts remain excluded.
- [x] All 13 rules enforced by the isolated AdGuard Home subscription.
- [x] An unrelated control domain resolved normally.
- [x] Build output is deterministic.
- [x] Repository validation passes on supported Python versions.
- [x] Licensing scope is documented locally.
- [x] False-positive reporting and rollback instructions are available.
- [x] Application-test limitations are disclosed.
- [ ] Create immutable `v0.2.0-alpha` tag from the final verified release commit.
- [ ] Publish the GitHub prerelease and verify its raw subscription URL.

## Planned immutable subscription

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/v0.2.0-alpha/blocklists/standard.txt
```

Do not use this URL until the tag has been published.

## Draft release notes

NetCalcKit Blocklist v0.2.0-alpha expands the independently curated alpha list from seven to 13 exact analytics and telemetry hostnames.

Highlights:

- New Relic and Datadog browser-telemetry coverage
- successful isolated AdGuard Home enforcement of all 13 rules
- deterministic build and automated validation
- verified AdGuard Home installation guide
- structured false-positive protocol
- transparent application-coverage record

This remains an alpha prerelease. Six rules have limited public-page application evidence; seven specialized regional or account-specific rules remain provisional. No third-party aggregate list is imported or rebranded.
