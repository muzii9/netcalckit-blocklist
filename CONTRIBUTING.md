# Contributing

Thank you for helping improve NetCalcKit Blocklist.

## Domain proposals

- Do not copy or bulk-import any third-party blocklist.
- Another list containing a domain is not sufficient evidence.
- Follow `docs/domain-policy.md` and provide independently reviewable evidence.
- Explain the category, observed behavior, affected product, observation date, and false-positive risk.
- Do not block shared or essential infrastructure without a narrowly justified subdomain.
- Add false-positive domains to the allowlist with a clear explanation.
- Keep rules lowercase, unique, and alphabetically sorted.

## Issue forms

Choose the matching GitHub issue form:

- **Report a tracking domain** for a new evidence-backed candidate.
- **Report a false positive** when a published rule breaks legitimate functionality.
- **Suggest an improvement** for tooling, validation, documentation, or process changes.

Submit one domain per report so each decision remains independently reviewable.

## Development checks

Run both commands before opening a pull request:

```bash
python3 scripts/build.py
python3 scripts/validate.py
```

In a pull request, explain what changed, why it is needed, how it was tested, and any expected compatibility impact.

## Original-work policy

NetCalcKit does not ingest or rebrand third-party aggregate lists. Submissions copied from external lists will be rejected. External lists may only identify candidates that are then investigated independently.
