# False-positive testing

A false positive occurs when a NetCalcKit rule blocks a hostname required for an essential or expected feature, rather than only suppressing advertising, tracking, or telemetry.

DNS enforcement alone does not prove application compatibility. Each rule remains provisional until representative application-level testing and community feedback provide enough confidence.

## Reproduce before reporting

1. Update or refresh the NetCalcKit subscription.
2. Confirm the affected hostname appears in the current `blocklists/standard.txt`.
3. Record the affected app or website, action, approximate time, and hostname shown in the DNS query log.
4. Repeat the action with NetCalcKit enabled.
5. Temporarily disable only NetCalcKit and repeat the same action under otherwise identical conditions.
6. Re-enable NetCalcKit and reproduce once more when safe.
7. Report the result only when the behavior consistently changes with NetCalcKit's state.

Do not include passwords, account identifiers, private URLs, authentication tokens, full browsing history, or other sensitive query-log data.

## Minimum application test matrix

For every candidate rule, test the relevant parts of the vendor or an affected product:

- app or page startup;
- sign-in, sign-out, and session continuity;
- navigation and core content loading;
- forms and data submission;
- search and API-backed content;
- media playback or downloads, when applicable;
- checkout or payments, when applicable;
- settings, updates, and error recovery.

Mark an item **not applicable** instead of claiming it passed when it was not exercised.

## Severity

- **Critical:** authentication, payments, safety features, or the product's primary function fails.
- **High:** a major feature fails with no practical workaround.
- **Moderate:** a secondary feature degrades or requires a workaround.
- **Low:** cosmetic or non-essential behavior changes.

A reproducible critical or high-severity false positive should be removed from the curated source promptly while it is investigated. Moderate and low reports still require evidence and review; popularity is not a reason to ignore breakage.

## Report

Use the repository's [false-positive issue form](https://github.com/muzii9/netcalckit-blocklist/issues/new?template=false-positive.yml). Include:

- exact blocked hostname;
- affected app/site and platform;
- steps to reproduce;
- behavior with NetCalcKit enabled and disabled;
- severity and the essential feature affected;
- sanitized query-log evidence, if available.

The report will be checked against the evidence ledger and domain policy. Confirmed removals are recorded in the changelog and may be protected through `allowlists/allowlist.txt`.
