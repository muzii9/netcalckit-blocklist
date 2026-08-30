# NetCalcKit Blocklist

A small open-source DNS blocklist for ads, trackers, and telemetry.

> **Status:** v0.2.0-alpha is published as a prerelease. The current `main` list contains 65 analytics, telemetry, and observability hostnames. The published v0.2.0-alpha release contains 13 rules.

## Subscribe

For ongoing alpha updates, use:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
```

For the immutable 13-rule `v0.2.0-alpha` snapshot, use:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/v0.2.0-alpha/blocklists/standard.txt
```

The `main` list includes work added after the release. If something breaks, use the false-positive issue form.

## Compatibility

The 13-rule v0.2.0-alpha list was loaded as the only active custom filter in an isolated AdGuard Home v0.107.79 instance. All 13 domains were blocked, the subscription refreshed successfully, and an unrelated control domain resolved normally. That confirms DNS enforcement, not universal app compatibility.

Controlled browser comparisons have exercised six of those 13 rules on vendor-owned public pages. Four received a basic core-render smoke test, two have render-only evidence, and seven remain unexercised.

The same 13-rule release was also parsed and enforced successfully in isolated AdGuard Home and Pi-hole environments, with an unrelated control domain resolving normally in both.

- [Install in AdGuard Home](docs/install-adguard-home.md)
- [Install in Pi-hole](docs/install-pihole.md)
- [False-positive testing protocol](docs/false-positive-testing.md)
- [Application compatibility test record](docs/application-testing.md)
- [Platform support status](docs/platform-support.md)
- [AdGuard Home test record](docs/adguard-home-testing.md)
- [Pi-hole test record](docs/pihole-testing.md)

NextDNS and Control D guides are being held back until those platforms are checked against current documentation and tested directly.

## Repository structure

- `blocklists/standard.txt` — generated standard DNS blocklist
- `allowlists/allowlist.txt` — domains that must not be blocked
- `sources/curated.txt` — reviewed NetCalcKit domain entries
- `sources/sources.txt` — external-source policy; aggregate feeds are disabled
- `evidence/initial-alpha.md` — evidence and risk notes for the first alpha batch
- `evidence/second-alpha-batch.md` — evidence and risk notes for the second batch
- `evidence/third-alpha-batch.md` — evidence and risk notes for the third batch
- `docs/domain-policy.md` — evidence and review requirements
- `docs/alpha-testing.md` — alpha release smoke-test record
- `docs/adguard-home-testing.md` — isolated AdGuard Home enforcement test
- `docs/install-adguard-home.md` — AdGuard Home installation and rollback guide
- `docs/install-pihole.md` — Pi-hole installation and rollback guide
- `docs/false-positive-testing.md` — application-level false-positive protocol
- `docs/application-testing.md` — controlled app-test results and rule coverage
- `docs/platform-support.md` — verified and pending platform status
- `docs/pihole-testing.md` — isolated Pi-hole Gravity and enforcement test
- `docs/stable-release-criteria.md` — gates for a non-prerelease version
- `scripts/domain_utils.py` — shared domain-file parser
- `scripts/build.py` — deterministic blocklist builder
- `scripts/validate.py` — format, ordering, duplicate, overlap, and reproducibility checks
- `tests/test_domain_utils.py` — parser and malformed-input unit tests
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

A domain is not added just because another blocklist contains it. Each rule needs reviewable evidence that it is used for advertising, tracking, or telemetry, plus a false-positive check.

Approved domains are recorded in `sources/curated.txt`. The builder normalizes them, removes allowlisted entries, sorts the result, and writes `blocklists/standard.txt`.

The list sticks to exact service hostnames where possible. Broad vendor apex domains and user-facing dashboard hosts are excluded.

## Reporting and contributions

Use the issue forms to report a tracking domain, a false positive, or a project improvement. Domain proposals should include evidence and a short false-positive assessment.

See `CONTRIBUTING.md` and `docs/domain-policy.md` before submitting a domain.

## Licensing

This is a multi-license repository:

- Curated-domain database, blocklists, and allowlist: **ODbL 1.0**, with individual contents under **DbCL 1.0**
- Python scripts: **MIT**
- Documentation: **CC BY 4.0**

See `LICENSE.md` for the exact scope, attribution notice, local legal texts, and trademark reservation.
