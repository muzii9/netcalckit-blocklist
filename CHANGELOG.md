# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Automatic GitHub Actions validation on pushes, pull requests, and manual runs.
- Immutable subscription URL for the v0.1.0-alpha snapshot.
- Independent DNS and HTTPS smoke-test verification from a separate Ubuntu host.
- Isolated AdGuard Home v0.107.79 enforcement test using only the NetCalcKit subscription.
- Second independently researched batch with six exact New Relic and Datadog browser telemetry hosts.
- Official-vendor evidence and two-environment network verification for every second-batch rule.
- Successful AdGuard Home subscription refresh and enforcement verification for all 13 current rules.
- Verified AdGuard Home installation, verification, troubleshooting, and rollback guide.
- Application-level false-positive testing protocol and severity model.
- Platform support matrix separating verified support from pending research.
- First controlled browser comparison of NetCalcKit core page, calculator, and tool-search behavior.
- Vendor-owned public-page comparison exercising six current rules; four received preliminary core-render passes and two received render-only evidence.\n- Official testability review for seven account-, region-, or resource-specific rules that remain unexercised.\n- v0.2.0-alpha release-candidate checklist and draft release notes.

### Changed

- Clarified that DNS enforcement testing does not constitute universal application compatibility.
- Withheld unverified Pi-hole, NextDNS, and Control D instructions until authoritative review and direct testing are complete.
- Kept rule-level classifications narrow when a page or test metric did not provide sufficient evidence.\n- Defined real-account or reproducible community evidence as the promotion requirement for specialized regional collectors.

## v0.1.0-alpha — 2026-08-25

### Added

- Initial repository structure for blocklists, allowlists, approved sources, and maintenance scripts.
- Deterministic build script with allowlist filtering.
- Validation checks for domain format, ordering, duplicates, overlap, and reproducibility.
- Project, contribution, licensing, and independent-domain evidence policies.
- Structured issue forms for domain reports, false positives, and project improvements.
- First independently researched batch containing seven exact analytics and telemetry hostnames.
- Evidence ledger recording official documentation, purpose, scope, and false-positive risk for each first-batch rule.
- Alpha release smoke-test record and direct subscription URL.

### Changed

- Adopted ODbL 1.0/DbCL 1.0 for blocklist data, MIT for scripts, and CC BY 4.0 for documentation.
- Adopted an original-curation model instead of ingesting third-party aggregate blocklists.
- Updated the build pipeline to use only independently reviewed NetCalcKit domains.

### Notes

- No third-party blocklist sources are included.
- The first batch deliberately excludes vendor apex domains, wildcards, and user-facing dashboard hosts.
- This is an alpha release; compatibility testing and false-positive review remain ongoing.
