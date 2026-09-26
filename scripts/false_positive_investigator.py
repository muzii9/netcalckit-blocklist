#!/usr/bin/env python3
"""Bounded read-only, fail-closed investigation of exact DNS tracking hosts.

Never approves, removes, or publishes a rule. Public unauthenticated sites only;
network interception models a DNS failure but does not replace a real-DNS test.
"""
import argparse
import csv
import ipaddress
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT / "tests/false-positive-investigator.json"
CANDIDATES_FILE = ROOT / "candidates/candidates.csv"
RULES_FILE = ROOT / "rules/rules.csv"
REGISTRY_FILE = ROOT / "tests/live-site-cases.json"
HOST_RE = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}")
INCONCLUSIVE = "INCONCLUSIVE"
REVIEW = "REVIEW_REQUIRED"
LIMITED = "LIMITED_SMOKE_PASS"

def host(url):
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""

def public_host(name):
    if not name or not HOST_RE.fullmatch(name) or name.endswith((".local", ".test", ".internal", ".invalid", ".localhost")):
        return False
    try:
        ipaddress.ip_address(name)
        return False
    except ValueError:
        return True

def public_page(url):
    if not isinstance(url, str) or len(url) > 250:
        return False
    try:
        p = urlsplit(url)
        return (p.scheme == "https" and public_host((p.hostname or "").lower())
                and not p.username and not p.password and p.port is None
                and not p.query and not p.fragment)
    except ValueError:
        return False

def approved_hosts(raw):
    return {row["domain"] for row in csv.DictReader(raw.splitlines())
            if row["status"] == "approved" and row["tier"] in {"lite", "standard"}}

def proposed_hosts(base_sha="", rules_path=RULES_FILE):
    if not base_sha:
        return set()
    if not re.fullmatch(r"[a-f0-9]{40,64}", base_sha):
        raise ValueError("Malformed PR base SHA")
    previous = subprocess.run(
        ["git", "show", base_sha + ":rules/rules.csv"], cwd=ROOT,
        text=True, capture_output=True, check=True, timeout=15).stdout
    return approved_hosts(rules_path.read_text(encoding="utf-8")) - approved_hosts(previous)

def validate_config(data):
    if data.get("schema_version") != 1:
        raise ValueError("Expected config schema_version=1")
    max_hosts = data.get("max_hosts_per_run")
    max_pages = data.get("max_seed_pages_per_host")
    seconds = data.get("observe_seconds")
    if type(max_hosts) is not int or not 1 <= max_hosts <= 4:
        raise ValueError("max_hosts_per_run must be 1..4")
    if type(max_pages) is not int or not 1 <= max_pages <= 8:
        raise ValueError("max_seed_pages_per_host must be 1..8")
    if type(seconds) is not int or not 2 <= seconds <= 12:
        raise ValueError("observe_seconds must be 2..12")
    targets = data.get("targets")
    pool = data.get("site_pool")
    if not isinstance(targets, list) or len(targets) > 8 or not isinstance(pool, list) or not 1 <= len(pool) <= 16:
        raise ValueError("Invalid target registry or bounded discovery pool")
    for url in pool:
        if not public_page(url):
            raise ValueError("Unsafe discovery URL")
    seen = set()
    for item in targets:
        h = item.get("host")
        if not isinstance(h, str) or not public_host(h) or h in seen:
            raise ValueError("Invalid or duplicate exact research hostname")
        if item.get("mode") != "research-only":
            raise ValueError("Research pins cannot auto-approve hosts")
        if not isinstance(item.get("vendor"), str) or not item["vendor"].strip():
            raise ValueError("Missing vendor label")
        pages = item.get("pages", [])
        if not isinstance(pages, list) or len(pages) > 4 or not all(public_page(x) for x in pages):
            raise ValueError("Research pins need safe public-page seeds")
        seen.add(h)
    return data

def registry_pages(raw):
    registry = json.loads(raw)
    out = {}
    for entry in registry.get("cases", []):
        if public_host(entry.get("host", "")):
            pages = [p for p in entry.get("pages", []) if public_page(p)]
            out[entry["host"]] = pages[:4]
    return out

