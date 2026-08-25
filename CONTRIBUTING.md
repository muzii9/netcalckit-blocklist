# Contributing

Thank you for helping improve NetCalcKit Blocklist.

## Before submitting a change

- Limit blocklist entries to domains used for ads, tracking, or telemetry.
- Do not add an upstream list until its provenance, maintenance quality, and license have been reviewed.
- Check that a proposed block does not break essential site functionality.
- Add false-positive domains to the allowlist only with a clear explanation.
- Keep domain rules lowercase, unique, and alphabetically sorted.

## Development checks

Run both commands before opening a pull request:

```bash
python3 scripts/build.py
python3 scripts/validate.py
```

In a pull request, explain what changed, why it is needed, how it was tested, and any expected compatibility impact.

## Source and license safety

Do not copy or aggregate third-party blocklist data without confirming that its license permits the intended use and redistribution. Licensing decisions are intentionally deferred until documented research is complete.
