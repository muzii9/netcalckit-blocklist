#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NetCalcKit contributors
# Run an isolated, disposable AdGuard Home enforcement lab for the checked-out Standard list.

set -Eeuo pipefail

ADGUARD_IMAGE="${ADGUARD_IMAGE:-adguard/adguardhome:v0.107.79}"
DNS_PORT="${DNS_PORT:-53535}"
WEB_PORT="${WEB_PORT:-58080}"
SETUP_PORT="${SETUP_PORT:-53000}"
SOURCE_PORT="${SOURCE_PORT:-58081}"
CONTROL_DOMAIN="${CONTROL_DOMAIN:-example.com}"
REPORT="${REPORT:-$PWD/netcalckit-adguard-lab-report.txt}"
LAB_LOG="${LAB_LOG:-$PWD/netcalckit-adguard-container.log}"

for command_name in docker curl dig python3 grep awk; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "ERROR: required command not found: $command_name" >&2
        exit 4
    fi
done

if [[ ! -f blocklists/standard.txt ]]; then
    echo "ERROR: run this script from the repository root." >&2
    exit 4
fi

expected_rules="$(grep -Ev '^[[:space:]]*(#|$)' blocklists/standard.txt | wc -l | tr -d ' ')"
lab_dir="$(mktemp -d)"
container="netcalckit-adguard-lab-$RANDOM-$$"
http_pid=""

cleanup() {
    set +e
    if [[ -n "$http_pid" ]]; then
        kill "$http_pid" >/dev/null 2>&1 || true
        wait "$http_pid" >/dev/null 2>&1 || true
    fi
    if docker inspect "$container" >/dev/null 2>&1; then
        docker logs "$container" >"$LAB_LOG" 2>&1 || true
    fi
    docker rm -f "$container" >/dev/null 2>&1 || true
    rm -rf "$lab_dir"
}
trap cleanup EXIT INT TERM

mkdir -p "$lab_dir/work" "$lab_dir/conf"

python3 -m http.server "$SOURCE_PORT" --bind 0.0.0.0 --directory "$PWD"     >"$lab_dir/source-http.log" 2>&1 &
http_pid=$!

for _ in {1..30}; do
    if curl -fsS "http://127.0.0.1:$SOURCE_PORT/blocklists/standard.txt" >/dev/null; then
        break
    fi
    sleep 0.2
done

curl -fsS "http://127.0.0.1:$SOURCE_PORT/blocklists/standard.txt" >/dev/null

docker run -d --name "$container"     --add-host=host.docker.internal:host-gateway     -p "127.0.0.1:$SETUP_PORT:3000/tcp"     -p "127.0.0.1:$WEB_PORT:80/tcp"     -p "127.0.0.1:$DNS_PORT:53/tcp"     -p "127.0.0.1:$DNS_PORT:53/udp"     -v "$lab_dir/work:/opt/adguardhome/work"     -v "$lab_dir/conf:/opt/adguardhome/conf"     "$ADGUARD_IMAGE" >/dev/null

for _ in {1..60}; do
    if curl -fsS "http://127.0.0.1:$SETUP_PORT/control/install/get_addresses" >/dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

curl -fsS "http://127.0.0.1:$SETUP_PORT/control/install/get_addresses" >/dev/null

curl -fsS -X POST     -H 'Content-Type: application/json'     --data '{"web":{"ip":"0.0.0.0","port":80},"dns":{"ip":"0.0.0.0","port":53},"username":"ci","password":"netcalckit-ci-only","language":"en"}'     "http://127.0.0.1:$SETUP_PORT/control/install/configure" >/dev/null

for _ in {1..60}; do
    if curl -fsS -u 'ci:netcalckit-ci-only' "http://127.0.0.1:$WEB_PORT/control/status" >/dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

curl -fsS -u 'ci:netcalckit-ci-only' "http://127.0.0.1:$WEB_PORT/control/status" >/dev/null

curl -fsS -u 'ci:netcalckit-ci-only' -X POST     -H 'Content-Type: application/json'     --data '{"blocking_mode":"null_ip","protection_enabled":true}'     "http://127.0.0.1:$WEB_PORT/control/dns_config" >/dev/null

filter_url="http://host.docker.internal:$SOURCE_PORT/blocklists/standard.txt"

curl -fsS -u 'ci:netcalckit-ci-only' -X POST     -H 'Content-Type: application/json'     --data "{"name":"NetCalcKit Standard RC","url":"$filter_url","whitelist":false}"     "http://127.0.0.1:$WEB_PORT/control/filtering/add_url" >/dev/null

curl -fsS -u 'ci:netcalckit-ci-only' -X POST     -H 'Content-Type: application/json'     --data '{"enabled":true,"interval":24}'     "http://127.0.0.1:$WEB_PORT/control/filtering/config" >/dev/null

curl -fsS -u 'ci:netcalckit-ci-only' -X POST     -H 'Content-Type: application/json'     --data '{"whitelist":false,"force":true}'     "http://127.0.0.1:$WEB_PORT/control/filtering/refresh" >/dev/null

status_json="$(curl -fsS -u 'ci:netcalckit-ci-only' "http://127.0.0.1:$WEB_PORT/control/filtering/status")"
loaded_rules="$(STATUS_JSON="$status_json" python3 - <<'PY'
import json
import os

data = json.loads(os.environ["STATUS_JSON"])
filters = data.get("filters", [])
for item in filters:
    if item.get("name") == "NetCalcKit Standard RC":
        print(item.get("rules_count", 0))
        break
else:
    print(0)
PY
)"

echo "AdGuard lab image : $ADGUARD_IMAGE"
echo "Expected rules    : $expected_rules"
echo "Loaded rules      : $loaded_rules"

if [[ "$loaded_rules" != "$expected_rules" ]]; then
    echo "ERROR: AdGuard loaded $loaded_rules rules; expected $expected_rules." >&2
    docker logs "$container" >&2 || true
    exit 5
fi

LIST_URL="http://127.0.0.1:$SOURCE_PORT/blocklists/standard.txt" DNS_SERVER=127.0.0.1 DNS_PORT="$DNS_PORT" CONTROL_DOMAIN="$CONTROL_DOMAIN" REPORT="$REPORT" bash scripts/test_adguard_home.sh
