# 20 — API Test Generator (Kiro Agent)

AI-powered Senior QE agent yang generate **complete API automation testing** — functional, contract, security, dan performance testing menggunakan Python + httpx + pytest + Allure.

---

## What This Does

| Aspect | Detail |
|--------|--------|
| Input | API URL, Swagger/OpenAPI spec, or Postman collection |
| Output | Complete pytest test suite with Allure reporting |
| Coverage | Functional + Contract + Security + Performance |
| Response Capture | Every API call attached as JSON to report |
| Report | Auto-opens in browser after `pytest` |

## Skills

| # | Skill | Purpose |
|---|-------|---------|
| 0 | API Strategy | Risk-based analysis, coverage planning |
| 1 | Analyze API | Extract endpoints, schemas, auth from spec |
| 2 | Generate Test Cases | Design: positive, negative, security, contract |
| 3 | Generate Automation | Produce pytest + httpx code with Allure |
| 4 | Contract Testing | Schema validation, breaking change detection |
| 5 | Security Testing | OWASP API Top 10 coverage |
| 6 | Performance Testing | Response time budgets, concurrency |
| 7 | Fix & Refactor | Diagnose failures, fix tests autonomously |

## Quick Start

```
Generate API test suite untuk https://reqres.in/api
Cover: users CRUD, auth, negative cases, contract validation.
```

## Generated Structure

```
output/[api-name]/
├── docs/                        ← Strategy, analysis, test cases
└── automation/
    ├── api/                     ← HTTP client layer
    │   ├── base_client.py       ← Wrapper with Allure logging
    │   └── [service]_client.py  ← Typed endpoint methods
    ├── schemas/                  ← Pydantic models for validation
    ├── tests/                    ← Test suites
    │   ├── test_[endpoint].py
    │   ├── test_contract.py
    │   ├── test_security.py
    │   └── test_performance.py
    ├── test_data/                ← Payloads, credentials
    ├── fixtures/                 ← Auth tokens, cleanup
    └── reports/                  ← Allure results
```

## Test Execution

```bash
# Setup
cd output/[api-name]/automation
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install allure

# Run (report auto-opens)
pytest -v                    # all tests + report
pytest -m smoke -v           # CRUD happy path
pytest -m contract -v        # schema validation
pytest -m security -v        # OWASP API Top 10
pytest -m performance -v     # response time budgets

# Different environment
ENV=staging pytest -v
```

## Report Features

| Feature | Detail |
|---------|--------|
| Auto-open | Report opens in browser after `pytest` finishes |
| Fresh per run | `--clean-alluredir` — only current run shown |
| Response capture | Every API call: request + response + timing as JSON |
| Per-step detail | Each `allure.step()` shows what was called |
| No screenshots | API = JSON attachments (equivalent of screenshots) |

## Differences from Folder 19 (Web UI Agent)

| Aspect | 19 (Web UI) | 20 (API) |
|--------|-------------|----------|
| Target | Website UI | REST/GraphQL API |
| Client | Playwright (browser) | httpx (HTTP client) |
| Assertions | Element visible, text contains | Status code, JSON body, schema |
| Screenshots | Full-page PNG | Response body JSON |
| Page Objects | POM classes | API Client classes |
| Contract | N/A | JSON Schema / Pydantic validation |
| Security | XSS in input | OWASP API Top 10 |
| Performance | Web Vitals, LCP | Response time budgets (ms) |

## License

Portfolio project — for demonstration purposes.
