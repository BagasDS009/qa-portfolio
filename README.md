# QA Portfolio - Bagas Dimas Saputra

![API Tests (Playwright)](https://github.com/BagasDS009/qa-portfolio/actions/workflows/api-test-playwright.yml/badge.svg)
![API Tests (Cypress)](https://github.com/BagasDS009/qa-portfolio/actions/workflows/api-test-cypress.yml/badge.svg)
![Mobile Tests](https://github.com/BagasDS009/qa-portfolio/actions/workflows/mobile-test-playwright.yml/badge.svg)
![Web Tests](https://github.com/BagasDS009/qa-portfolio/actions/workflows/web-test-playwright.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.49+-green?logo=playwright)
![Cypress](https://img.shields.io/badge/Cypress-13+-green?logo=cypress)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

A comprehensive QA Engineer portfolio showcasing expertise in web automation, API testing, manual testing, database testing, and performance testing across multiple frameworks.

## Portfolio Structure

```
qa-portfolio/
│
├── 01-web-automation-playwright/    → Web UI Automation (Python + Playwright)
├── 02-api-testing-postman/          → API Testing (Postman + Newman)
├── 03-database-testing/             → SQL Database Validation
├── 04-manual-testing/               → Test Plan, Test Cases, Bug Report
├── 05-performance-testing/          → Load & Performance Testing (JMeter)
├── 06-api-testing-playwright/       → API Automation (Python + Playwright)
├── 07-web-test-cypress/             → Web UI Automation (JavaScript + Cypress)
├── 08-api-test-cypress/             → API Automation (JavaScript + Cypress)
└── 09-mobile-web-testing/           → Mobile Web Testing (Playwright Device Emulation)
```

## Projects Detail

| # | Project | Framework | Language | Target |
|---|---------|-----------|----------|--------|
| 01 | Web Automation | Playwright | Python | booking.kai.id |
| 02 | API Testing | Postman/Newman | JavaScript | reqres.in |
| 03 | Database Testing | MySQL/PostgreSQL | SQL | - |
| 04 | Manual Testing | - | - | E-Commerce |
| 05 | Performance Testing | JMeter | - | - |
| 06 | API Automation | Playwright | Python | fakerestapi.azurewebsites.net |
| 07 | Web Automation | Cypress | JavaScript | booking.kai.id |
| 08 | API Automation | Cypress | JavaScript | fakerestapi.azurewebsites.net |
| 09 | Mobile Web Testing | Playwright | Python | saucedemo.com (device emulation) |

## CI/CD Pipelines

All automation projects run on GitHub Actions:

| Workflow | Framework | Status |
|----------|-----------|--------|
| `web-test-playwright.yml` | Playwright (Python) | Partial pass (Cloudflare WAF) |
| `api-test-playwright.yml` | Playwright (Python) | Full pass |
| `api-test-cypress.yml` | Cypress (JavaScript) | Full pass |

## Skills & Tools

| Category | Tools |
|----------|-------|
| Web Automation | Playwright (Python), Cypress (JavaScript) |
| API Testing | Playwright API, Cypress `cy.request()`, Postman, Newman |
| Reporting | Allure Report, pytest-html |
| Database | MySQL, PostgreSQL, SQL |
| Manual Testing | Test Plan, Test Cases, Bug Report, Test Summary |
| Performance | Apache JMeter |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |
| Design Pattern | Page Object Model (POM) |
| Anti-Detection | playwright-stealth, Cloudflare bypass |
| Mobile Testing | Playwright device emulation (iPhone, Pixel, Galaxy, iPad) |

## Test Coverage Summary

| Project | Total Tests | Automated | Status |
|---------|-------------|-----------|--------|
| 01 - Web (Playwright) | 23 | 13 | ✅ Pass (local) |
| 06 - API (Playwright) | 22 | 22 | ✅ Full pass |
| 07 - Web (Cypress) | 13 | 13 | ⚠️ Limited (flexdatalist) |
| 08 - API (Cypress) | 22 | 22 | ✅ Full pass |
| 09 - Mobile Web (Playwright) | 9 (x3 devices) | 29 | ✅ Full pass |
| **Total** | **89** | **99** | |

## How to Run

### Web Automation (Playwright)
```bash
cd 01-web-automation-playwright
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest tests/test_search.py -v
```

### API Automation (Playwright)
```bash
cd 06-api-testing-playwright
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install
pytest -v
```

### API Automation (Cypress)
```bash
cd 08-api-test-cypress
npm install
npx cypress run
```

## Author

**Bagas Dimas Saputra** - QA Engineer

- GitHub: [BagasDS009](https://github.com/BagasDS009)
