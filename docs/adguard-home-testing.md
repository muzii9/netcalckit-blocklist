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

The non-standard loopback ports keep the test isolated. The host's existing DNS listener, router configuration, Portainer container, and client DNS settings were not changed. The test admin endpoint is reachable only from the server loopback interface.

## Filter configuration

Only the NetCalcKit subscription was enabled for the test:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
```

AdGuard Home reported exactly 13 loaded rules after the second batch was published and refreshed. Its bundled AdGuard DNS and AdAway filters were disabled before testing, preventing unrelated rules from affecting the result.

## DNS results

| Query group | Result |
| --- | --- |
| 7 first-batch hostnames | All blocked as `0.0.0.0` |
| 6 second-batch New Relic and Datadog hostnames | All blocked as `0.0.0.0` |
| `example.com` control query | Resolved normally |

Second-batch exact results:

| Query | Result |
| --- | --- |
| `bam-cell.nr-data.net` | Blocked as `0.0.0.0` |
| `bam.eu01.nr-data.net` | Blocked as `0.0.0.0` |
| `bam.nr-data.net` | Blocked as `0.0.0.0` |
| `browser-intake-datadoghq.com` | Blocked as `0.0.0.0` |
| `browser-intake-datadoghq.eu` | Blocked as `0.0.0.0` |
| `js-agent.newrelic.com` | Blocked as `0.0.0.0` |

## Conclusion

The standard list is accepted by AdGuard Home as a one-domain-per-line subscription, all 13 current rules are enforced, and an unrelated control domain remains resolvable. This confirms list-format, subscription-refresh, and DNS-enforcement compatibility; broader application-level false-positive testing remains ongoing.