def select_targets(config, candidate_csv, case_json, new_hosts, week=None):
    """New proposed rules first; existing research pins; rotating HOLD candidate."""
    if week is None:
        week = datetime.now(timezone.utc).isocalendar().week
    known = {t["host"]: t for t in config["targets"]}
    registry = registry_pages(case_json)
    candidates = {row["domain"]: row for row in csv.DictReader(candidate_csv.splitlines())
                  if row["status"] == "hold" and public_host(row["domain"])}
    selected = []
    def add(h, source, vendor, known_pages):
        if not public_host(h) or any(x["host"] == h for x in selected):
            return
        pool = known_pages + registry.get(h, []) + config["site_pool"]
        pages = list(dict.fromkeys(u for u in pool if public_page(u)))
        selected.append({"host": h, "source": source, "vendor": vendor,
                         "pages": pages[:config["max_seed_pages_per_host"]]})
    for h in sorted(new_hosts):
        pin = known.get(h, {})
        add(h, "NEW_APPROVED_PROPOSAL", pin.get("vendor", candidates.get(h, {}).get("vendor", "Unspecified")),
            pin.get("pages", []))
    for pin in config["targets"]:
        add(pin["host"], "RESEARCH_PIN", pin["vendor"], pin.get("pages", []))
    holds = sorted(set(candidates) - {t["host"] for t in selected})
    if holds:
        pick = holds[week % len(holds)]
        add(pick, "ROTATING_HOLD", candidates[pick]["vendor"], [])
    capacity = config["max_hosts_per_run"]
    omitted = sorted(new_hosts - {x["host"] for x in selected[:capacity]})
    return selected[:capacity], omitted

def classify(baselines, blocked):
    """Conservative repeated evidence classification. Performance flags are review, not proof of harm."""
    if len(baselines) != 2 or len(blocked) != 2:
        return INCONCLUSIVE, ["Two paired baseline/blocked trials are required"]
    if any(x["http"] != 200 or x["body_chars"] < 250 or x["natural_requests"] < 1 for x in baselines):
        return INCONCLUSIVE, ["Host not naturally exercised in both complete public baselines"]
    if any(x["http"] != 200 or x["intercepted"] < 1 or x["body_chars"] < 250 for x in blocked):
        return INCONCLUSIVE, ["Host not intercepted in two complete blocked trials"]
    if any(x["navigation_error"] for x in baselines + blocked):
        return INCONCLUSIVE, ["A browser navigation or rendering error interrupted comparison"]
    b_body = statistics.median(x["body_chars"] for x in baselines)
    f_body = statistics.median(x["body_chars"] for x in blocked)
    b_links = statistics.median(x["links"] for x in baselines)
    f_links = statistics.median(x["links"] for x in blocked)
    b_requests = statistics.median(x["natural_requests"] for x in baselines)
    f_requests = statistics.median(x["intercepted"] for x in blocked)
    b_dom = statistics.median(x["dom_ms"] for x in baselines)
    f_dom = statistics.median(x["dom_ms"] for x in blocked)
    b_js = statistics.median(x["uncaught_js_errors"] for x in baselines)
    f_js = statistics.median(x["uncaught_js_errors"] for x in blocked)
    b_other = statistics.median(x["other_request_failures"] for x in baselines)
    f_other = statistics.median(x["other_request_failures"] for x in blocked)
    reasons = []
    if f_body < 0.7 * b_body or (b_links >= 5 and f_links < 0.7 * b_links):
        reasons.append("Public page body/link presence degraded")
    if any(not x["title_present"] for x in blocked) and all(x["title_present"] for x in baselines):
        reasons.append("Document title lost")
    if b_requests > 0 and f_requests >= 15 and f_requests > 4 * b_requests:
        reasons.append("Failed-request amplification: median %.0f vs %.0f" % (b_requests, f_requests))
    if f_dom > max(2 * b_dom, b_dom + 2500):
        reasons.append("DOM timing regression signal; network conditions may contribute")
    if f_js > b_js + 2:
        reasons.append("New uncaught JavaScript error count increased")
    if f_other > b_other + 4:
        reasons.append("Unrelated network failures increased after blocking")
    return (REVIEW, reasons) if reasons else (LIMITED, ["Limited public-page smoke signals retained; not complete compatibility"])

