#!/bin/bash
# OWASP ZAP API Scan - Scan API using OpenAPI spec
# Runs active scan against API endpoints

TARGET_URL="${TARGET_URL:-https://fakerestapi.azurewebsites.net}"
OPENAPI_URL="${TARGET_URL}/swagger/v1/swagger.json"
REPORT_DIR="reports"

mkdir -p "$REPORT_DIR"

echo "=== OWASP ZAP API Scan ==="
echo "Target: $TARGET_URL"
echo "OpenAPI: $OPENAPI_URL"
echo "==========================="

docker run --rm \
    -v "$(pwd)/$REPORT_DIR:/zap/wrk:rw" \
    ghcr.io/zaproxy/zaproxy:stable \
    zap-api-scan.py \
    -t "$OPENAPI_URL" \
    -f openapi \
    -r api-scan-report.html \
    -J api-scan-report.json \
    -l WARN \
    --auto

EXIT_CODE=$?

echo ""
echo "Reports generated:"
echo "  - $REPORT_DIR/api-scan-report.html"
echo "  - $REPORT_DIR/api-scan-report.json"

exit $EXIT_CODE
