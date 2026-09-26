#!/usr/bin/env python3
"""Read-only A/B public-site smoke test. An unexercised host is NOT a pass."""
import json
import csv
import io
import re
import subprocess
from pathlib import Path
import os
import shutil
import sys
from datetime import datetime, timezone
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CASES_FILE = ROOT / "tests" / "live-site-cases.json"
RULES_FILE = ROOT / "rules" / "rules.csv"
HOST_PATTERN = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}")

def approved_from_csv(raw):
    return {row["domain"] for row in csv.DictReader(io.StringIO(raw))
            if row["status"] == "approved"}

def load_cases(path=CASES_FILE, rules_path=RULES_FILE):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
        raise ValueError("Expected live-site cases schema_version 1 and cases array")
    approved = approved_from_csv(rules_path.read_text(encoding="utf-8"))
    seen = set()
    cases = []
    for case in data["cases"]:
        vendor, target = case["vendor"], case["host"]
        seconds, pages = case["wait_seconds"], case["pages"]
        if not isinstance(vendor, str) or not vendor.strip():
            raise ValueError("Every browser case needs a vendor")
        if not isinstance(target, str) or not HOST_PATTERN.fullmatch(target):
            raise ValueError("Browser case must use an exact lowercase hostname")
        if target in seen:
            raise ValueError("Duplicate browser case for " + target)
        if target not in approved:
            raise ValueError("Browser case targets an unapproved rule: " + target)
        if type(seconds) is not int or not 1 <= seconds <= 20:
            raise ValueError("wait_seconds must be an integer from 1 to 20")
        if not isinstance(pages, list) or not 1 <= len(pages) <= 5:
            raise ValueError("Each browser case needs 1 to 5 public pages")
        for url in pages:
            if not isinstance(url, str):
                raise ValueError("Browser case URL must be HTTPS text")
            parsed = urlsplit(url)
            if (parsed.scheme != "https" or not parsed.hostname or parsed.username
                    or parsed.password or parsed.query or parsed.fragment):
                raise ValueError("Use public HTTPS URLs without credentials or query data")
        seen.add(target)
        cases.append((vendor, target, seconds, pages))
    return cases

def newly_approved_hosts(base_sha, current_path=RULES_FILE):
    """Require a public-page test mapping when a PR adds a new approved rule."""
    if not base_sha:
        return set()
    if not re.fullmatch(r"[0-9a-f]{40,64}", base_sha):
        raise ValueError("Invalid BASE_SHA")
    old = subprocess.run(["git", "show", base_sha + ":rules/rules.csv"],
                         cwd=ROOT, text=True, capture_output=True,
                         check=True, timeout=15).stdout
    current = current_path.read_text(encoding="utf-8")
    return approved_from_csv(current) - approved_from_csv(old)

def host(url):
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""

def capture(browser, url, target, seconds, blocked):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800},
                              locale="en-US", service_workers="block")
    requested = []
    prevented = []
    ctx.on("request", lambda r: requested.append(target) if host(r.url) == target else None)
    if blocked:
        def intercept(route):
            if host(route.request.url) == target:
                prevented.append(target)
                route.abort(error_code="namenotresolved")
            else:
                route.continue_()
        ctx.route("**/*", intercept)
    page = ctx.new_page()
    result = {"url": url, "http": None, "title": False, "body": 0,
              "links": 0, "h1": False, "requests": 0, "blocked_requests": 0,
              "error": ""}
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
        result["http"] = response.status if response else None
        page.wait_for_timeout(seconds * 1000)
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)[:100]
    try:
        result["title"] = bool(page.title().strip())
        result["body"] = len(page.locator("body").inner_text(timeout=4000).strip())
        result["links"] = page.locator("a[href]").count()
        result["h1"] = page.locator("h1").count() > 0
    except Exception:
        pass
    result["requests"] = len(requested)
    result["blocked_requests"] = len(prevented)
    ctx.close()
    return result

