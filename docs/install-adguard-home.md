# Install in AdGuard Home

> **Alpha notice:** NetCalcKit is under active testing. Use the moving subscription only if you are comfortable reporting possible false positives.

AdGuard Home accepts domain-only blocklists, which is the format used by `blocklists/standard.txt`. The current list has been loaded, refreshed, and enforced successfully in an isolated AdGuard Home v0.107.79 instance.

## Add the subscription

1. Open the AdGuard Home admin interface.
2. Go to **Filters → DNS blocklists**.
3. Choose **Add blocklist**, then **Add a custom list**.
4. Enter the name `NetCalcKit Alpha`.
5. Paste this URL:

   ```text
   https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
   ```

6. Save the list and refresh the filters.
7. Confirm that AdGuard Home reports 13 rules for the subscription.

The `main` URL follows ongoing alpha development. The immutable `v0.1.0-alpha` snapshot contains only the original seven rules:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/v0.1.0-alpha/blocklists/standard.txt
```

## Verify it

Choose a hostname from the current list and query it through the AdGuard Home resolver. For example:

```bash
dig @YOUR_ADGUARD_IP www.google-analytics.com
dig @YOUR_ADGUARD_IP example.com
```

The listed hostname should receive the configured blocking response. The unrelated control domain `example.com` should still resolve normally. AdGuard Home's Query Log can confirm which filter matched the request.

## If something breaks

1. Temporarily disable only the **NetCalcKit Alpha** subscription.
2. Repeat the same action in the affected app or website.
3. If the feature works only while NetCalcKit is disabled, follow `false-positive-testing.md` and submit a false-positive report.
4. Keep the subscription disabled until the exact rule is reviewed if the affected feature is essential.

To roll back completely, disable or remove the custom NetCalcKit subscription from **Filters → DNS blocklists**. This does not alter AdGuard Home's other lists.

## References

- [AdGuard Home configuration](https://github.com/AdguardTeam/AdGuardHome/wiki/Configuration)
- [AdGuard Home blocklist syntax](https://github.com/AdguardTeam/AdGuardHome/wiki/Hosts-Blocklists)
- [AdGuard Home FAQ](https://github.com/AdguardTeam/AdGuardHome/wiki/FAQ)
