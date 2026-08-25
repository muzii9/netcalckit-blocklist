# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Initial repository structure for blocklists, allowlists, approved sources, and maintenance scripts.
- Deterministic starter build script with allowlist filtering.
- Validation checks for domain format, ordering, duplicates, and blocklist/allowlist overlap.
- Initial project and contribution documentation.
- Independent domain inclusion and evidence policy.
- Dedicated curated-domain input for original NetCalcKit rules.
- Structured issue forms for domain reports, false positives, and project improvements.

### Changed

- Adopted ODbL 1.0/DbCL 1.0 for blocklist data, MIT for scripts, and CC BY 4.0 for documentation.

- Adopted an original-curation model instead of ingesting third-party aggregate blocklists.
- Updated the build pipeline to use only independently reviewed NetCalcKit domains.

### Notes

- No third-party blocklist sources are included.
