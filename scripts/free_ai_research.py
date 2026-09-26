#!/usr/bin/env python3
"""Optional zero-paid-tier AI research report. Never modifies candidate/rule databases."""
import json
import csv
import hashlib
import re
import os
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/ai-research-report.json"
REGISTRY = ROOT / "research/vendor-registry.json"
QUEUE = ROOT / "candidates/candidates.csv"
RULES = ROOT / "rules/rules.csv"
MAX_SEARCHES = 8
HOST = re.compile(r"(?<![\\w.-])(?:[a-z0-9-]+\\.)+[a-z]{2,}(?![\\w.-])", re.I)

def known_hosts():
    known = set()
    for path in (QUEUE, RULES):
        with path.open(newline="", encoding="utf-8") as stream:
            known.update(row["domain"].lower() for row in csv.DictReader(stream))
    return known

def exact_excerpt_host(host, hits):
    return any(host in set(HOST.findall(hit["content_excerpt"].lower())) for hit in hits)


def post(url, payload, headers):
    data = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(request, timeout=35) as response:
        return json.load(response)

def main():
    gemini = os.environ.get("GEMINI_API_KEY")
    tavily = os.environ.get("TAVILY_API_KEY")
    if not gemini or not tavily:
        print("Gemini/Tavily secrets unavailable; skipping optional AI research.")
        return 0
    sources = json.loads(REGISTRY.read_text())["sources"]
    findings, errors = [], []
    known = known_hosts()
    if not sources:
        print("No registered vendors; skipping optional AI research.")
        return 0
    # One query per registered vendor, up to eight per day. Report-only.
    queries = [
        "official collection ingest hostname documentation",
        "tracking endpoint domain SDK configuration official",
        "analytics API endpoint domain official docs",
        "data collection domains network allowlist documentation",
        "event capture endpoint hostname configuration",
        "regional ingestion hosts official documentation",
        "telemetry endpoint network firewall allowlist",
        "session recording collection hostname docs",
    ]
    day = date.today().toordinal()
    ordered = sorted(sources, key=lambda source: hashlib.sha256(
        (str(day) + source["vendor"]).encode()).hexdigest())
    for index, source in enumerate(ordered[:MAX_SEARCHES]):
        query = queries[(day + index) % len(queries)]
        try:
            search = post("https://api.tavily.com/search",
                {"api_key": tavily, "query": source["vendor"] + " " + query,
                 "search_depth": "basic", "max_results": 3, "include_answer": False},
                {})
            hits = [{"url": h.get("url", ""), "title": h.get("title", ""),
                     "content_excerpt": h.get("content", "")[:700]}
                    for h in search.get("results", [])[:3]]
            # One Gemini analysis per successful search; AI results remain report-only.
            # Gemini response is untrusted research commentary; never promoted automatically.
            prompt = ("You are a conservative DNS blocklist research assistant. Analyze these search excerpts. "
                "Return concise JSON with keys vendor, candidate_hosts (array of {hostname, source_url, "
                "purpose, false_positive_concerns}), and unresolved_questions. Do not invent hosts or citations. "
                "If evidence is weak return an empty array. Treat login, CDN, SDK delivery, feature flags, "
                "experimentation, security and mixed-purpose services as risky. Every result remains HOLD. "
                "Only suggest exact hostnames that appear literally in the supplied search excerpts. "
                "Vendor: " + source["vendor"] + ". Excerpts: " + json.dumps(hits))
            response = post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent",
                {"contents": [{"parts": [{"text": prompt}]}],
                 "generationConfig": {"temperature": 0, "responseMimeType": "application/json", "maxOutputTokens": 1200}},
                {"x-goog-api-key": gemini})
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            analysis = json.loads(text)
            # Deterministic checks: only literal excerpt hosts, suffix-matched; report only.
            safe = []
            for item in analysis.get("candidate_hosts", []):
                host = str(item.get("hostname", "")).lower().strip()
                if (host and host not in known and exact_excerpt_host(host, hits) and
                    any(host.endswith("." + suffix) for suffix in source["allowed_suffixes"])):
                    safe.append({**item, "hostname": host, "status": "hold_unverified"})
            findings.append({"vendor": source["vendor"], "query": query, "search_hits": hits,
                             "ai_suggestions": safe[:10],
                             "unresolved_questions": analysis.get("unresolved_questions", [])})
        except Exception as exc:
            errors.append({"vendor": source["vendor"], "query": query, "error_type": type(exc).__name__})
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"date": date.today().isoformat(), "findings": findings,
        "errors": errors, "disclaimer": "AI suggestions are unverified and never automatically blocklisted."},
        indent=2) + "\n")
    print("AI research completed:", len(findings), "queries;", len(errors), "errors; cap", MAX_SEARCHES, "daily.")
    return 0 if findings else 1

if __name__ == "__main__":
    raise SystemExit(main())
