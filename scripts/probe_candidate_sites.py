#!/usr/bin/env python3
"""Read-only public-page baseline reconnaissance for HOLD candidates; never approves rules."""
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

TARGETS = {"ct.pinterest.com", "bat.bing.com"}
PUBLIC_SITES = [
    "https://www.ctvnews.ca/",
    "https://www.allbirds.com/",
    "https://www.wayfair.com/",
    "https://www.etsy.com/",
    "https://www.potterybarn.com/",
    "https://www.newegg.com/",
]

def hostname(url):
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""

def main():
    import shutil
    browser_path = next((p for n in ("google-chrome", "google-chrome-stable", "chromium")
                         if (p := shutil.which(n))), None)
    if not browser_path:
        print("Chrome unavailable; inconclusive")
        return 2
    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=browser_path, headless=True,
                                             args=["--no-sandbox", "--disable-dev-shm-usage"])
        for url in PUBLIC_SITES:
            context = browser.new_context(viewport={"width": 1280, "height": 800},
                                          locale="en-US", service_workers="block")
            hits = {host: 0 for host in TARGETS}
            def on_request(request):
                found = hostname(request.url)
                if found in hits:
                    hits[found] += 1
            context.on("request", on_request)
            page = context.new_page()
            row = {"url": url, "http_status": None, "title_present": False,
                   "body_length": 0, "target_requests": hits.copy(), "error": ""}
            try:
                response = page.goto(url, wait_until="domcontentloaded", timeout=16000)
                row["http_status"] = response.status if response else None
                page.wait_for_timeout(6000)
                row["title_present"] = bool(page.title().strip())
                row["body_length"] = len(page.locator("body").inner_text(timeout=2500).strip())
            except Exception as exc:
                row["error"] = type(exc).__name__
            row["target_requests"] = hits.copy()
            results.append(row)
            context.close()
        browser.close()
    report = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Identify real public pages naturally requesting exact HOLD hosts; baseline only",
        "limits": "No blocked-mode test. Bot protection and cookie consent may suppress trackers. No synthetic requests.",
        "results": results,
    }
    os.makedirs("qa-reports", exist_ok=True)
    with open("qa-reports/candidate-public-baseline.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    lines = ["# Candidate public-site baseline reconnaissance", "",
             "Presence is NOT compatibility approval; an absent host is inconclusive.", ""]
    for row in results:
        observed = ", ".join(h + "=" + str(n) for h,n in sorted(row["target_requests"].items()))
        lines.append("- " + row["url"] + ": HTTP " + str(row["http_status"]) +
                     "; body " + str(row["body_length"]) + "; " + observed +
                     ("; " + row["error"] if row["error"] else ""))
    text = "\n".join(lines) + "\n"
    print(text)
    with open("qa-reports/candidate-public-baseline.md", "w", encoding="utf-8") as f:
        f.write(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text)
    return 0  # Reconnaissance is report-only. Absent hosts do not become approved.

if __name__ == "__main__":
    raise SystemExit(main())
