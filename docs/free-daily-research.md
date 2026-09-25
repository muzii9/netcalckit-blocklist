# Free daily research pilot

This workflow uses GitHub Actions and Python only. No OpenAI API or paid AI service.

- Scheduled daily at 03:17 UTC (08:17 Pakistan time), with optional manual dispatch. GitHub may delay scheduled jobs.
- Scans three explicitly registered official vendor documentation pages. It is **not** an autonomous general web-search engine; expand the registry after reviewing vendor documentation.
- Discovers up to 30 exact hostnames within registered vendor suffixes. It rejects existing candidates, existing rules, allowlisted names, vendor apexes and common risky infrastructure labels.
- Every discovery is **HOLD** with unknown essential/shared-service flags. Page-text presence is a discovery signal, **not** proof of tracking or permission to block.
- If new candidates exist, opens a draft PR and triggers the existing candidate review and validation workflows. No new candidates means no PR.
- Does not modify rules, generated blocklists, main, or create Standard release-candidate PRs.
- The scheduled job only starts after this automation PR is reviewed and merged into main.

## Telegram (optional)

Create a Telegram bot using BotFather and send it a private message. Obtain your own chat ID securely. In GitHub repository Settings > Secrets and variables > Actions, add **repository secrets** `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. Never paste the token in a PR, chat or source code. Until secrets are configured, the workflow logs a notification skip.

GitHub Actions may require Settings > Actions > General > Workflow permissions: **Read and write permissions**, and permission to create pull requests. Configure these in repository settings if the draft PR step reports insufficient permissions.

## Seven-day pilot review

Review daily workflow runs and draft PRs. Inspect candidate-review artifacts for DNS health, validate the documentation context manually, and record false-positive concerns. A clean DNS result does not prove a hostname is safe to block. If documentation fetch fails, the scanner records an error and does not fabricate evidence.

No automated promotion or merge is permitted.

## Optional Gemini + Tavily research (free quotas only)

Add repository Actions secrets `GEMINI_API_KEY` and `TAVILY_API_KEY`. The workflow makes at most 24 basic Tavily searches and 24 Gemini analysis requests per daily run, then uploads `free-ai-research-report` as a workflow artifact. Gemini model: `gemini-3.1-flash-lite`; model availability and free-tier quotas must be confirmed in your own account. API failures do not automatically trigger paid fallback.

AI suggestions are **not** added to the candidate database: they are report-only, remain unverified HOLD suggestions, and require independent first-party documentation review. The deterministic scanner separately stages only documented hostnames as HOLD. Never enable paid billing just to run this workflow; watch both providers' dashboards for quota changes.

### Verified free-tier budgeting (September 2026)

Tavily Researcher includes 1,000 free credits per calendar month. Basic search costs 1 credit; advanced costs 2. This pilot performs 24 **basic** searches per day, maximum 744 in a 31-day month, leaving 256 credits for safety. If this key is shared with other projects, reduce the daily budget accordingly. Do not upgrade or enable pay-as-you-go. Tavily resets on the first of each month.

Gemini 3.1 Flash-Lite is listed with free-tier text usage, but per-project request/day and token limits vary; inspect the actual project in Google AI Studio. Your AI Studio project shows Gemini 3.1 Flash-Lite at 15 RPM, 250K TPM and 500 RPD. This workflow schedules 24 analyses/day (744 in a 31-day month), below that project's daily limit; quota may change. Failed or rate-limited calls are logged and must never trigger paid fallback. Gemini's own search grounding is not enabled; Tavily supplies excerpts.

The initial registry contains three vendors, so 24 search variations/day may overlap. Expand official vendor coverage and deduplicate research results during the pilot before treating search volume as useful discovery.
