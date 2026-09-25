#!/usr/bin/env python3
"""Optional zero-paid-tier AI research report. Never modifies candidate/rule databases."""
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/ai-research-report.json"
REGISTRY = ROOT / "research/vendor-registry.json"

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
    # 24 basic searches/day = at most 744 credits in a 31-day month.
    # Reserve at least 256 of the 1,000 free monthly credits.
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
    for index in range(24):
        source = sources[index % len(sources)]
        query = queries[(index // len(sources)) % len(queries)]
        try:
            search = post("https://api.tavily.com/search",
                {"api_key": tavily, "query": source["vendor"] + " " + query,
                 "search_depth": "basic", "max_results": 3, "include_answer": False},
                {})
            hits = [{"url": h.get("url", ""), "title": h.get("title", ""),
                     "content_excerpt": h.get("content", "")[:700]}
                    for h in search.get("results", [])[:3]]
            # Analyze every fourth search (six Gemini requests/day).
            if index % 4 != 0:
                findings.append({"vendor": source["vendor"], "query": query,
                                 "search_hits": hits, "ai_suggestions": [],
                                 "unresolved_questions": ["Not AI-reviewed; human verification required"]})
                continue
            # Gemini response is untrusted research commentary; never promoted automatically.
            prompt = ("You are a conservative DNS blocklist research assistant. Analyze these search excerpts. "
                "Return concise JSON with keys vendor, candidate_hosts (array of {hostname, source_url, "
                "purpose, false_positive_concerns}), and unresolved_questions. Do not invent hosts or citations. "
                "If evidence is weak return an empty array. Treat login, CDN, SDK delivery, feature flags, "
                "experimentation, security and mixed-purpose services as risky. Every result remains HOLD. "
                "Only suggest exact hostnames that appear literally in the supplied search excerpts. "
                "Vendor: " + source["vendor"] + ". Excerpts: " + json.dumps(hits))
            response = post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent",
                {"contents": [{"parts": [{"text": prompt}]}],
                 "generationConfig": {"temperature": 0, "responseMimeType": "application/json", "maxOutputTokens": 1200}},
                {"x-goog-api-key": gemini})
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            analysis = json.loads(text)
            # Deterministic checks: only literal excerpt hosts, suffix-matched; report only.
            corpus = " ".join(h["content_excerpt"] for h in hits).lower()
            safe = []
            for item in analysis.get("candidate_hosts", []):
                host = str(item.get("hostname", "")).lower().strip()
                if (host and host in corpus and
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
    print("AI research completed:", len(findings), "vendors;", len(errors), "errors.")
    return 0 if findings else 1

if __name__ == "__main__":
    raise SystemExit(main())
