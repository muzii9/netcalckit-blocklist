# Install in Pi-hole

> **Pre-stable notice:** NetCalcKit remains under compatibility review. Keep rollback access available and report possible false positives.

Pi-hole Gravity accepts subscribed domain lists and successfully parsed the current NetCalcKit list as 13 exact domains with zero invalid entries.

## Add the subscription

1. Open the Pi-hole admin interface.
2. Open the list-management page and add this address as an enabled denylist subscription:

   ```text
   https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
   ```

3. Give it a recognizable comment such as `NetCalcKit`.
4. Run **Update Gravity** from Pi-hole's tools page, or run `pihole updateGravity` on the Pi-hole host.
5. Confirm that Pi-hole reports 13 domains from the subscription and zero invalid entries.

## Verify it

Query a listed hostname through Pi-hole and then query an unrelated control domain:

```bash
dig @YOUR_PIHOLE_IP www.google-analytics.com
dig @YOUR_PIHOLE_IP example.com
```

The listed hostname should receive Pi-hole's configured blocking response. `example.com` should resolve normally. `pihole query www.google-analytics.com` can show whether the domain came from the NetCalcKit subscription.

## Roll back

If essential functionality breaks, disable only the NetCalcKit subscription, update Gravity, and repeat the affected action. Remove the subscription only after recording the exact hostname and following `false-positive-testing.md`.

## Official references

- [Pi-hole command documentation](https://docs.pi-hole.net/main/pihole-command/)
- [Pi-hole domain database and subscribed lists](https://docs.pi-hole.net/database/domain-database/)
- [Official Pi-hole Docker documentation](https://docs.pi-hole.net/docker/)
