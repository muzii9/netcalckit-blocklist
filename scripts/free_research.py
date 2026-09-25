#!/usr/bin/env python3
"""Conservative, no-paid-API vendor documentation discovery. All discoveries are HOLD."""
import csv
import html
import json
import re
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/vendor-registry.json"
QUEUE = ROOT / "candidates/candidates.csv"
RULES = ROOT / "rules/rules.csv"
ALLOW = ROOT / "allowlists/allowlist.txt"
OUT = ROOT / "research/discoveries.json"
HOST = re.compile(r"(?<![\w.-])(?:[a-z0-9-]+\.)+[a-z]{2,}(?![\w.-])", re.I)
SKIP = re.compile(r"(^|[.-])(auth|login|account|payment|billing|update|security|recovery|cdn|static|dashboard|api-gateway)([.-]|$)", re.I)
MAX_NEW = 30

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))["sources"]
    candidates = read_csv(QUEUE)
    known = {r["domain"] for r in candidates} | {r["domain"] for r in read_csv(RULES)}
    known |= {s.strip().lstrip("#").strip() for s in ALLOW.read_text().splitlines() if s.strip() and not s.startswith("#")}
    added, errors = [], []
    for source in registry:
        if len(added) >= MAX_NEW:
            break
        url = source["url"]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NetCalcKit-research/1.0 (documentation audit)"})
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status != 200 or "text/html" not in response.headers.get("Content-Type", ""):
                    raise ValueError("Unexpected documentation response")
                page = response.read(2_000_000).decode("utf-8", errors="replace")
            # Hostnames in script/style/HTML markup alone are not adequate evidence.
            page = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", page, flags=re.I | re.S)
            page = html.unescape(re.sub(r"<[^>]+>", " ", page))
            page = re.sub(r"\s+", " ", page)
        except Exception as exc:
            errors.append({"source": url, "error": str(exc)[:160]})
            continue
        for match in HOST.finditer(page):
            host = match.group().lower().rstrip(".")
            suffixes = source["allowed_suffixes"]
            if not any(host.endswith("." + suffix) for suffix in suffixes):
                continue  # no broad apex; only explicit vendor suffixes
            if host in known or SKIP.search(host) or host.startswith("www."):
                continue
            # Require literal appearance in rendered documentation text; still NOT approval.
            row = dict.fromkeys(candidates[0].keys() if candidates else [
                "domain","vendor","category","evidence_url","evidence_type",
                "dedicated_service","shared_infrastructure","essential_function",
                "false_positive_risk","status","observed_date","notes"], "")
            row.update(domain=host, vendor=source["vendor"], category=source["category"],
                evidence_url=url, evidence_type="vendor-doc", dedicated_service="unknown",
                shared_infrastructure="unknown", essential_function="unknown",
                false_positive_risk="unknown", status="hold",
                observed_date=date.today().isoformat(),
                notes="Automated documentation-text discovery only; HOLD until human confirms endpoint purpose and false-positive safety")
            candidates.append(row)
            known.add(host)
            added.append({"hostname": host, "vendor": source["vendor"], "evidence_url": url})
            if len(added) >= MAX_NEW:
                break
    if added:
        candidates.sort(key=lambda r: r["domain"])
        with QUEUE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(candidates[0]))
            writer.writeheader()
            writer.writerows(candidates)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"date": date.today().isoformat(), "new": added, "source_errors": errors}, indent=2) + "\n")
    print(f"New HOLD candidates: {len(added)}; source errors: {len(errors)}")
    if errors:
        print("Source errors:", json.dumps(errors))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
