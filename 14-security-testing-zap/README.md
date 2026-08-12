# 14 - Security Testing with OWASP ZAP

![OWASP](https://img.shields.io/badge/OWASP-ZAP-orange?logo=owasp)
![Docker](https://img.shields.io/badge/Docker-Required-2496ED?logo=docker)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

Automated security testing using **OWASP ZAP** (Zed Attack Proxy) — the world's most popular open-source web security scanner. This project demonstrates shift-left security with automated vulnerability scanning in CI pipelines.

**Target API:** [fakerestapi.azurewebsites.net](https://fakerestapi.azurewebsites.net/api/v1)

## Scan Types

| # | Type | Duration | Approach | CI-Safe |
|---|------|----------|----------|---------|
| 1 | Baseline Scan | ~2 min | Passive only (spider + observe) | Yes |
| 2 | API Scan | ~5 min | OpenAPI spec-driven, light active | Yes |
| 3 | Full Scan | 10-30 min | Active + Passive (attacks target) | Permission required |

## OWASP Top 10 Coverage

| # | Vulnerability | ZAP Rule | Detection |
|---|---|---|---|
| A01 | Broken Access Control | 40012, 10021 | Active scan |
| A02 | Cryptographic Failures | 10011, 10010 | Passive scan |
| A03 | Injection (SQL, OS Command) | 40018, 90020 | Active scan |
| A05 | Security Misconfiguration | 10020, 10038 | Passive scan |
| A07 | Cross-Site Scripting (XSS) | 40012, 40014 | Active scan |
| A08 | Software & Data Integrity | 10017 | Passive scan |
| A09 | Security Logging Failures | 10015 | Passive scan |

## Project Structure

```
14-security-testing-zap/
├── scripts/
│   ├── baseline-scan.sh    # Passive scan (CI-safe, fast)
│   ├── api-scan.sh         # API-focused scan via OpenAPI spec
│   └── full-scan.sh        # Full active + passive scan
├── zap-rules.conf          # Custom rule config (IGNORE/WARN/FAIL)
├── .gitignore
└── README.md
```

## Setup & Run

### Prerequisites

- Docker installed (`brew install --cask docker`)

### Run Scans

```bash
cd 14-security-testing-zap

# Quick baseline scan (passive, CI-safe)
chmod +x scripts/*.sh
./scripts/baseline-scan.sh

# API scan using OpenAPI/Swagger spec
./scripts/api-scan.sh

# Full scan (active attacks - use only on authorized targets!)
./scripts/full-scan.sh

# Custom target
TARGET_URL=https://your-app.com ./scripts/baseline-scan.sh
```

## CI/CD Integration

Baseline scan runs automatically in GitHub Actions:

```yaml
- name: OWASP ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.12.0
  with:
    target: 'https://fakerestapi.azurewebsites.net'
    rules_file_name: 'zap-rules.conf'
```

## Rule Configuration

The `zap-rules.conf` file controls CI behavior:

| Action | Meaning |
|--------|---------|
| `IGNORE` | Don't report (informational noise) |
| `WARN` | Report in results but don't fail build |
| `FAIL` | Critical vulnerability — block deployment |

## Sample Findings

```
WARN-NEW: X-Frame-Options Header Not Set [10020]
WARN-NEW: Content Security Policy Not Set [10038]
WARN-NEW: Cookie Without Secure Flag [10011]
PASS: SQL Injection [40018] - No vulnerabilities found
PASS: Cross Site Scripting [40012] - No vulnerabilities found
PASS: Remote OS Command Injection [90020] - No vulnerabilities found
```

## Reports

Reports are generated in HTML and JSON format:
- `reports/baseline-report.html` — Visual summary with risk levels
- `reports/api-scan-report.json` — Machine-parseable for CI integration

## Key Concepts Demonstrated

- **Shift-left security**: Automated scans in CI before deployment
- **OWASP Top 10 awareness**: Configured rules map to OWASP categories
- **Risk-based rule configuration**: IGNORE/WARN/FAIL based on severity
- **API security testing**: OpenAPI spec-driven scanning
- **Docker-based execution**: No local install needed, reproducible

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating security testing integration in CI/CD pipelines*
