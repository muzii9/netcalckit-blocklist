# Ninth alpha research batch — 2026-09-25

Research reviewed current first-party documentation for browser analytics and data-collection services. No hostname met the project's strict low-false-positive promotion threshold in this pass.

## Adobe Experience Platform

`edge.adobedc.net` is documented by Adobe as an Edge Network endpoint used for data collection. The same platform supports personalization, advertising, marketing, Analytics, and other Experience Cloud services. Because the hostname is mixed-purpose, it is not suitable for Standard promotion.

Evidence: https://developer.adobe.com/data-collection-apis/docs/endpoints/

## Decision

- Standard promotions: 0
- Release-candidate PR: not created
- Main branch remains unchanged

This pass intentionally prioritizes false-positive safety rather than filling the research cap with weak candidates.
