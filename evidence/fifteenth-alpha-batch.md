# Fifteenth candidate review — Optimizely

Reviewed: 2026-09-29

## Primary vendor evidence

Optimizely documents `logx.optimizely.com/v1/events` as its Event API endpoint used by Web Experimentation and Feature Experimentation to send event data to Optimizely backend servers.

Sources:
- https://docs.developers.optimizely.com/experimentation-data/docs/send-events-overview
- https://docs.developers.optimizely.com/experimentation-data/docs/event-api-getting-started
- https://docs.developers.optimizely.com/experimentation-data/reference/post_events

## Candidate

- `logx.optimizely.com`

Assessment:
- Dedicated service: yes
- Shared infrastructure: no evidence from reviewed first-party documentation
- Essential site function: no; documented purpose is experimentation event ingestion
- False-positive risk: low-moderate
- Initial status: research

## Exclusions

No broad Optimizely apex, CDN/datafile, account, authentication, administration, or inferred wildcard hosts are included.

## Promotion gate

Research only until repository candidate-review, validation, DNS-health, and isolated AdGuard release-candidate enforcement all pass. Human review remains mandatory before merge.
