# Stable release criteria

NetCalcKit uses **alpha** for early evidence-backed rules, **release candidate** for a frozen build under final review, and **stable** only after the criteria below are met. A stable label is a compatibility claim, not merely a version-number choice.

## Required gates

- [x] Every rule has independently reviewable primary evidence.
- [x] No third-party aggregate list is copied, imported, or rebranded.
- [x] The build fails on malformed, duplicate, or unsorted source data.
- [x] Unit tests cover parser failure modes.
- [x] Generated output is deterministic and validated automatically.
- [x] Database, contents, software, and documentation license texts are available locally.
- [x] All rules pass isolated AdGuard Home enforcement with a normal control domain.
- [x] All current hosts resolve and reach their dedicated HTTPS services from two independent environments.
- [ ] Every rule has representative application-level evidence, or a documented equivalent review approved for the stable scope.
- [ ] The subscription is enforced successfully on a second supported DNS filtering platform.
- [ ] A frozen release candidate completes a public alpha soak period without an unresolved critical or high-severity false positive.
- [ ] Stable installation, rollback, support scope, and immutable subscription documentation are finalized.

## Current assessment

The 13-rule candidate is technically valid and suitable for alpha testing. Six rules have limited public-page application evidence; seven specialized regional or account-specific rules remain unexercised. AdGuard Home is the only directly verified consumer platform. The project therefore does not yet meet its own stable-release gates.

## Promotion rule

Do not publish a stable GitHub release while a required gate is open. If a gate cannot be satisfied for a rule, either keep that rule in an explicitly experimental list or remove it from the stable list before promotion.
