# Automatic draft release proposals

NetCalcKit can automate the repetitive path from a researched candidate to a **draft**
Standard release-candidate pull request. It still does **not** auto-merge or auto-publish.

## End-to-end flow

1. Daily official-document research finds plausible exact collection hostnames.
2. Strong deterministic discoveries enter `candidates/candidates.csv` with status
   `research`. Explicit maintainer `hold` and `rejected` rows are never eligible for
   automatic release proposals.
3. The automatic RC proposer selects at most one conservative candidate.
4. It runs the existing false-positive investigator against a bounded, reviewed
   public-site pool. It never fabricates tracker requests.
5. The candidate must naturally appear on at least **two independent public sites**.
   Each site gets two normal and two exact-host-failed browser trials.
6. Both sites must remain `LIMITED_SMOKE_PASS`. `REVIEW_REQUIRED`,
   `INCONCLUSIVE`, bot-protected pages, one-site evidence, or no natural request
   produce **no release proposal**.
7. Only then does automation stage a branch with:
   - an evidence record;
   - one proposed approved Standard rule;
   - removal of that hostname from the candidate queue;
   - the naturally exercised public pages in `tests/live-site-cases.json`;
   - rebuilt generated blocklist files; and
   - the updated moving-main rule count.
8. GitHub opens the result as a **DRAFT pull request**. The normal rule validation,
   candidate checks, real-site browser tests, strict false-positive investigation,
   and isolated AdGuard Home lab run again on the proposed RC.
9. A maintainer must inspect those results and explicitly approve the merge.

There is no automated merge step.

## Deterministic pre-browser exclusions

The proposer refuses automatic RC preparation when any of these apply:

- candidate status is `hold` or `rejected`;
- evidence is not vendor documentation, vendor code, or a first-party config;
- shared infrastructure or essential function is explicitly `yes`;
- dedicated service is explicitly `no`;
- false-positive risk is `high`;
- the hostname is a broad/apex-style domain rather than a subdomain;
- category indicates authentication, payment, billing, security, updates, CDN/SDK
  delivery, experimentation, or another mixed/essential role;
- research notes already warn about login, checkout, mixed-purpose use, SDK
  delivery, shared infrastructure, guide metadata, or similar essential behavior.

Unknown metadata is not silently treated as safe. If a candidate with unknown
false-positive risk ever reaches a draft proposal through strong two-site browser
evidence, the proposed rule is conservatively recorded as `moderate` risk for
human review.

## Scheduling

`.github/workflows/auto-release-proposal.yml` runs:

- immediately after relevant candidate/config changes are merged to `main`;
- daily at 04:45 UTC (09:45 Pakistan time);
- manually through GitHub Actions.

The daily research workflow runs earlier at 03:17 UTC. Its research PR must still
be explicitly merged before any newly discovered candidate can enter the automatic
RC proposal stage.

## What a green job means

A green `Automatic draft RC proposer` job only means the workflow executed
according to policy. It may legitimately create **no PR** because:

- there is no eligible research-stage candidate;
- an open PR already exists for the selected hostname;
- the hostname is not naturally exercised in the bounded public-site pool;
- fewer than two independent sites exercise it;
- the false-positive investigator returned `REVIEW_REQUIRED` or `INCONCLUSIVE`.

If it does create a draft RC, that is still a proposal rather than publication.

## Security and privacy boundaries

The proposer:

- does not log into sites;
- does not submit checkout, payment, forms, or user data;
- does not store cookies, query strings, tracker payloads, or JavaScript error text;
- does not crawl arbitrary private/internal hosts;
- does not modify router or user DNS settings;
- does not grant itself permission to merge;
- never treats AI output alone as publication evidence.

Browser interception approximates name-resolution failure. The separate AdGuard
Home lab remains the actual isolated DNS-enforcement gate.

## Quotas and cost

The RC proposer itself uses GitHub-hosted browser testing and no paid search API.
The optional daily Gemini/Tavily research remains independently quota-limited and
report-only; it does not bypass this proposal gate.
