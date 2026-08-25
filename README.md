# NetCalcKit Blocklist

An independently curated, open-source DNS blocklist for reducing ads, trackers, and telemetry at the DNS level.

> **Status:** Alpha development after v0.1.0-alpha. The standard list currently contains 13 independently reviewed analytics and telemetry hostnames. NetCalcKit does not rebrand or republish third-party aggregate blocklists.

## Subscribe

For ongoing alpha updates, use:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
```

For the immutable seven-rule `v0.1.0-alpha` snapshot, use:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/v0.1.0-alpha/blocklists/standard.txt
```

The moving `main` list includes post-release alpha work. Review the testing documents and report any broken essential functionality through the false-positive issue form.

## Compatibility

The current 13-rule list was loaded as the only active custom filter in an isolated AdGuard Home v0.107.79 instance. All 13 listed domains were blocked, the subscription refreshed successfully, and an unrelated control domain resolved normally. See `docs/adguard-home-testing.md` for the exact environment and results.

## Repository structure

- `blocklists/standard.txt` — generated standard DNS blocklist
- `allowlists/allowlist.txt` — reviewed domains that must not be blocked
- `sources/curated.txt` — independently reviewed NetCalcKit domain entries
- `sources/sources.txt` — external-source policy; aggregate feeds are disabled
- `evidence/initial-alpha.md` — evidence and risk record for the first alpha batch
- `evidence/second-alpha-batch.md` — evidence and risk record for the second batch
- `docs/domain-policy.md` — evidence and review requirements
- `docs/alpha-testing.md` — alpha release smoke-test record
- `docs/adguard-home-testing.md` — isolated AdGuard Home enforcement test
- `scripts/build.py` — deterministic blocklist builder
- `scripts/validate.py` — format, ordering, duplicate, overlap, and reproducibility checks
- `.github/workflows/validate.yml` — automatic validation for pushes and pull requests
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

Only exact service hostnames documented by their vendors are considered. Broad vendor apex domains and user-facing dashboard hosts are intentionally excluded.

## Reporting and contributions

Use the repository's structured issue forms to report a tracking domain, report a false positive, or suggest an improvement. Domain proposals require independent evidence and a false-positive assessment.

See `CONTRIBUTING.md` and `docs/domain-policy.md` before submitting a domain.

## Licensing

This is a multi-license repository:

- Curated-domain database, blocklists, and allowlist: **ODbL 1.0**, with individual contents under **DbCL 1.0**
- Python scripts: **MIT**
- Documentation: **CC BY 4.0**

See `LICENSE.md` for the exact scope, attribution notice, local legal texts, and trademark reservation.
