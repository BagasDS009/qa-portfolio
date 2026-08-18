# 19 — Web Test Generator (Kiro Agent)

AI-powered Senior QE agent yang generate **complete web automation testing** secara cepat, akurat, dan profesional — mencakup functional, accessibility, performance, dan visual regression testing.

---

## What Makes This Different

| Aspect | Basic Agent | This Agent (Senior QE Level) |
|--------|-------------|------------------------------|
| Planning | Jump langsung ke test | Risk-based strategy dulu |
| Coverage | Happy path + negative | + Edge case + Security + a11y + Visual + Performance |
| API Layer | UI only | + Network intercept + Mock failures |
| Accessibility | None | WCAG 2.1 AA (axe-core + keyboard + ARIA) |
| Visual | None | Screenshot comparison multi-viewport |
| Performance | None | Core Web Vitals + API budgets |
| Maintenance | No guidance | Anti-pattern rules + flaky prevention |
| Cross-browser | Single browser | Chrome + Firefox + Safari matrix |

---

## Skills Overview

```
                              ┌─── Skill 3 (Functional Tests)
                              │
Skill 0 (Strategy) → Skill 1 (Analyze) → Skill 2 (Test Cases) ──┼─── Skill 4 (Accessibility)
                                                                  │
                                                                  ├─── Skill 5 (API + Performance)
                                                                  │
                                                                  └─── Skill 6 (Visual Regression)
```

| # | Skill | Apa yang dihasilkan |
|---|-------|---------------------|
| 0 | Test Strategy | Risk assessment, coverage plan, quality gates, browser matrix |
| 1 | Analyze Website | Element inventory, user flows, test boundaries |
| 2 | Generate Test Cases | Scenario: critical, positive, negative, edge, security |
| 3 | Generate Automation | Playwright + pytest code (POM, fixtures, Allure, auto-report) |
| 4 | Accessibility | axe-core scan, keyboard nav, ARIA, color contrast |
| 5 | API Intercept | Request validation, mock failures, performance budgets, Web Vitals |
| 6 | Visual Regression | Screenshot comparison, component states, responsive, cross-browser |
| 7 | Refactor & Fix | Diagnose errors, fix broken tests, refactor code, auto fix-loop |

---

## Quick Start

### Full Professional Suite
```
Generate complete test suite untuk https://practicesoftwaretesting.com
Mulai dari test strategy (risk assessment), lalu generate semua:
functional, accessibility, API intercept, dan visual regression test.
```

### Specific Skill
```
# Strategy only
Buat risk-based test strategy untuk https://myapp.com

# Accessibility only
Generate accessibility test untuk https://myapp.com/checkout

# Visual regression only
Generate visual regression test untuk semua halaman kritis
```

---

## Output Convention

Setiap website yang di-generate mendapat folder sendiri di `output/`:

```
output/
├── practicesoftwaretesting/     ← website pertama
├── tokopedia/                   ← website kedua
├── myapp-staging/               ← website ketiga
└── tokopedia-v2/                ← same site, re-generated
```

**Naming rules:**
- Dari URL domain: `https://practicesoftwaretesting.com` → `practicesoftwaretesting`
- Subdomain jadi suffix: `staging.myapp.io` → `myapp-staging`
- Custom name via prompt: `--name tokopedia-v2`
- Folder sudah ada? Agent tanya: overwrite, rename (`-v2`), atau abort

## Generated Project Structure (Per Output)

```
output/[project-name]/
├── docs/                              ← Skill 0, 1, 2 (documents)
│   ├── test-strategy.md              ← Risk assessment, quality gates
│   ├── site-analysis.md              ← Element inventory, user flows
│   ├── test-cases.md                 ← Semua scenario + TC-IDs
│   └── traceability-matrix.md        ← TC-ID → test method → page object
│
└── automation/                        ← Skill 3, 4, 5, 6 (executable code)
    ├── conftest.py                   ← Core fixtures & hooks
    ├── pytest.ini                    ← Markers, plugins
    ├── requirements.txt              ← Dependencies
    ├── .gitignore
    │
    ├── config/                       ← Multi-environment
    │   ├── .env.dev
    │   ├── .env.sit
    │   ├── .env.staging
    │   └── settings.py              ← Config loader
    │
    ├── pages/                        ← Page Objects
    │   ├── __init__.py
    │   ├── base_page.py
    │   └── [feature]_page.py
    │
    ├── tests/                        ← Test suites
    │   ├── test_[feature].py         ← Functional
    │   ├── test_accessibility.py     ← a11y (Skill 4)
    │   ├── test_api_intercept.py     ← API validation (Skill 5)
    │   ├── test_performance.py       ← Performance (Skill 5)
    │   └── test_visual.py           ← Visual regression (Skill 6)
    │
    ├── test_data/                    ← Separated test data
    │   ├── users.py                  ← Credentials per role
    │   ├── products.py               ← Product data
    │   ├── addresses.py              ← Billing/shipping
    │   └── negative_inputs.py        ← Invalid/boundary/security
    │
    ├── fixtures/                     ← Complex reusable setup
    │   ├── auth.py                   ← Login/register
    │   ├── cart.py                   ← Pre-filled cart
    │   └── database.py              ← Data seeding/cleanup
    │
    ├── utils/                        ← Shared utilities
    │   ├── config.py                 ← Settings loader
    │   ├── accessibility.py          ← axe-core helpers
    │   ├── visual.py                ← Screenshot comparison
    │   └── api_helpers.py           ← Network intercept helpers
    │
    └── reports/                      ← Test artifacts (gitignored)
        ├── allure-results/
        ├── screenshots/
        └── visual/
            ├── baselines/            ← Reference images (committed)
            ├── actual/               ← Current run (gitignored)
            └── diffs/                ← Diff images (gitignored)
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Automation | Playwright (sync API) |
| Framework | pytest + plugins |
| Reporting | Allure |
| Accessibility | axe-core 4.9 |
| Visual | Pillow + numpy |
| Performance | Web Vitals API |
| Pattern | Page Object Model |

---

## Test Execution

```bash
# === Setup (first time) ===
cd output/practicesoftwaretesting/automation
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install firefox
brew install allure    # for auto-report

