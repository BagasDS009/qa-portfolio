# 13 - Performance Testing with k6

![k6](https://img.shields.io/badge/k6-7.x-7D64FF?logo=k6&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

Automated performance testing using **k6** (Grafana) — a modern, developer-friendly load testing tool. This project covers 5 types of performance tests against the FakeREST API.

**Target API:** [fakerestapi.azurewebsites.net](https://fakerestapi.azurewebsites.net/api/v1)

## Test Types

| # | Type | Purpose | VUs | Duration |
|---|------|---------|-----|----------|
| 1 | Smoke Test | Verify system is alive | 1 | 30s |
| 2 | Load Test | Normal traffic patterns | 20→50 | 5 min |
| 3 | Stress Test | Find breaking point | 10→200 | 5 min |
| 4 | Spike Test | Sudden traffic surge | 5→150→5 | 1.5 min |
| 5 | Soak Test | Sustained endurance | 30 | 6.5 min |

## Thresholds (Pass/Fail Criteria)

| Test | p(95) Response Time | Error Rate | Throughput |
|------|--------------------:|------------|------------|
| Smoke | < 2000ms | < 1% | - |
| Load | < 1500ms | < 5% | > 10 req/s |
| Stress | < 5000ms | < 15% | - |
| Spike | < 4000ms | < 10% | - |
| Soak | < 2000ms | < 2% | - |

## Project Structure

```
13-performance-testing-k6/
├── scripts/
│   ├── smoke-test.js      # Quick health check
│   ├── load-test.js       # Normal capacity test
│   ├── stress-test.js     # Beyond capacity test
│   ├── spike-test.js      # Sudden burst test
│   └── soak-test.js       # Endurance test
├── .gitignore
└── README.md
```

## Setup & Run

### Prerequisites

```bash
# macOS
brew install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D68
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update && sudo apt-get install k6
```

### Run Tests

```bash
# Smoke test (quick health check)
k6 run scripts/smoke-test.js

# Load test (normal traffic)
k6 run scripts/load-test.js

# Stress test (find breaking point)
k6 run scripts/stress-test.js

# Spike test (sudden surge)
k6 run scripts/spike-test.js

# Soak test (endurance)
k6 run scripts/soak-test.js

# Custom base URL
k6 run -e BASE_URL=https://your-api.com/api/v1 scripts/load-test.js

# Output to JSON for post-processing
k6 run --out json=results.json scripts/load-test.js
```

## CI/CD Integration

Runs automatically in GitHub Actions with threshold-based pass/fail:

```yaml
- name: Run k6 Smoke Test
  run: k6 run scripts/smoke-test.js
```

If thresholds are breached, the pipeline fails — **shift-left performance testing**.

## Key Metrics Monitored

| Metric | Description |
|--------|-------------|
| `http_req_duration` | Total request time (DNS + connect + TLS + send + wait + receive) |
| `http_req_failed` | Percentage of failed requests |
| `http_reqs` | Total requests per second (throughput) |
| `vus` | Number of concurrent virtual users |
| `checks` | Assertion pass rate |

## Sample Output

```
     ✓ GET all: status 200
     ✓ GET by ID: status 200
     ✓ POST: status 200

     checks.........................: 100.00% ✓ 4521 ✗ 0
     http_req_duration..............: avg=234ms  min=45ms  p(95)=890ms  p(99)=1.2s
     http_req_failed................: 0.00%   ✓ 0    ✗ 4521
     http_reqs......................: 4521    15.07/s
     vus............................: 50      min=0   max=50
```

## Why k6 over JMeter?

| Aspect | k6 | JMeter |
|--------|-----|--------|
| Language | JavaScript (ES6) | XML/GUI |
| CI/CD | Native CLI, easy pipeline | Needs JMeter binary |
| Version Control | Scripts are code | XML blobs, hard to diff |
| Developer Experience | Modern, code-first | GUI-first, complex |
| Resource Usage | Go-based, lightweight | JVM, heavy |
| Cloud Integration | Grafana Cloud native | Third-party plugins |

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating shift-left performance testing with code-first approach*
