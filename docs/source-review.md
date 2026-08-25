# Source and License Review

Review date: 2026-08-25

## Decision

NetCalcKit selected the **original curation** model.

The project will not ingest, transform, rebrand, or republish third-party aggregate blocklists. HaGeZi, OISD, AdGuard DNS Filter, StevenBlack Hosts, and similar projects are not approved upstream feeds.

They may be consulted only as discovery signals during research. A domain still requires independent primary evidence and NetCalcKit's own false-positive review before inclusion.

## Reason

- Build a genuinely distinct NetCalcKit dataset.
- Maintain clear provenance for every published rule.
- Avoid presenting another maintainer's work as NetCalcKit's work.
- Avoid inherited aggregate-source licensing ambiguity.
- Keep quality decisions and market positioning under NetCalcKit control.

## Operational rule

- `sources/curated.txt` contains only independently reviewed NetCalcKit entries.
- `sources/sources.txt` remains free of aggregate-feed URLs.
- `docs/domain-policy.md` defines the required evidence.
- No project license will be added until the original dataset and code licensing choice is finalized.

This decision supersedes the preliminary shortlist previously recorded in this document.
