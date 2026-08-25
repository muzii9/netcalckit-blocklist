# Preliminary Source and License Review

Review date: 2026-08-25

This document records the initial review of candidate upstream DNS blocklists. It is not legal advice. No candidate is approved for ingestion until the project licensing model is selected and attribution requirements are documented.

## Evaluation criteria

- Clear redistribution terms from a primary source
- Active maintenance and public issue reporting
- DNS-compatible downloadable format
- False-positive posture suitable for a standard/balanced list
- Traceable provenance and attribution requirements

## Candidates

### HaGeZi DNS Blocklists — Normal

- Project: https://github.com/hagezi/dns-blocklists
- License: GNU General Public License v3.0
- Format considered: wildcard domains / only-domains
- Maintenance: actively maintained, with public issues, mirrors, multiple blocking levels, and documented sources
- Fit: strong technical candidate for a balanced list; the maintainer describes Normal as relaxed/balanced and designed to avoid restrictions for the most part
- Concern: it is already a large aggregated list. Redistributing a transformed derivative requires GPL compliance, preserved notices, modification notices, and complete attribution/provenance review

Status: **Shortlisted, not approved**

### OISD Small

- Project: https://oisd.nl/
- License: GNU General Public License v3.0
- Format considered: DNS domain list
- Maintenance: domains are pruned regularly; the project emphasizes low breakage and documents exclusions
- Fit: strong false-positive posture for a conservative standard list
- Concern: it is an aggregator, so combining it with other aggregators adds duplication and makes source-level provenance harder to explain

Status: **Shortlisted, not approved**

### AdGuard DNS Filter

- Project: https://github.com/AdguardTeam/AdGuardSDNSFilter
- License: GNU General Public License v3.0
- Format considered: AdGuard DNS filtering syntax
- Maintenance: actively maintained and used by AdGuard Home and public AdGuard DNS
- Fit: established DNS-focused filter
- Concern: the upstream explicitly notes that extracting only hosts/domains does not make much sense. The current NetCalcKit parser does not support AdGuard rule syntax or modifiers, so adding it now would silently discard useful rules

Status: **Deferred until parser support is designed**

### StevenBlack Hosts

- Project: https://github.com/StevenBlack/hosts
- Repository license: MIT
- Format considered: hosts file
- Maintenance: actively maintained, with documented sources and issue routing
- Fit: technically compatible with the current parser
- Concern: the unified output aggregates multiple upstream lists with different licenses, including attribution-bearing sources. The repository-level MIT file alone should not be treated as proof that every incorporated upstream entry can be redistributed without preserving its applicable notices

Status: **Deferred pending per-source license review**

## Preliminary recommendation

Use one curated upstream family for the first release instead of combining several all-in-one aggregators.

The leading technical candidates are:

1. **HaGeZi Normal** for broader balanced protection.
2. **OISD Small** for a more conservative, low-breakage profile.

If either GPL-3.0 candidate is used to create and publicly redistribute a transformed list, the project should adopt a GPL-compatible distribution model for the generated blocklist and preserve source, copyright, license, and modification notices. The scripts can be licensed separately if desired, but that creates a multi-license repository and should be documented clearly.

## Required decision before ingestion

Choose one path:

- **GPL-first:** use a shortlisted GPL-3.0 source and distribute the generated blocklist under GPL-3.0 with complete notices.
- **Permissive-first:** research and combine only primary sources with verified permissive/data licenses; this takes longer but avoids building the initial dataset on a GPL aggregator.
- **Original curation:** publish only independently reviewed NetCalcKit entries at first; lowest license complexity, highest maintenance effort.

Until a path is selected, `sources/sources.txt` must remain empty and no project license should be added.
