# QA Portfolio - Bagas Dimas Saputra

![Playwright Tests](https://github.com/BagasDS009/qa-portfolio/actions/workflows/playwright-tests.yml/badge.svg)
![Cypress Tests](https://github.com/BagasDS009/qa-portfolio/actions/workflows/cypress-tests.yml/badge.svg)
![Selenium Tests](https://github.com/BagasDS009/qa-portfolio/actions/workflows/selenium-tests.yml/badge.svg)

## Live Test Report

> All test executions are automatically published via GitHub Actions after each push to `main`.

| Report | URL | Content |
|--------|-----|---------|
| Allure Report | [bagasds009.github.io/qa-portfolio](https://bagasds009.github.io/qa-portfolio/) | Combined results from all frameworks (Playwright, Cypress, Selenium) with execution timeline, pass/fail breakdown, and request/response details |

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Java](https://img.shields.io/badge/Java-17-red?logo=openjdk)
![Playwright](https://img.shields.io/badge/Playwright-1.49+-green?logo=playwright)
![Cypress](https://img.shields.io/badge/Cypress-13+-green?logo=cypress)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green?logo=selenium)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

A comprehensive QA Engineer portfolio showcasing expertise in web automation, API testing, mobile web testing, manual testing, database testing, and performance testing across multiple frameworks and languages.

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
├── 09-mobile-web-testing/           → Mobile Web Testing (Playwright Device Emulation)
├── 10-web-automation-selenium/      → Web UI Automation (Java + Selenium)
├── 11-api-test-selenium/            → API Automation (Java + RestAssured)
└── 12-mobile-web-testing-selenium/  → Mobile Web Testing (Java + Selenium Firefox)
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
| 10 | Web Automation | Selenium | Java | automationexercise.com |
| 11 | API Automation | RestAssured | Java | fakerestapi.azurewebsites.net |
| 12 | Mobile Web Testing | Selenium (Firefox) | Java | saucedemo.com (viewport emulation) |

## CI/CD Pipelines

All automation projects run on GitHub Actions:

| Workflow | Framework | Projects | Status |
|----------|-----------|----------|--------|
| `playwright-tests.yml` | Playwright (Python) | 01, 06, 09 | ✅ |
| `cypress-tests.yml` | Cypress (JavaScript) | 08 | ✅ |
| `selenium-tests.yml` | Selenium/RestAssured (Java) | 10, 11, 12 | ✅ |
| `deploy-reports.yml` | Allure Reports → GitHub Pages | All | ✅ |

## Skills & Tools

| Category | Tools |
|----------|-------|
| Web Automation | Playwright (Python), Cypress (JavaScript), Selenium (Java) |
| API Testing | Playwright API, Cypress `cy.request()`, RestAssured, Postman, Newman |
| Mobile Testing | Playwright device emulation, Selenium Firefox viewport emulation |
| Reporting | Allure Report, pytest-html |
| Database | MySQL, PostgreSQL, SQL |
| Manual Testing | Test Plan, Test Cases, Bug Report, Test Summary |
| Performance | Apache JMeter |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |
| Build Tools | Maven, npm |
| Design Pattern | Page Object Model (POM) |
| Languages | Python, Java, JavaScript, SQL |

## Test Coverage Summary

| Project | Total Tests | Automated | Status |
|---------|-------------|-----------|--------|
| 01 - Web (Playwright) | 23 | 13 | ✅ Pass (local) |
| 06 - API (Playwright) | 22 | 22 | ✅ Full pass |
| 07 - Web (Cypress) | 13 | 13 | ⚠️ Limited (flexdatalist) |
| 08 - API (Cypress) | 25 | 25 | ✅ Full pass |
| 09 - Mobile Web (Playwright) | 9 (x3 devices) | 29 | ✅ Full pass |
| 10 - Web (Selenium) | 7 | 7 | ✅ Pass (local) |
| 11 - API (RestAssured) | 25 | 25 | ✅ Full pass |
| 12 - Mobile Web (Selenium) | 17 (x3 devices) | 39 | ✅ Full pass |
| **Total** | **141** | **173** | |

## How to Run

### Playwright (Python)
```bash
cd 01-web-automation-playwright
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest tests/ -v
```

### Cypress (JavaScript)
```bash
cd 08-api-test-cypress
npm install
npx cypress run
```

### Selenium / RestAssured (Java)
```bash
cd 11-api-test-selenium
mvn clean test

cd ../12-mobile-web-testing-selenium
mvn clean test
```

## Author

**Bagas Dimas Saputra** - QA Engineer

- GitHub: [BagasDS009](https://github.com/BagasDS009)
