# NetCalcKit Blocklist

An independently curated, open-source DNS blocklist for reducing ads, trackers, and telemetry at the DNS level.

> **Status:** Early development. NetCalcKit does not rebrand or republish third-party aggregate blocklists. Every published rule must pass the project's own evidence and false-positive review.

## Repository structure

- `blocklists/standard.txt` — generated standard DNS blocklist
- `allowlists/allowlist.txt` — reviewed domains that must not be blocked
- `sources/curated.txt` — independently reviewed NetCalcKit domain entries
- `sources/sources.txt` — external-source policy; aggregate feeds are disabled
- `docs/domain-policy.md` — evidence and review requirements
- `scripts/build.py` — deterministic blocklist builder
- `scripts/validate.py` — format, ordering, and duplicate checks
- `CONTRIBUTING.md` — contribution guidelines
- `CHANGELOG.md` — project history

## Quick start

Python 3.10 or newer is required. The scripts use only the Python standard library.

```bash
python3 scripts/build.py
python3 scripts/validate.py
```

## Curation model

A domain is not added merely because another blocklist contains it. A proposed rule needs independently reviewable evidence showing that the domain is dedicated to advertising, tracking, or telemetry, plus a false-positive assessment.

Approved domains are recorded in `sources/curated.txt`. The builder normalizes them, removes allowlisted entries, sorts the result, and writes `blocklists/standard.txt`.

## Licensing

This is a multi-license repository:

- Curated-domain database, blocklists, and allowlist: **ODbL 1.0**, with individual contents under **DbCL 1.0**
- Python scripts: **MIT**
- Documentation: **CC BY 4.0**

See `LICENSE.md` for the exact scope, attribution notice, local legal texts, and trademark reservation.
