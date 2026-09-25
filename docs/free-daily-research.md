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