def capture(browser, url, target, blocked, seconds):
    context = browser.new_context(viewport={"width": 1280, "height": 800},
                                  locale="en-US", service_workers="block")
    target_requests = []
    intercepted = []
    page_errors = []
    other_failures = []
    start = time.monotonic()
    context.on("request", lambda req:
               target_requests.append(round(time.monotonic()-start, 2)) if host(req.url) == target else None)
    def request_failed(req):
        if host(req.url) != target:
            other_failures.append(host(req.url) or "unknown")
    context.on("requestfailed", request_failed)
    def route_request(route):
        h = host(route.request.url)
        if h and not public_host(h):
            route.abort(error_code="blockedbyclient")
        elif blocked and h == target:
            intercepted.append(round(time.monotonic()-start, 2))
            route.abort(error_code="namenotresolved")
        else:
            route.continue_()
    context.route("**/*", route_request)
    page = context.new_page()
    page.on("pageerror", lambda e: page_errors.append(type(e).__name__))
    result = {"mode": "blocked" if blocked else "normal", "http": None,
              "title_present": False, "body_chars": 0, "links": 0,
              "dom_ms": None, "natural_requests": 0, "intercepted": 0,
              "early_target_requests": 0, "uncaught_js_errors": 0,
              "other_request_failures": 0, "navigation_error": ""}
    try:
        begin = time.monotonic()
        response = page.goto(url, wait_until="domcontentloaded", timeout=14000)
        result["dom_ms"] = round((time.monotonic()-begin)*1000)
        result["http"] = response.status if response else None
        # An unexpected external redirect makes the result inconclusive rather than a pass.
        original = host(url).removeprefix("www.")
        final = host(page.url).removeprefix("www.")
        if final != original:
            result["navigation_error"] = "External-or-regional redirect"
        page.wait_for_timeout(seconds * 1000)
        result["title_present"] = bool(page.title().strip())
        result["body_chars"] = len(page.locator("body").inner_text(timeout=3500).strip())
        result["links"] = page.locator("a[href]").count()
    except Exception as exc:
        result["navigation_error"] = type(exc).__name__
    finally:
        result["natural_requests"] = len(target_requests)
        result["intercepted"] = len(intercepted)
        result["early_target_requests"] = sum(t < 6 for t in target_requests)
        result["uncaught_js_errors"] = len(page_errors)
        result["other_request_failures"] = len(other_failures)
        context.close()
    return result

def run_site(browser, host_name, url, seconds):
    # Alternating order and clean contexts: B -> F -> F -> B.
    trials = [capture(browser, url, host_name, mode, seconds)
              for mode in (False, True, True, False)]
    baselines = [x for x in trials if x["mode"] == "normal"]
    blocked = [x for x in trials if x["mode"] == "blocked"]
    status, reasons = classify(baselines, blocked)
    return {"url": url, "status": status, "reasons": reasons, "trials": trials}

