#!/bin/bash
# OWASP ZAP Baseline Scan - Quick passive scan
# Runs in ~2 minutes, no active attacks, CI-safe

TARGET_URL="${TARGET_URL:-https://fakerestapi.azurewebsites.net}"
REPORT_DIR="reports"

mkdir -p "$REPORT_DIR"

echo "=== OWASP ZAP Baseline Scan ==="
echo "Target: $TARGET_URL"
echo "================================"

docker run --rm \
    -v "$(pwd)/$REPORT_DIR:/zap/wrk:rw" \
    ghcr.io/zaproxy/zaproxy:stable \
    zap-baseline.py \
    -t "$TARGET_URL" \
    -r baseline-report.html \
    -J baseline-report.json \
    -l WARN \
    --auto

EXIT_CODE=$?

echo ""
echo "Reports generated:"
echo "  - $REPORT_DIR/baseline-report.html"
echo "  - $REPORT_DIR/baseline-report.json"

exit $EXIT_CODE
