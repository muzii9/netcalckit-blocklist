#!/usr/bin/env python3
"""Repeat public Pinterest-host A/B experiments and flag retry amplification.

Browser request blocking approximates a DNS error, not complete device-level DNS testing.
No accounts, user data, synthetic analytics events, or site mutations.
"""
import json
import os
import shutil
import statistics
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit

SITES = ("https://oddmuse.co.uk/", "https://bydeeaus.com/")
TARGET = "ct.pinterest.com"
OBSERVE_MS = 12000
# A conservative review trigger, not a universal safety threshold.
MIN_RETRY_BURST = 15
RETRY_MULTIPLIER = 4

def exact_host(url):
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""

def audit_pair(baselines, blocked):
    """Pure, fail-closed classification of one site's repeated A/B results."""
    if len(baselines) != 2 or len(blocked) != 2:
        return "inconclusive", ["Missing paired repeats"]
    if any(x["http"] != 200 or x["body"] < 250 or x["requests"] == 0 for x in baselines):
        return "inconclusive", ["Baseline did not load and naturally exercise exact host twice"]
    if any(x["http"] != 200 or x["intercepted"] == 0 or x["body"] < 250 for x in blocked):
        return "inconclusive", ["Blocked experiment did not fully exercise exact host twice"]
    base_requests = statistics.median(x["requests"] for x in baselines)
    blocked_attempts = statistics.median(x["intercepted"] for x in blocked)
    base_body = statistics.median(x["body"] for x in baselines)
    blocked_body = statistics.median(x["body"] for x in blocked)
    reasons = []
    if blocked_body < 0.7 * base_body or any(not x["title"] for x in blocked):
        reasons.append("Basic page rendering degraded under exact-host blocking")
    if blocked_attempts >= MIN_RETRY_BURST and blocked_attempts > RETRY_MULTIPLIER * base_requests:
        reasons.append("Repeat-request amplification: baseline median %s, blocked median %s"
                       % (base_requests, blocked_attempts))
    base_dom = statistics.median(x["dom_ms"] for x in baselines)
    blocked_dom = statistics.median(x["dom_ms"] for x in blocked)
    if blocked_dom > max(base_dom * 2, base_dom + 2500):
        reasons.append("DOM-load timing warning (highly environment-sensitive): %s -> %s ms"
                       % (base_dom, blocked_dom))
    if reasons:
        return "review-required", reasons
    return "limited-smoke-pass", ["No strong retry/render signal during these limited trials"]

def capture(browser, url, blocked):
    context = browser.new_context(viewport={"width": 1280, "height": 800},
                                  locale="en-US", service_workers="block")
    request_times = []
    intercepted_times = []
    start = time.monotonic()

    def on_request(request):
        if exact_host(request.url) == TARGET:
            request_times.append(round(time.monotonic() - start, 2))
    context.on("request", on_request)

    if blocked:
        def on_route(route):
            if exact_host(route.request.url) == TARGET:
                intercepted_times.append(round(time.monotonic() - start, 2))
                route.abort(error_code="namenotresolved")
            else:
                route.continue_()
        context.route("**/*", on_route)

    page = context.new_page()
    result = {"mode": "blocked" if blocked else "baseline", "http": None,
              "title": False, "body": 0, "links": 0, "requests": 0, "intercepted": 0,
              "first_six_seconds": 0, "later_requests": 0, "dom_ms": None,
              "navigation_error": None}
    try:
        nav_start = time.monotonic()
        response = page.goto(url, wait_until="domcontentloaded", timeout=20000)
        result["dom_ms"] = round((time.monotonic() - nav_start) * 1000)
        result["http"] = response.status if response else None
        page.wait_for_timeout(OBSERVE_MS)
        result["title"] = bool(page.title().strip())
        result["body"] = len(page.locator("body").inner_text(timeout=4000).strip())
        result["links"] = page.locator("a[href]").count()
    except Exception as exc:
        result["navigation_error"] = type(exc).__name__
    result["requests"] = len(request_times)
    result["intercepted"] = len(intercepted_times)
    result["first_six_seconds"] = sum(t < 6 for t in request_times)
    result["later_requests"] = sum(t >= 6 for t in request_times)
    context.close()
    return result

def main():
    chrome = next((shutil.which(x) for x in ("google-chrome", "google-chrome-stable", "chromium")
                   if shutil.which(x)), None)
    if not chrome:
        print("No Chrome available; inconclusive")
        return 2
    from playwright.sync_api import sync_playwright
    reports = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=chrome, headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"])
        for url in SITES:
            # Alternating order reduces cache/order bias; each trial has a fresh context.
            sequence = [False, True, True, False]
            trials = [capture(browser, url, blocked) for blocked in sequence]
            baselines = [x for x in trials if x["mode"] == "baseline"]
            blocked = [x for x in trials if x["mode"] == "blocked"]
            status, reasons = audit_pair(baselines, blocked)
            reports.append({"site": url, "status": status, "reasons": reasons,
                            "trials": trials})
        browser.close()

    report = {"utc": datetime.now(timezone.utc).isoformat(), "host": TARGET,
              "observation_window_ms": OBSERVE_MS, "sites": reports,
              "scope": "Repeated public browser A/B. Exact-host interception emulates name-resolution error; not actual DNS subscription or full merchant usability."}
    os.makedirs("qa-reports", exist_ok=True)
    with open("qa-reports/pinterest-retry-audit.json", "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2)
        out.write("\n")
    lines = ["# Pinterest retry/performance audit", "",
             "Repeated public baseline vs DNS-like exact-host blocking; no full compatibility claim.", ""]
    for site in reports:
        lines.append("## " + site["site"] + " — " + site["status"])
        for trial in site["trials"]:
            lines.append("- " + trial["mode"] + ": HTTP " + str(trial["http"])
                         + "; natural requests " + str(trial["requests"])
                         + "; blocked requests " + str(trial["intercepted"])
                         + "; requests after 6s " + str(trial["later_requests"])
                         + "; DOM load " + str(trial["dom_ms"]) + "ms"
                         + "; readable characters " + str(trial["body"]))
        lines.extend("- " + reason for reason in site["reasons"])
        lines.append("")
    lines.append("Interpretation: retry review flags signal potential overhead, not proven user-facing harm. DOM timing is susceptible to network variance.")
    summary = "\n".join(lines) + "\n"
    print(summary)
    with open("qa-reports/pinterest-retry-audit.md", "w", encoding="utf-8") as out:
        out.write(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as out:
            out.write(summary)
    if any(s["status"] == "review-required" for s in reports):
        return 1  # Keep RC out of green CI when retry amplification remains.
    return 0 if all(s["status"] == "limited-smoke-pass" for s in reports) else 2

if __name__ == "__main__":
    sys.exit(main())