# === Run Tests (report auto-opens in browser) ===
pytest -v              # all 63 tests + auto-report
pytest -m smoke -v     # 9 critical path tests + auto-report
pytest -m wave1 -v     # 47 functional tests + auto-report
pytest -m a11y -v      # 16 accessibility tests + auto-report

# === Other Markers ===
pytest -m regression -v
pytest -m "api or performance" -v

# === Cross-browser (install tambahan dulu) ===
playwright install chromium webkit
pytest --browser firefox --browser chromium --browser webkit -v

# === Headed debug mode (lihat browser) ===
pytest --browser firefox --headed --slowmo=500 -v

# === Deactivate venv when done ===
deactivate
```

### Report Features

| Feature | Detail |
|---------|--------|
| Auto-open | Report otomatis muncul di browser setelah pytest selesai |
| Fresh per run | `--clean-alluredir` — hanya hasil run saat ini yang ditampilkan |
| Screenshot per step | Setiap `allure.step` punya full-page screenshot |
| Screenshot on failure | Extra full-page screenshot saat test gagal |
| Markers shown | Tags smoke/wave1/regression/a11y terlihat di report |
| Step timeline | Detail per-step dengan durasi |

---

## Quality Gates

```
RELEASE BLOCKED if:
  ✗ Any CRITICAL test fails
  ✗ > 5% of NORMAL tests fail
  ✗ Accessibility score < 90
  ✗ LCP > 2.5s on critical pages
  ✗ Visual diff > 0.1% on critical pages

RELEASE WARNING if:
  ⚠ Any NORMAL test fails
  ⚠ New a11y violations introduced
  ⚠ CLS > 0.1 on any page
  ⚠ Test execution time increased > 20%
```

---

## Agent Files

```
19-web-test-generator/
├── .kiro/
│   ├── agents/web-test-generator/
│   │   ├── agent.md                      ← Agent identity & config
│   │   └── skills/
│   │       ├── 0-test-strategy.md        ← Risk-based planning
│   │       ├── 1-analyze-website.md      ← Website analysis
│   │       ├── 2-generate-test-cases.md  ← Test case design
│   │       ├── 3-generate-automation.md  ← Functional code generation
│   │       ├── 4-accessibility-test.md   ← a11y testing
│   │       ├── 5-api-intercept-test.md   ← API + performance
│   │       └── 6-visual-regression.md    ← Visual testing
│   └── steering/
│       └── test-quality-standards.md     ← Quality rules & anti-patterns
├── PROMPT-GUIDE.md                       ← How to use + example prompts
└── README.md                             ← This file
```

---

## CI/CD Integration

```yaml
# GitHub Actions
name: Test Suite
on: [push, pull_request]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: playwright install firefox --with-deps
      - run: pytest -m smoke --alluredir=reports/allure-results
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: allure-results, path: reports/allure-results }

  regression:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: playwright install firefox --with-deps
      - run: pytest -m "regression and not slow" --alluredir=reports/allure-results
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: regression-results, path: reports/allure-results }
```

---

## FAQ

**Q: Apakah agent ini hanya untuk satu website?**
A: Tidak. Agent ini bisa generate test suite untuk website apapun — cukup kasih URL.

**Q: Kalau website-nya pakai React/Vue/Angular?**
A: Fully supported. Playwright handle SPA dengan auto-wait. Agent adapt selector strategy ke framework yang dipakai.

**Q: Apakah accessibility test bisa replace manual audit?**
A: Automated a11y (axe-core) menangkap ~30% masalah. Masih perlu manual testing untuk full WCAG compliance (screen reader, cognitive accessibility). Tapi 30% otomatis itu gratis dan jalan di setiap build.

**Q: Visual test gagal terus karena dynamic content?**
A: Agent generate strategy untuk mock/hide dynamic elements (timestamps, random IDs) sebelum screenshot. Threshold juga bisa di-adjust.

**Q: Bisa parallel execution?**
A: Ya. Install `pytest-xdist` dan run `pytest -n auto`. Tests sudah designed untuk isolation.

---

## License

Portfolio project — for demonstration purposes.
