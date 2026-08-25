# Pi-hole enforcement test

Tested: 2026-08-25

## Environment

- Pi-hole Core v6.4.3, Web v6.6
- Official `pihole/pihole:latest` image at digest `sha256:f7d1be836e3bc608b56d82fc9904f5a831cdfbc0dc9c6d58f94e4c985c70038b`
- Isolated Docker container on `my-home-server`
- DNS exposed only on host loopback port 3153 during the test
- Web interface exposed only on host loopback port 3180 during the test
- Restart policy disabled
- NetCalcKit was the only subscribed denylist during the final run
- Existing router, client DNS, AdGuard Home, and Portainer settings were unchanged

## Subscription result

Pi-hole Gravity downloaded:

```text
https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
```

Gravity reported:

- 13 exact domains parsed;
- 13 unique gravity domains;
- 0 ABP-style domains;
- 0 invalid or ignored entries;
- successful list status.

## DNS result

Every one of the 13 current list hostnames returned Pi-hole's blocking response. The unrelated control domain `example.com` returned normal public IPv4 answers.

Result: **13/13 blocked; control domain resolved normally.**

## Cleanup

The disposable Pi-hole test container and its dedicated volume were removed after the result was recorded. The downloaded official image was left in Docker's image cache. No production DNS service was changed.

## Scope

This verifies subscription parsing, Gravity ingestion, and DNS enforcement in Pi-hole. It does not expand the application-level false-positive claims recorded in `application-testing.md`.
