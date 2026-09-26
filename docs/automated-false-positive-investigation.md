# Automated false-positive investigator (v1)

This is a read-only, bounded public-site investigation workflow. It **does not edit
rules, approve candidates, submit forms, access private accounts, or publish lists**.
A green *report-only* workflow means the investigation itself ran, **not** that the
tracked domains are safe. Read the explicit per-host statuses in its artifact.

## Workflow

- GitHub Actions: Automated false-positive investigation
- Events: every pull request that updates rule/candidate/approved-list or investigator code;
  weekly Thursday 04:15 UTC (09:15 PKT); and optional manual dispatch.
- It validates its safety/risk classification offline before opening a browser.
- It uses the reviewed public-page pool and research pins from
  tests/false-positive-investigator.json plus the approved-site case registry.
- NEW approved Standard rules are prioritized on release-candidate PRs.
- For routine research it checks two explicit research pins and one rotating HOLD
  candidate from candidates/candidates.csv. No more than three target hosts
  or six public seed pages per host are explored in one run.
- It observes a target only when an *independent public site naturally requests*
  its exact DNS hostname. It does not create synthetic tracker traffic.
- For up to two public sites per host, it runs normal -> exact-host-blocked ->
  exact-host-blocked -> normal, with clean browser contexts and seven seconds of
  observation on each visit. Each blocked request fails with a DNS-like error.
- It records the count of naturally requested vs failed exact-host requests,
  repeated request amplification, DOM-loaded timing, uncaught JS error count,
  other failed-request count, readable body length and public-link count.
  Error *contents*, query strings, tracking payloads, cookies and private URLs
  are never written to its report.
- Basic public-page rendering can be checked automatically. Arbitrary checkout,
  sign-in, purchases and private or side-effecting interactive flows cannot
  be safely verified by this browser run.

## Classification

- LIMITED_SMOKE_PASS: target naturally exercised in *both* baseline trials,
  intercepted in *both* blocked trials, and none of the measured basic
  smoke signals crosses its conservative warning threshold. This is **not**
  universal compatibility approval.
- REVIEW_REQUIRED: reproducible content/link degradation, unusually large
  repeated failed-request counts, an appreciable DOM-load regression signal,
  many newly uncaught JS errors, or a substantial increase in other network
  errors. These are signals for further review, not proof of end-user harm.
- INCONCLUSIVE: no natural request, public site blocks automation, a redirect
  changes site scope, or a repeated trial did not finish. This is **not** a pass.

The reproducible request threshold is **15 or more blocked attempts AND more
than four times the normal median**, based on two normal and two blocked trials.
DOM-load timing is noisy on shared cloud runners and must never be the only
proof of a user-visible regression. The initial Pinterest experiments previously
showed 3 normal vs 32 blocked requests in both repeats on two independent
merchant pages, so this threshold intentionally flags that pattern.

## Publication guardrail

For a pull request that introduces a new *approved Standard* hostname, the
investigator compares that PR's rule database with its base commit. Every
new proposed hostname must fit within the bounded test run and receive a
LIMITED_SMOKE_PASS, or **the workflow fails and leaves the PR for human review**.
This is an additional automated gate, not permission to merge: real AdGuard
enforcement, first-party evidence, complex app compatibility and explicit
maintainer approval remain independent requirements.

An existing HOLD or research-only host never becomes an approved rule through
this workflow. On a weekly or ordinary research run, review-required and
inconclusive findings are warnings in the GitHub job summary and archived JSON
and Markdown; a successful job does not imply the host was cleared.

GitHub Actions artifacts (21-day retention):
false-positive-investigation/false-positive-investigation.json and
false-positive-investigation/false-positive-investigation.md.

## Coverage boundaries and resource limits

The site pool is intentionally small and versioned. Discovery means searching
that *reviewed public-site pool*, not an unrestricted crawler of the entire web.
Unknown hosts may remain INCONCLUSIVE until a genuine public site is added to
the pool or its exact approved-host case registry. Never invent a website
request or use a first-party vendor script to manufacture compatibility.
No separate search API quota or GitHub write permission is required.

Browser request interception mimics failure and may produce different retries
from an actual subscribed DNS provider. Use the existing isolated AdGuard Home
DNS lab and additional resource-performance investigation for suspicious
cases. Don't add a domain simply to increase a published rule count.
