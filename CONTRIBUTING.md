# Contributing

Thanks for helping improve NetCalcKit Blocklist.

## Domain proposals

- Don't copy or bulk-import another blocklist.
- A domain appearing on another list is not enough on its own.
- Follow `docs/domain-policy.md` and include a source that can be checked.
- Note what the domain does, which product uses it, when it was observed, and the likely false-positive risk.
- Avoid shared or essential infrastructure unless the exact subdomain is clearly justified.
- Put confirmed false positives in the allowlist with a short reason.
- Keep rules lowercase, unique, and alphabetically sorted.

## Issue forms

Use the matching GitHub issue form:

- **Report a tracking domain** for a new candidate.
- **Report a false positive** when a published rule breaks legitimate functionality.
- **Suggest an improvement** for tooling, validation, docs, or process changes.

Please keep domain reports to one domain each so they are easier to review.

## Development checks

Run both commands before opening a pull request:

```bash
python3 scripts/build.py
python3 scripts/validate.py
```

In a pull request, say what changed, why, how you tested it, and whether it could affect compatibility.

## Original-work policy

NetCalcKit does not ingest or rebrand third-party aggregate lists. External lists can point to candidates, but each candidate still needs its own review before it is added here.
