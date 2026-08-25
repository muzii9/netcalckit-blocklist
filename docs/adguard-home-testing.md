# Isolated AdGuard Home test

SPDX-License-Identifier: CC-BY-4.0

Tested: 2026-08-25

## Environment

- Host: `my-home-server`
- OS: Ubuntu 24.04 LTS, x86_64
- Runtime: Docker
- AdGuard Home: `v0.107.79`
- Container: `netcalckit-adguard-test`
- DNS listener: `127.0.0.1:3053` over TCP and UDP
- Admin listener: `127.0.0.1:3080`
- Restart policy: disabled

The non-standard loopback ports keep the test isolated. The host's existing DNS listener, router configuration, Portainer container, and client DNS settings were not changed.

## Filter configuration

Only the NetCalcKit subscription was enabled for the test:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
```

AdGuard Home reported exactly seven loaded rules. Its bundled AdGuard DNS and AdAway filters were disabled before testing, preventing unrelated rules from affecting the result.

## DNS results

| Query | Result |
| --- | --- |
| `api.eu.amplitude.com` | Blocked as `0.0.0.0` |
| `api2.amplitude.com` | Blocked as `0.0.0.0` |
| `region1.google-analytics.com` | Blocked as `0.0.0.0` |
| `script.hotjar.com` | Blocked as `0.0.0.0` |
| `static.hotjar.com` | Blocked as `0.0.0.0` |
| `www.clarity.ms` | Blocked as `0.0.0.0` |
| `www.google-analytics.com` | Blocked as `0.0.0.0` |
| `example.com` control query | Resolved normally |

## Conclusion

The standard list is accepted by AdGuard Home as a one-domain-per-line subscription, all seven current rules are enforced, and an unrelated control domain remains resolvable. This confirms list-format and DNS-enforcement compatibility; broader application-level false-positive testing remains ongoing.