def report_text(report):
    lines = ["# Automated false-positive investigation", "",
             "Result meanings: REVIEW_REQUIRED is a risk signal, INCONCLUSIVE is never clearance, "
             "LIMITED_SMOKE_PASS is not universal compatibility.", "",
             "Run: " + report["utc"], "Mode: " + report["mode"], ""]
    for candidate in report["targets"]:
        lines.append("## " + candidate["host"] + " — " + candidate["status"]
                     + " (" + candidate["source"] + ")")
        lines.append("Public pages probed: " + str(len(candidate["probed"]))
                     + "; naturally exercising pages tested: " + str(len(candidate["sites"])))
        for site in candidate["sites"]:
            b = [x for x in site["trials"] if x["mode"] == "normal"]
            f = [x for x in site["trials"] if x["mode"] == "blocked"]
            lines.append("- " + site["url"] + ": " + site["status"]
                         + "; normal requests=" + ",".join(str(x["natural_requests"]) for x in b)
                         + "; failed-target requests=" + ",".join(str(x["intercepted"]) for x in f)
                         + "; DOM milliseconds normal=" + ",".join(str(x["dom_ms"]) for x in b)
                         + ", blocked=" + ",".join(str(x["dom_ms"]) for x in f))
            lines.extend("  - " + reason for reason in site["reasons"])
        lines.extend("- " + issue for issue in candidate["reasons"])
        lines.append("")
    if report["omitted_new_rules"]:
        lines.append("UNTESTED NEW APPROVED RULES: " + ", ".join(report["omitted_new_rules"]))
    lines.append("No rules or candidate statuses were changed. Unexercised hosts and bot-protected sites remain INCONCLUSIVE.")
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-new", action="store_true",
                        help="Fail CI when any newly approved Standard rule lacks limited smoke evidence")
    parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "qa-reports")
    args = parser.parse_args()
    config = validate_config(json.loads(args.config.read_text(encoding="utf-8")))
    new = proposed_hosts(os.environ.get("FP_BASE_SHA", ""))
    candidate_raw = CANDIDATES_FILE.read_text(encoding="utf-8")
    case_raw = REGISTRY_FILE.read_text(encoding="utf-8")
    targets, omitted = select_targets(config, candidate_raw, case_raw, new)
    chrome = next((shutil.which(x) for x in ("google-chrome", "google-chrome-stable", "chromium")
                   if shutil.which(x)), None)
    if not chrome:
        print("Chrome not installed; no investigation can be inferred", file=sys.stderr)
        return 3
    from playwright.sync_api import sync_playwright
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=chrome, headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"])
        for candidate in targets:
            url_hits, checked, sites = [], [], []
            # No fabricated tracker requests. Every hit must occur on a real third-party public page.
            for url in candidate["pages"]:
                probe = capture(browser, url, candidate["host"], False, config["observe_seconds"])
                checked.append({"url": url, "http": probe["http"],
                                "target_requests": probe["natural_requests"],
                                "content_present": probe["body_chars"] >= 250,
                                "reason": probe["navigation_error"]})
                if (probe["http"] == 200 and probe["body_chars"] >= 250
                        and probe["natural_requests"] > 0 and not probe["navigation_error"]):
                    url_hits.append(url)
                if len(url_hits) >= 2:
                    break
            for url in url_hits:
                sites.append(run_site(browser, candidate["host"], url, config["observe_seconds"]))
            statuses = {s["status"] for s in sites}
            status = (REVIEW if REVIEW in statuses else
                      INCONCLUSIVE if not sites or INCONCLUSIVE in statuses else LIMITED)
            reasons = (["No natural public-page exercise found in bounded seed pool"] if not sites else
                       ["Review any flagged site before publication"] if status == REVIEW else
                       ["One or more repeated tests incomplete"] if status == INCONCLUSIVE else
                       ["Only limited public-page checks passed"])
            results.append({**{k:candidate[k] for k in ("host","vendor","source")},
                            "status":status,"reasons":reasons,"probed":checked,"sites":sites})
        browser.close()
    report={"utc":datetime.now(timezone.utc).isoformat(),
            "mode":"strict-new" if args.strict_new else "report-only",
            "new_approved_rules":sorted(new),"omitted_new_rules":omitted,
            "targets":results,
            "limitations":"Public read-only A/B only; no authentication, forms, checkout, private user data, real DNS subscription or CPU/battery validation."}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"false-positive-investigation.json").write_text(
        json.dumps(report,indent=2)+"\n",encoding="utf-8")
    markdown=report_text(report)
    (args.output_dir/"false-positive-investigation.md").write_text(markdown,encoding="utf-8")
    print(markdown,flush=True)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as f:
            f.write(markdown)
    for x in results:
        if x["status"] != LIMITED:
            print("::warning::"+x["host"]+": "+x["status"]+" (not approved)",flush=True)
    if args.strict_new:
        by_host={r["host"]:r["status"] for r in results}
        unsafe=sorted(h for h in new if by_host.get(h) != LIMITED)
        if unsafe or omitted:
            print("::error::New Standard rule(s) lack limited public-site clearance: "
                  +", ".join(sorted(set(unsafe)|set(omitted))),flush=True)
            return 2
    return 0  # Report-only mode may report REVIEW REQUIRED without implying clearance.

if __name__ == "__main__":
    sys.exit(main())
