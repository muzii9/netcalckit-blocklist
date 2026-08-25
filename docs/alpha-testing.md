# Alpha compatibility test record

SPDX-License-Identifier: CC-BY-4.0

Tested: 2026-08-25

## Scope

This is a release-readiness smoke test for the seven exact hostnames in the first NetCalcKit alpha batch. It confirms that each hostname resolves and that its HTTPS service is reachable before blocking. It does not prove compatibility with every website or application.

## Results

| Hostname | DNS | HTTPS response | Risk classification |
| --- | --- | --- | --- |
| `api.eu.amplitude.com` | Resolved | 400 at root path | Moderate; event-ingestion endpoint |
| `api2.amplitude.com` | Resolved | 400 at root path | Moderate; event-ingestion endpoint |
| `region1.google-analytics.com` | Resolved | 404 at root path | Low to moderate; exact collection host |
| `script.hotjar.com` | Resolved | 403 at root path | Low to moderate; exact script host |
| `static.hotjar.com` | Resolved | 200 at root path | Low to moderate; exact static service host |
| `www.clarity.ms` | Resolved | 200 at root path | Moderate; collection and service resources |
| `www.google-analytics.com` | Resolved | 200 at root path | Low to moderate; exact analytics host |

HTTP error codes at a root path are expected for API or resource hosts and do not indicate that the documented collection endpoint is unavailable.

## Independent-device verification

The same seven checks were repeated from the separately administered Ubuntu host `my-home-server` on 2026-08-25. Every hostname resolved, and each returned the same HTTP status class and exact status code observed during the primary test:

- Amplitude ingestion hosts: 400
- Google Analytics regional collection host: 404
- Hotjar script host: 403
- Hotjar static host, Microsoft Clarity, and standard Google Analytics host: 200

No DNS, firewall, SSH, or system configuration was changed on the server during this read-only test.

## Release decision

- All seven exact hostnames are retained for the alpha.
- No wildcard or vendor apex domain is added.
- Amplitude and Clarity rules remain explicitly marked moderate-risk.
- Reports of broken essential functionality should use the false-positive issue form.
- A confirmed material false positive is grounds for immediate allowlisting or rule removal.

## Reproducibility

The repository was freshly cloned, `python3 scripts/build.py` was run, followed by `python3 scripts/validate.py`. Validation passed and the generated working tree remained unchanged.
