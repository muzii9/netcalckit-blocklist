#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NetCalcKit contributors
# Verify the current NetCalcKit DNS blocklist against an AdGuard Home DNS endpoint.
#
# Optional environment variables:
#   DNS_SERVER=127.0.0.1
#   DNS_PORT=53
#   LIST_URL=https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt
#   CONTROL_DOMAIN=example.com

set -u

DNS_SERVER="${DNS_SERVER:-127.0.0.1}"
DNS_PORT="${DNS_PORT:-53}"
LIST_URL="${LIST_URL:-https://raw.githubusercontent.com/muzii9/netcalckit-blocklist/main/blocklists/standard.txt}"
CONTROL_DOMAIN="${CONTROL_DOMAIN:-example.com}"

timestamp="$(date +%Y%m%d-%H%M%S)"
report="${REPORT:-$PWD/netcalckit-adguard-test-$timestamp.txt}"
list_file="$(mktemp)"
trap 'rm -f "$list_file"' EXIT

for command_name in dig curl grep awk; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "ERROR: required command not found: $command_name" >&2
        exit 4
    fi
done

total=0
passed=0
retry_passed=0
failed=0
errors=0

is_blocked() {
    grep -qx '0\.0\.0\.0' <<< "$1"
}

run_query() {
    local domain="$1"
    local protocol="$2"
    local timeout="$3"
    local tries="$4"

    if [[ "$protocol" == "tcp" ]]; then
        dig @"$DNS_SERVER" -p "$DNS_PORT" "$domain" A             +tcp +short +time="$timeout" +tries="$tries" 2>&1
    else
        dig @"$DNS_SERVER" -p "$DNS_PORT" "$domain" A             +short +time="$timeout" +tries="$tries" 2>&1
    fi
}

echo "NetCalcKit AdGuard Home Verification"
echo "DNS: $DNS_SERVER:$DNS_PORT"
echo

echo "=== CONTROL TEST ==="
control="$(run_query "$CONTROL_DOMAIN" udp 3 1)"

if [[ -z "$control" ]] || is_blocked "$control" || grep -qiE 'timed out|no servers could be reached|communications error|connection refused|network is unreachable' <<< "$control"; then
    echo "ERROR: control domain did not resolve normally: $CONTROL_DOMAIN"
    echo "$control"
    exit 1
fi

echo "Control OK: $CONTROL_DOMAIN"
echo "$control"
echo

echo "=== DOWNLOADING CURRENT NETCALCKIT LIST ==="
if ! curl -fsSL "$LIST_URL" -o "$list_file"; then
    echo "ERROR: could not download NetCalcKit blocklist." >&2
    exit 1
fi

rule_count="$(grep -Ev '^[[:space:]]*(#|$)' "$list_file" | wc -l | tr -d ' ')"
echo "Rules found: $rule_count"
echo

{
    echo "NetCalcKit AdGuard Home Verification"
    echo "Date: $(date)"
    echo "DNS server: $DNS_SERVER:$DNS_PORT"
    echo "Rules downloaded: $rule_count"
    echo
} > "$report"

echo "=== FULL BLOCKLIST TEST ==="

while IFS= read -r domain; do
    domain="${domain//$'\r'/}"
    [[ -z "$domain" || "$domain" == \#* ]] && continue

    ((total++))

    result1="$(run_query "$domain" udp 2 1)"
    if is_blocked "$result1"; then
        ((passed++))
        printf "PASS        %-45s UDP\n" "$domain"
        printf "PASS        %-45s UDP\n" "$domain" >> "$report"
        continue
    fi

    sleep 0.15
    result2="$(run_query "$domain" udp 5 2)"
    if is_blocked "$result2"; then
        ((retry_passed++))
        printf "RETRY PASS  %-45s UDP retry\n" "$domain"
        printf "RETRY PASS  %-45s UDP retry\n" "$domain" >> "$report"
        continue
    fi

    sleep 0.15
    result3="$(run_query "$domain" tcp 5 2)"
    if is_blocked "$result3"; then
        ((retry_passed++))
        printf "RETRY PASS  %-45s TCP fallback\n" "$domain"
        printf "RETRY PASS  %-45s TCP fallback\n" "$domain" >> "$report"
        continue
    fi

    combined="$result1"$'\n'"$result2"$'\n'"$result3"
    if grep -qiE 'timed out|no servers could be reached|communications error|connection refused|network is unreachable' <<< "$combined"; then
        ((errors++))
        printf "ERROR       %-45s DNS transport failure\n" "$domain"
        {
            printf "ERROR       %-45s DNS transport failure\n" "$domain"
            echo "  UDP1: $(tr '\n' ' ' <<< "$result1")"
            echo "  UDP2: $(tr '\n' ' ' <<< "$result2")"
            echo "  TCP : $(tr '\n' ' ' <<< "$result3")"
        } >> "$report"
        continue
    fi

    ((failed++))
    final_answer="$(tr '\n' ' ' <<< "$result3")"
    printf "FAIL        %-45s %s\n" "$domain" "$final_answer"
    {
        printf "FAIL        %-45s %s\n" "$domain" "$final_answer"
        echo "  UDP1: $(tr '\n' ' ' <<< "$result1")"
        echo "  UDP2: $(tr '\n' ' ' <<< "$result2")"
        echo "  TCP : $(tr '\n' ' ' <<< "$result3")"
    } >> "$report"

done < "$list_file"

confirmed=$((passed + retry_passed))

{
    echo
    echo "================== SUMMARY =================="
    echo "Total rules tested : $total"
    echo "Immediate PASS     : $passed"
    echo "Retry PASS         : $retry_passed"
    echo "Confirmed blocked  : $confirmed"
    echo "Real FAIL          : $failed"
    echo "DNS errors         : $errors"
    if (( total > 0 )); then
        awk -v c="$confirmed" -v t="$total" 'BEGIN { printf "Confirmed pass rate: %.2f%%\n", (c/t)*100 }'
    fi
    echo "============================================="
} | tee -a "$report"

echo
echo "Report saved: $report"

if (( failed == 0 && errors == 0 && confirmed == total )); then
    echo "RESULT: ALL RULES VERIFIED"
    exit 0
elif (( failed == 0 )); then
    echo "RESULT: BLOCKING OK, BUT SOME DNS TESTS WERE INCONCLUSIVE"
    exit 2
else
    echo "RESULT: ONE OR MORE RULES REQUIRE REVIEW"
    exit 3
fi
