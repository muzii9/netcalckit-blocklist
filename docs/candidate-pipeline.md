# Candidate Pipeline

NetCalcKit uses a staged research queue so discovery does not immediately affect published DNS filtering.

## Lifecycle

```text
candidate discovery
      |
      v
candidates/candidates.csv
      |
      +--> syntax + duplicate checks
      +--> deterministic triage score
      +--> DNS health report
      |
      v
human evidence / false-positive review
      |
      v
evidence/<batch>.md + rules/rules.csv
      |
      v
build + validation + isolated enforcement test
      |
      v
published blocklist
```

## What automation decides

Automation can safely decide whether data is structurally valid and whether a hostname currently resolves. It can also calculate a transparent triage score from recorded evidence/risk fields.

Automation does **not** decide that a candidate is safe to publish.

## Triage bands

The score prioritizes research:

- `HIGH` — strong first-party/reproducible evidence, dedicated service, low shared/essential risk.
- `REVIEW` — plausible candidate needing more evidence or compatibility work.
- `HOLD` — shared/essential infrastructure, high risk, non-dedicated service, or weak signals.

Hard-risk fields force `HOLD` even if other signals are strong.

## DNS health

The DNS-health job reports:

- `resolving` — current A and/or AAAA/CNAME-chain answer exists;
- `no-address` — query completed but no A/AAAA answer was returned;
- `error` — resolver/tool transport failed.

A hostname going non-resolving is a review signal, not an automatic deletion. Vendors may use regional, account-specific, or temporarily inactive endpoints.

## False-positive protection

Candidates should not be promoted when they are:

- broad vendor apex domains;
- authentication, payment, update, security, or recovery infrastructure;
- shared CDN/hosting infrastructure without narrow justification;
- supported only by a third-party blocklist;
- high-risk without reproducible compatibility evidence.

A credible false-positive report takes priority over list growth.

## Scheduled work

GitHub Actions runs published-rule and candidate DNS health weekly and stores CSV artifacts for 30 days. It does not auto-edit, auto-remove, or auto-publish rules.
