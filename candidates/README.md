# Candidate Queue

`candidates/candidates.csv` is a staging area for domains that still need research or review.

Candidates are **not published**. A domain reaches `rules/rules.csv` only after evidence and false-positive review are complete.

## Columns

- `domain` — exact lowercase hostname.
- `vendor` — product or service owner.
- `category` — narrow purpose label.
- `evidence_url` — direct research source, preferably first-party.
- `evidence_type` — one of:
  - `vendor-doc`
  - `vendor-code`
  - `first-party-config`
  - `repro-observation`
  - `community-report`
  - `third-party-signal`
- `dedicated_service` — `yes`, `no`, or `unknown`.
- `shared_infrastructure` — `yes`, `no`, or `unknown`.
- `essential_function` — `yes`, `no`, or `unknown`.
- `false_positive_risk` — `low`, `low-moderate`, `moderate`, `high`, or `unknown`.
- `status` — `new`, `research`, `review`, `hold`, or `rejected`.
- `observed_date` — ISO date (`YYYY-MM-DD`).
- `notes` — short factual context. Quote the CSV cell if it contains commas.

Rows must be unique and sorted by `domain`.

## Triage score

`scripts/score_candidates.py` produces a deterministic research-priority score.

The score is **not an approval decision**. It helps sort work:

- `HIGH` — strong research signals; still needs evidence record and compatibility review.
- `REVIEW` — useful candidate but missing confidence or carrying some risk.
- `HOLD` — weak evidence, shared/essential infrastructure, high false-positive risk, or an explicit maintainer hold/reject status.

A third-party blocklist hit can create a candidate, but can never by itself make a rule publishable.

## Promotion

Before promotion to `rules/rules.csv`:

1. establish primary or reproducible evidence;
2. write an evidence record under `evidence/`;
3. assess false-positive risk and essential/shared infrastructure;
4. check current DNS health;
5. perform isolated enforcement testing when practical;
6. add the reviewed row to `rules/rules.csv`;
7. remove the candidate row;
8. rebuild and validate generated lists.
