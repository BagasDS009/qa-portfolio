#!/bin/bash
# OWASP ZAP Full Scan - Active + Passive scan
# WARNING: This performs active attacks. Only use on targets you own or have permission to test.
# Takes 10-30 minutes depending on target size.

TARGET_URL="${TARGET_URL:-https://fakerestapi.azurewebsites.net}"
REPORT_DIR="reports"

mkdir -p "$REPORT_DIR"

echo "=== OWASP ZAP Full Scan ==="
echo "Target: $TARGET_URL"
echo "WARNING: Active scanning enabled!"
echo "============================"

docker run --rm \
    -v "$(pwd)/$REPORT_DIR:/zap/wrk:rw" \
    ghcr.io/zaproxy/zaproxy:stable \
    zap-full-scan.py \
    -t "$TARGET_URL" \
    -r full-scan-report.html \
    -J full-scan-report.json \
    -l WARN \
    --auto

EXIT_CODE=$?

echo ""
echo "Reports generated:"
echo "  - $REPORT_DIR/full-scan-report.html"
echo "  - $REPORT_DIR/full-scan-report.json"

exit $EXIT_CODE
