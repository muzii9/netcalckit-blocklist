# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Two Twilio Segment event-ingestion hosts, with vendor documentation and false-positive notes.

## v0.2.0-alpha — 2026-08-25

### Added

- Automatic GitHub Actions validation on pushes, pull requests, and manual runs.
- Immutable subscription URL for the v0.1.0-alpha snapshot.
- DNS and HTTPS smoke tests from a separate Ubuntu host.
- Isolated AdGuard Home v0.107.79 enforcement test using only the NetCalcKit subscription.
- Second batch with six exact New Relic and Datadog browser telemetry hosts.
- Vendor documentation and two-environment network checks for the second batch.
- AdGuard Home subscription refresh and enforcement checks for all 13 release rules.
- AdGuard Home installation, verification, troubleshooting, and rollback guide.
- Application-level false-positive testing protocol and severity model.
- Platform support matrix separating verified support from pending research.
- First controlled browser comparison of NetCalcKit core page, calculator, and tool-search behavior.
- Vendor-owned public-page comparison covering six rules; four received basic core-render checks and two received render-only evidence.
- Testability review for seven account-, region-, or resource-specific rules that remain unexercised.
- v0.2.0-alpha release-candidate checklist and draft release notes.
- Shared domain parser with checks for malformed, duplicate, unsorted, hosts-format, inline-comment, and IP-address entries.
- Unit tests for accepted input and seven parser failure modes.
- Local DbCL 1.0 legal text and stable-release criteria.
- Isolated Pi-hole Core v6.4.3 Gravity and DNS enforcement test for all 13 rules.
- Pi-hole installation, verification, and rollback guide.

### Changed

- Clarified that DNS enforcement tests do not prove universal application compatibility.
- Held back unverified Pi-hole, NextDNS, and Control D instructions until documentation review and direct testing are complete.
- Kept rule classifications narrow when available evidence did not support broader claims.
- Required real-account or reproducible community evidence before promoting specialized regional collectors.
- Updated the builder and validator to use the same parser and check the generated header and final newline.

## v0.1.0-alpha — 2026-08-25

### Added

- Initial repository structure for blocklists, allowlists, approved sources, and maintenance scripts.
- Deterministic build script with allowlist filtering.
- Validation checks for domain format, ordering, duplicates, overlap, and reproducibility.
- Project, contribution, licensing, and domain evidence policies.
- Structured issue forms for domain reports, false positives, and project improvements.
- First batch containing seven exact analytics and telemetry hostnames.
- Evidence notes covering documentation, purpose, scope, and false-positive risk for each first-batch rule.
- Alpha release smoke-test record and direct subscription URL.

### Changed

- Adopted ODbL 1.0/DbCL 1.0 for blocklist data, MIT for scripts, and CC BY 4.0 for documentation.
- Chose original curation instead of ingesting third-party aggregate blocklists.
- Updated the build pipeline to use reviewed NetCalcKit domains only.

### Notes

- No third-party blocklist sources are included.
- The first batch excludes vendor apex domains, wildcards, and user-facing dashboard hosts.
- This is an alpha release; compatibility testing and false-positive review are ongoing.
