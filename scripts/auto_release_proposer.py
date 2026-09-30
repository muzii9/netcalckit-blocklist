#!/usr/bin/env python3
"""Prepare a conservative DRAFT Standard RC from a researched candidate.

This script never talks to GitHub and never merges/publishes anything. It can:
1) choose one research-stage candidate for bounded compatibility investigation;
2) create a one-host investigator config; and
3) after a strong LIMITED_SMOKE_PASS on >=2 independent public sites, stage the
   repository changes that a GitHub Actions workflow may place in a DRAFT PR.

Human review and an explicit merge remain mandatory.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from candidate_db import Candidate, load_candidates

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "candidates" / "candidates.csv"
RULES = ROOT / "rules" / "rules.csv"
ALLOWLIST = ROOT / "allowlists" / "allowlist.txt"
FP_CONFIG = ROOT / "tests" / "false-positive-investigator.json"
LIVE_CASES = ROOT / "tests" / "live-site-cases.json"
README = ROOT / "README.md"

PRIMARY_EVIDENCE = {"vendor-doc", "vendor-code", "first-party-config"}
AUTO_STATUSES = {"new", "research", "review"}
BAD_CATEGORY_TOKENS = {
    "auth", "login", "payment", "billing", "security", "update", "cdn",
    "sdk", "feature_flag", "experimentation", "essential", "download",
}
GOOD_CATEGORY_TOKENS = {
    "analytics", "telemetry", "tracking", "measurement", "observability",
    "session_replay", "advertising", "conversion", "product_analytics",
    "behavioral_analytics", "web_analytics", "ad_", "audience",
}
NOTE_RISK = re.compile(
    r"\b(auth|login|payment|checkout|billing|security|update|mixed[- ]purpose|"
    r"shared host|shared infrastructure|sdk delivery|javascript/css|guide metadata|"
    r"in-app guide|admin tooling|feature flag|experimentation)\b",
    re.I,
)
HOST_RE = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}")


def read_rules(path: Path = RULES) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_allowlist(path: Path = ALLOWLIST) -> set[str]:
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def candidate_gate(candidate: Candidate) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if candidate.status not in AUTO_STATUSES:
        reasons.append("status is an explicit hold/reject or outside automatic research flow")
    if candidate.evidence_type not in PRIMARY_EVIDENCE:
        reasons.append("evidence is not primary enough for an automatic draft proposal")
    if candidate.dedicated_service == "no":
        reasons.append("service is explicitly not dedicated")
    if candidate.shared_infrastructure == "yes":
        reasons.append("shared infrastructure is explicitly confirmed")
    if candidate.essential_function == "yes":
        reasons.append("essential functionality is explicitly confirmed")
    if candidate.false_positive_risk == "high":
        reasons.append("false-positive risk is high")
    if candidate.domain.count(".") < 2:
        reasons.append("broad/apex-style hostname is excluded from automatic RC proposals")
    category = candidate.category.lower()
    if any(token in category for token in BAD_CATEGORY_TOKENS):
        reasons.append("category contains a mixed/essential delivery risk token")
    if not any(token in category for token in GOOD_CATEGORY_TOKENS):
        reasons.append("category is not narrowly recognized as measurement/telemetry")
    if NOTE_RISK.search(candidate.notes):
        reasons.append("research notes contain a mixed-use/essential-function warning")
    return not reasons, reasons


def priority(candidate: Candidate) -> tuple:
    status_rank = {"review": 0, "research": 1, "new": 2}
    evidence_rank = {"vendor-doc": 0, "vendor-code": 0, "first-party-config": 1}
    risk_rank = {"low": 0, "low-moderate": 1, "moderate": 2, "unknown": 3}
    known_safety = sum(
        (
            candidate.dedicated_service == "yes",
            candidate.shared_infrastructure == "no",
            candidate.essential_function == "no",
        )
    )
    return (
        status_rank.get(candidate.status, 9),
        evidence_rank.get(candidate.evidence_type, 9),
        risk_rank.get(candidate.false_positive_risk, 9),
        -known_safety,
        candidate.domain,
    )


def select_candidate(candidates, rules, allowlisted):
    existing = {row["domain"] for row in rules}
    eligible = []
    audit = []
    for candidate in candidates:
        allowed, reasons = candidate_gate(candidate)
        reasons = list(reasons)
        if candidate.domain in existing:
            reasons.append("already present in rule database")
        if candidate.domain in allowlisted:
            reasons.append("explicitly allowlisted")
        eligible_flag = allowed and not reasons
        if eligible_flag:
            eligible.append(candidate)
        audit.append(
            {
                "domain": candidate.domain,
                "status": candidate.status,
                "eligible_for_public_investigation": eligible_flag,
                "reasons": reasons,
            }
        )
    eligible.sort(key=priority)
    return (eligible[0] if eligible else None), audit


def safe_public_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").lower()
        return bool(
            parsed.scheme == "https"
            and HOST_RE.fullmatch(hostname)
            and not parsed.username
            and not parsed.password
            and parsed.port is None
            and not parsed.query
            and not parsed.fragment
            and not hostname.endswith((".local", ".internal", ".test", ".invalid", ".localhost"))
        )
    except ValueError:
        return False


def known_pages_for(host: str, config: dict, live_cases: dict) -> list[str]:
    pages = []
    for target in config.get("targets", []):
        if target.get("host") == host:
            pages.extend(target.get("pages", []))
    for case in live_cases.get("cases", []):
        if case.get("host") == host:
            pages.extend(case.get("pages", []))
    return list(dict.fromkeys(url for url in pages if safe_public_url(url)))


def make_investigator_config(candidate: Candidate, base_config: dict, live_cases: dict) -> dict:
    pool = [url for url in base_config.get("site_pool", []) if safe_public_url(url)]
    pages = known_pages_for(candidate.domain, base_config, live_cases)
    return {
        "schema_version": 1,
        "description": "One-host automatic RC investigation. Report only; never publishes.",
        "max_hosts_per_run": 1,
        "max_seed_pages_per_host": min(8, max(1, int(base_config.get("max_seed_pages_per_host", 6)))),
        "observe_seconds": min(12, max(4, int(base_config.get("observe_seconds", 7)))),
        "targets": [
            {
                "host": candidate.domain,
                "vendor": candidate.vendor,
                "mode": "research-only",
                "pages": pages[:4],
            }
        ],
        "site_pool": pool,
    }


def report_decision(host: str, report: dict, minimum_sites: int = 2) -> dict:
    target = next((item for item in report.get("targets", []) if item.get("host") == host), None)
    if not target:
        return {"ready": False, "host": host, "reason": "host missing from investigator report", "sites": []}
    sites = [
        site for site in target.get("sites", [])
        if site.get("status") == "LIMITED_SMOKE_PASS" and safe_public_url(site.get("url", ""))
    ]
    unique = list(dict.fromkeys(site["url"] for site in sites))
    if target.get("status") != "LIMITED_SMOKE_PASS":
        return {
            "ready": False,
            "host": host,
            "reason": "investigator status is " + str(target.get("status")),
            "sites": unique,
        }
    if len(unique) < minimum_sites:
        return {
            "ready": False,
            "host": host,
            "reason": f"need {minimum_sites} independent public sites; found {len(unique)}",
            "sites": unique,
        }
    return {
        "ready": True,
        "host": host,
        "reason": "limited repeated public-site evidence met automatic draft-RC threshold",
        "sites": unique[:5],
    }


def release_risk(candidate: Candidate) -> str:
    if candidate.false_positive_risk in {"low", "low-moderate", "moderate"}:
        return candidate.false_positive_risk
    return "moderate"


def slug(host: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")


def evidence_markdown(candidate: Candidate, decision: dict, report: dict) -> str:
    target = next(item for item in report["targets"] if item.get("host") == candidate.domain)
    lines = [
        f"# Automated Standard RC proposal — {candidate.domain}",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "**Status: unmerged DRAFT proposal. Human review and explicit merge approval are mandatory.**",
        "This document does not claim universal compatibility and does not authorize automatic publication.",
        "",
        "## Candidate evidence",
        "",
        f"- Vendor: {candidate.vendor}",
        f"- Category: {candidate.category}",
        f"- Primary evidence: {candidate.evidence_url}",
        f"- Evidence type: {candidate.evidence_type}",
        f"- Candidate metadata: dedicated_service={candidate.dedicated_service}, "
        f"shared_infrastructure={candidate.shared_infrastructure}, "
        f"essential_function={candidate.essential_function}, "
        f"false_positive_risk={candidate.false_positive_risk}",
        f"- Original research note: {candidate.notes}",
        "",
        "## Automated false-positive investigation",
        "",
        f"- Result: {target.get('status')}",
        f"- Public sites meeting repeated limited-smoke threshold: {len(decision['sites'])}",
    ]
    for site in target.get("sites", []):
        if site.get("url") not in decision["sites"]:
            continue
        baseline = [trial for trial in site.get("trials", []) if trial.get("mode") == "normal"]
        blocked = [trial for trial in site.get("trials", []) if trial.get("mode") == "blocked"]
        lines.extend(
            [
                f"- {site['url']}",
                "  - normal exact-host requests: " + ", ".join(
                    str(x.get("natural_requests")) for x in baseline
                ),
                "  - blocked/intercepted exact-host requests: " + ", ".join(
                    str(x.get("intercepted")) for x in blocked
                ),
                "  - DOM-loaded milliseconds normal: " + ", ".join(
                    str(x.get("dom_ms")) for x in baseline
                ),
                "  - DOM-loaded milliseconds blocked: " + ", ".join(
                    str(x.get("dom_ms")) for x in blocked
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Limitations and merge gate",
            "",
            "- Browser interception models a DNS-like failure; it is not a complete real-device DNS-provider test.",
            "- Public unauthenticated pages cannot prove login, checkout, private app, media, battery, CPU, or universal compatibility.",
            "- LIMITED_SMOKE_PASS only means bounded automated signals stayed within conservative thresholds on the listed pages.",
            "- Full repository CI, isolated AdGuard enforcement, the live-site registry gate, and maintainer review must pass on the generated RC branch.",
            "- Do not auto-merge. If any later workflow becomes inconclusive or review-required, leave the proposal unmerged.",
            "",
        ]
    )
    return "\n".join(lines)


def write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def apply_proposal(candidate, report, decision, candidates_path=CANDIDATES, rules_path=RULES,
                   live_cases_path=LIVE_CASES, readme_path=README, root=ROOT):
    if not decision.get("ready"):
        return {"changed": False, **decision}
    current_candidates = load_candidates(candidates_path)
    current = next((item for item in current_candidates if item.domain == candidate.domain), None)
    if current is None:
        raise ValueError("candidate disappeared before proposal application")
    allowed, reasons = candidate_gate(current)
    if not allowed:
        raise ValueError("candidate no longer eligible: " + "; ".join(reasons))

    with rules_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rule_fields = list(reader.fieldnames or [])
        rules = list(reader)
    if any(row["domain"] == candidate.domain for row in rules):
        raise ValueError("candidate already exists in rule database")

    evidence_rel = f"evidence/auto-rc-{slug(candidate.domain)}.md"
    evidence_path = root / evidence_rel
    if evidence_path.exists():
        raise ValueError("automatic evidence file already exists")

    rules.append(
        {
            "domain": candidate.domain,
            "vendor": candidate.vendor,
            "category": candidate.category,
            "evidence_file": evidence_rel,
            "false_positive_risk": release_risk(candidate),
            "tier": "standard",
            "status": "approved",
            "last_reviewed": date.today().isoformat(),
        }
    )
    rules.sort(key=lambda row: row["domain"])
    write_csv(rules_path, rule_fields, rules)

    with candidates_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        candidate_fields = list(reader.fieldnames or [])
        candidate_rows = [row for row in reader if row["domain"] != candidate.domain]
    candidate_rows.sort(key=lambda row: row["domain"])
    write_csv(candidates_path, candidate_fields, candidate_rows)

    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(evidence_markdown(candidate, decision, report), encoding="utf-8")

    cases = json.loads(live_cases_path.read_text(encoding="utf-8"))
    if any(case.get("host") == candidate.domain for case in cases.get("cases", [])):
        raise ValueError("live-site case already exists for candidate")
    cases["cases"].append(
        {
            "vendor": candidate.vendor,
            "host": candidate.domain,
            "wait_seconds": 7,
            "pages": decision["sites"][:5],
        }
    )
    live_cases_path.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    approved_standard = sum(
        row["status"] == "approved" and row["tier"] in {"lite", "standard"}
        for row in rules
    )
    tick = chr(96)
    needle = "The current " + tick + "main" + tick + " list contains "
    text_value = readme_path.read_text(encoding="utf-8")
    if text_value.count(needle) != 1:
        raise ValueError("README current main-rule count sentence was not found exactly once")
    text_value = re.sub(
        re.escape(needle) + r"\d+(?= analytics, telemetry, advertising-measurement, and observability hostnames\.)",
        needle + str(approved_standard),
        text_value,
        count=1,
    )
    readme_path.write_text(text_value, encoding="utf-8")

    return {
        "changed": True,
        "host": candidate.domain,
        "evidence_file": evidence_rel,
        "sites": decision["sites"],
        "proposed_standard_count": approved_standard,
        "rule_risk": release_risk(candidate),
    }


def find_candidate(host: str, candidates):
    item = next((candidate for candidate in candidates if candidate.domain == host), None)
    if item is None:
        raise ValueError("candidate not found: " + host)
    return item


def dump(path, value: dict) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    select = sub.add_parser("select")
    select.add_argument("--output", type=Path)

    config = sub.add_parser("config")
    config.add_argument("--host", required=True)
    config.add_argument("--output", type=Path, required=True)

    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--host", required=True)
    apply_cmd.add_argument("--report", type=Path, required=True)
    apply_cmd.add_argument("--decision-output", type=Path)

    args = parser.parse_args()
    candidates = load_candidates(CANDIDATES)

    if args.command == "select":
        chosen, audit = select_candidate(candidates, read_rules(), read_allowlist())
        payload = {
            "date": date.today().isoformat(),
            "selected": asdict(chosen) if chosen else None,
            "audit": audit,
            "policy": "One conservative research candidate per run; explicit HOLD/rejected rows are never auto-proposed.",
        }
        dump(args.output, payload)
        print(chosen.domain if chosen else "")
        return 0

    candidate = find_candidate(args.host, candidates)

    if args.command == "config":
        base = json.loads(FP_CONFIG.read_text(encoding="utf-8"))
        cases = json.loads(LIVE_CASES.read_text(encoding="utf-8"))
        payload = make_investigator_config(candidate, base, cases)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(args.output)
        return 0

    report = json.loads(args.report.read_text(encoding="utf-8"))
    decision = report_decision(candidate.domain, report)
    if not decision["ready"]:
        dump(args.decision_output, {"changed": False, **decision})
        print("NOT_READY: " + decision["reason"])
        return 0
    result = apply_proposal(candidate, report, decision)
    dump(args.decision_output, result)
    print("PROPOSAL_READY: " + candidate.domain)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
