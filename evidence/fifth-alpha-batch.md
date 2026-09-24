# Fifth alpha batch

SPDX-License-Identifier: CC-BY-4.0

Reviewed: 2026-09-24

This batch adds eight exact hostnames used by the LinkedIn Insight Tag and related website measurement infrastructure. The sources below are official LinkedIn documentation. These rules target advertising measurement, conversion tracking, retargeting, and website analytics infrastructure; they are not being labeled as malicious.

## LinkedIn Insight Tag and website measurement

Sources:

- https://www.linkedin.com/help/linkedin/answer/a418880
- https://www.linkedin.com/help/linkedin/answer/a425696
- https://www.linkedin.com/help/linkedin/answer/a489169
- https://business.linkedin.com/content/dam/lem/business/en/advertise/ads/targeting/linkedIn-matched-audiences-final.pdf

LinkedIn documents the Insight Tag as code used for campaign reporting, conversion tracking, website audiences, retargeting, and audience insights. Its troubleshooting documentation lists the hostnames below as domains that must not be blocked when troubleshooting Insight Tag loading. LinkedIn's installation material also shows the tag script loading from `snap.licdn.com` and the image pixel using `px.ads.linkedin.com`.

| Hostname | Category | Why it is included | False-positive risk | Decision |
| --- | --- | --- | --- | --- |
| `snap.licdn.com` | Advertising measurement / tag delivery | Official Insight Tag JavaScript host | Moderate: blocks LinkedIn Insight Tag loading and any site code that incorrectly depends on the tag | Include for alpha testing |
| `px.ads.linkedin.com` | Conversion / retargeting pixel | Official Insight Tag image-pixel and collection host | Low to moderate: blocks LinkedIn conversion and retargeting measurement | Include |
| `px4.ads.linkedin.com` | Advertising measurement | Listed by LinkedIn as required for Insight Tag operation | Low to moderate: disables related measurement requests | Include |
| `p.adsymptotic.com` | Advertising measurement | Listed by LinkedIn as required for Insight Tag operation | Moderate: exact advertising-related service host, but compatibility still needs app/site testing | Include for alpha testing |
| `cdn.linkedin.oribi.io` | Website analytics / tag support | Listed by LinkedIn as required for Insight Tag operation | Moderate: may disable LinkedIn-owned analytics resources loaded through Oribi infrastructure | Include for alpha testing |
| `gw.linkedin.oribi.io` | Website analytics / event gateway | Listed by LinkedIn as required for Insight Tag operation | Moderate: may disable LinkedIn-owned analytics event delivery | Include for alpha testing |
| `dc.ads.linkedin.com` | Advertising measurement | Listed by LinkedIn as required for Insight Tag operation | Low to moderate: exact ads/measurement service host | Include |
| `sjs.bizographics.com` | Advertising / audience measurement | Listed by LinkedIn as required for Insight Tag operation | Moderate: disables related audience-measurement script delivery | Include for alpha testing |

## Scope and exclusions

- The broad `linkedin.com` apex listed in troubleshooting documentation is deliberately excluded because it provides essential user-facing LinkedIn functionality.
- The path `px.ads.linkedin.com/wa` does not create a separate DNS rule because DNS filtering operates on the hostname `px.ads.linkedin.com`.
- No wildcard, LinkedIn login, account, messaging, feed, or other broad user-facing hostname is included.
- No third-party aggregate blocklist was imported or used as sole evidence.
- These rules should be removed or allowlisted if a reproducible material false positive is found.

## Validation status

Primary-source review and false-positive scoping are complete. DNS enforcement and compatibility checks for this batch should be run in the project's isolated AdGuard Home test environment before promotion to a stable release.