def main():
    cases = load_cases()
    new_hosts = newly_approved_hosts(os.environ.get("BASE_SHA", ""))
    missing = sorted(new_hosts - {case[1] for case in cases})
    from playwright.sync_api import sync_playwright
    browser_path = next((p for name in ("google-chrome", "google-chrome-stable", "chromium")
                         if (p := shutil.which(name))), None)
    if not browser_path:
        print("Missing preinstalled Chrome browser")
        return 2
    report = {"utc": datetime.now(timezone.utc).isoformat(), "results": [], "newly_approved": sorted(new_hosts),
              "missing_cases": missing,
              "scope": "Unauthenticated public pages; exact-host HTTP interception emulates DNS failure",
              "limitations": "Basic core-render presence only, no logins/payments; baseline must naturally request host."}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=browser_path,
                                             args=["--no-sandbox", "--disable-dev-shm-usage"])
        for vendor, target, seconds, pages in cases:
            case = {"vendor": vendor, "host": target, "status": "inconclusive", "attempts": []}
            for url in pages:
                baseline = capture(browser, url, target, seconds, False)
                attempt = {"baseline": baseline}
                if baseline["http"] is not None and baseline["http"] >= 400:
                    attempt["note"] = "Main page returned HTTP error"
                elif baseline["body"] < 250:
                    attempt["note"] = "Insufficient readable content"
                elif baseline["requests"] == 0:
                    attempt["note"] = "Target not requested naturally; no rule-level evidence"
                else:
                    filtered = capture(browser, url, target, seconds, True)
                    attempt["blocked"] = filtered
                    intact = (filtered["blocked_requests"] > 0 and
                        (filtered["http"] is None or filtered["http"] < 400) and
                        filtered["title"] and filtered["body"] >= max(250, baseline["body"] * .6) and
                        (baseline["links"] < 5 or filtered["links"] >= baseline["links"] * .6) and
                        (not baseline["h1"] or filtered["h1"]))
                    if filtered["blocked_requests"] == 0:
                        case["status"] = "inconclusive"
                        attempt["note"] = "No target interception in blocked mode"
                    else:
                        case["status"] = "preliminary-pass" if intact else "fail"
                        attempt["note"] = "Basic core render comparison only"
                case["attempts"].append(attempt)
                if "blocked" in attempt:
                    break
            report["results"].append(case)
        browser.close()
    os.makedirs("qa-reports", exist_ok=True)
    with open("qa-reports/live-browser-smoke.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    rows = ["# Public real-site A/B smoke", "", "Only pages naturally requesting the exact host count.", "",
            "Newly approved rules on this PR: " + (", ".join(sorted(new_hosts)) or "none"),
            "Missing live-site test mappings: " + (", ".join(missing) or "none"), ""]
    for case in report["results"]:
        rows.append(case["vendor"] + " / " + case["host"] + ": **" + case["status"] + "**")
        for a in case["attempts"]:
            b = a["baseline"]
            line = "- " + b["url"] + " — baseline HTTP " + str(b["http"])
            line += ", body " + str(b["body"]) + ", target requests " + str(b["requests"])
            if "blocked" in a:
                line += "; blocked body " + str(a["blocked"]["body"])
                line += ", intercepted " + str(a["blocked"]["blocked_requests"])
            line += "; " + a["note"]
            rows.append(line)
        rows.append("")
    rows += ["Limitations: " + report["limitations"]]
    summary = "\n".join(rows) + "\n"
    print(summary)
    with open("qa-reports/live-browser-smoke.md", "w", encoding="utf-8") as f:
        f.write(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(summary)
    if missing:
        return 3  # New approved rules without public-page mapping must be reviewed.
    if any(c["status"] == "fail" for c in report["results"]):
        return 1
    return 0 if all(c["status"] == "preliminary-pass" for c in report["results"]) else 2

if __name__ == "__main__":
    sys.exit(main())
