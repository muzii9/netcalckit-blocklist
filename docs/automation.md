# Automation Architecture

NetCalcKit separates rule research from repetitive validation.

## Source of truth

`rules/rules.csv` contains reviewed metadata. Generated files are rebuilt from that database:

```text
rules/rules.csv
      |
      +--> sources/curated.txt
      |
      +--> blocklists/standard.txt
```

`allowlists/allowlist.txt` is applied at build time so an approved rule can be temporarily overridden without deleting its research record.

## Candidate intake

New discoveries are staged in `candidates/candidates.csv`. CI validates the queue, calculates a transparent triage score, and records DNS health. Candidates never flow into the published list automatically; promotion still requires evidence and false-positive review.

See `docs/candidate-pipeline.md` for the lifecycle and scoring rules.

## GitHub Actions quality gate

Every push and pull request:

1. runs unit tests;
2. rebuilds generated files from the rule database;
3. validates metadata, evidence references, domains, sorting, duplicates, allowlist behavior, and reproducibility;
4. validates the staged candidate queue against existing rules and the allowlist;
5. fails if generated files differ from what is committed.

This prevents hand-edited or stale published lists from being merged.

## Home-server test lab

The isolated AdGuard Home instance is used for live DNS enforcement checks. `scripts/test_adguard_home.sh`:

- verifies a normal control domain first;
- tests every published rule;
- retries temporary UDP failures;
- falls back to TCP;
- separates transport errors from actual rule failures;
- writes a timestamped report.

This proves DNS enforcement. It does not prove universal application compatibility.

## Human review still required

Automation cannot reliably decide whether blocking a domain breaks a real product. Human review remains required for:

- new vendors or categories;
- moderate/high false-positive risk;
- authentication, payments, updates, shared infrastructure, or broad hostnames;
- credible false-positive reports;
- release promotion.

The goal is to automate repetitive checks while keeping risky inclusion decisions reviewable.
