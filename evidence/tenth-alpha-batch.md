# Tenth alpha research batch — 2026-09-26

Research-only batch. One candidate remains HOLD. No Standard promotion.

## analytex.userpilot.io — HOLD (high risk)

Primary evidence: https://docs.userpilot.com/api-references/real-time/bulk-identify-update

Vendor documentation explicitly identifies this hostname as a Bulk Users & Companies Update HTTP API: it synchronizes and modifies user/company profiles and also serves bulk-job status. It is **not proven to be a dedicated, non-essential tracking collection endpoint**. DNS blocking could interrupt legitimate profile synchronization and administration. Do not promote under the low-false-positive policy. A path-specific API function cannot be safely distinguished by an exact-host DNS rule.

Duplicate check against main candidates: hostname absent as of this review. No overlap with the two Contentsquare hosts in automated research PR #13. Candidate stays HOLD; no rules or release candidate changes.
