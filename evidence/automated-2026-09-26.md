# Automated documentation scan — 2026-09-26

Discovery only. Both candidates remain HOLD. No release candidate or published rules changes.

Primary vendor documentation: https://docs.contentsquare.com/en/web/requests/

## srm.bf.contentsquare.net — HOLD

Vendor documents `https://srm.bf.contentsquare.net/exist` and `/putTag` as US/AWS collection of non-public resources during session data collection, including resources behind authentication. This is session-replay-related resource collection, **not proven to be exclusively non-essential tracking**. Blocking could affect replay/resource behavior. Dedicated-service, essential-function, and DNS health require further verification; no Standard promotion.

## srm.af.contentsquare.net — HOLD

Vendor documents `https://srm.af.contentsquare.net/exist` and `/putTag` as US/Azure collection of non-public resources during session data collection, including resources behind authentication. Same risk and verification requirements as above; no Standard promotion.

## Duplicate and promotion review

Neither hostname appears in main's 13 staged candidates as of review. Neither overlaps batch 010's Userpilot hostname. These are only documentation-based findings, not independently verified safe DNS block rules. Keep both HOLD; do not publish or open Standard RC.
