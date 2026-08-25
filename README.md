# NetCalcKit Blocklist

An open-source DNS blocklist project for reducing ads, trackers, and telemetry at the DNS level.

> **Status:** Phase 1 foundation. The standard list is intentionally empty until candidate sources and their licenses have been reviewed.

## Repository structure

- `blocklists/standard.txt` — generated standard DNS blocklist
- `allowlists/allowlist.txt` — reviewed domains that must not be blocked
- `sources/sources.txt` — approved upstream source URLs
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

The builder reads only sources explicitly listed in `sources/sources.txt`. No third-party sources are included yet.

## Rule format

The starter pipeline accepts one domain per line:

```text
example.com
tracker.example
```

Blank lines and comments beginning with `#`, `!`, or `[` are ignored. Hosts-file entries using `0.0.0.0` or `127.0.0.1` are normalized to domains. Allowlisted domains are removed from generated output.

## License

No license has been selected. A license will be added only after the project and upstream-source licensing requirements have been researched.
