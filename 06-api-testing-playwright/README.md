# API Testing with Playwright (Python)

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.49+-green?logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-8.2+-orange?logo=pytest)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

Automated REST API testing framework using Playwright's API testing capabilities with pytest and Allure reporting.

**Target API:** [FakeREST API](https://fakerestapi.azurewebsites.net/index.html)

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Programming language |
| Playwright | HTTP client for API requests |
| pytest | Test framework |
| Allure Report | Professional test reporting |
| GitHub Actions | CI/CD pipeline |

## API Resources Under Test

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Activities | `/api/v1/Activities` | GET, POST, PUT, DELETE |
| Authors | `/api/v1/Authors` | GET, POST, PUT, DELETE |
| Books | `/api/v1/Books` | GET, POST, PUT, DELETE |
| Users | `/api/v1/Users` | GET, POST, PUT, DELETE |

## Test Cases (22 Total)

### Activities (6 tests)

| Test Case | Method | Expected |
|-----------|--------|----------|
| Get all activities | GET | Status 200, returns list |
| Get activity by ID | GET /1 | Status 200, correct fields |
| Get non-existent activity | GET /99999 | Status 404 |
| Create activity | POST | Status 200, body matches |
| Update activity | PUT /999 | Status 200, updated fields |
| Delete activity | DELETE /999 | Status 200 |

### Authors (6 tests)

| Test Case | Method | Expected |
|-----------|--------|----------|
| Get all authors | GET | Status 200, returns list |
| Get author by ID | GET /1 | Status 200, correct fields |
| Get authors by book ID | GET /authors/books/1 | Status 200, returns list |
| Create author | POST | Status 200, body matches |
| Update author | PUT /999 | Status 200, updated fields |
| Delete author | DELETE /999 | Status 200 |

### Books (5 tests)

| Test Case | Method | Expected |
|-----------|--------|----------|
| Get all books | GET | Status 200, returns list |
| Get book by ID | GET /1 | Status 200, required fields |
| Create book | POST | Status 200, body matches |
| Update book | PUT /999 | Status 200, updated fields |
| Delete book | DELETE /999 | Status 200 |

### Users (5 tests)

| Test Case | Method | Expected |
|-----------|--------|----------|
| Get all users | GET | Status 200, returns list |
| Get user by ID | GET /1 | Status 200, correct fields |
| Create user | POST | Status 200, body matches |
| Update user | PUT /999 | Status 200, updated fields |
| Delete user | DELETE /999 | Status 200 |

## Project Structure

```
06-api-testing-playwright/
├── tests/
│   ├── __init__.py
│   ├── test_data.py          # Centralized test payloads
│   ├── test_activities.py    # Activities CRUD tests
│   ├── test_authors.py       # Authors CRUD tests
│   ├── test_books.py         # Books CRUD tests
│   └── test_users.py         # Users CRUD tests
├── conftest.py               # Playwright API context fixture + Allure hook
├── pytest.ini                # pytest + Allure configuration
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## Setup & Installation

```bash
cd 06-api-testing-playwright

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright (required for API context)
playwright install
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run CRUD tests only
pytest -m crud

# Run specific resource
pytest tests/test_activities.py
pytest tests/test_books.py

# Run with HTML report
pytest --html=reports/report.html --self-contained-html
```

## Reports

### Allure Report (auto-generated)

```bash
# After running pytest, open report
allure open reports/allure-report

# Or serve live
allure serve reports/allure-results
```

### Test Execution Summary

```
Test Summary - API Automation (FakeREST API)
────────────────────────────────────────────
Total     : 22
Passed    : 22
Failed    : 0
Skipped   : 0
Pass Rate : 100%

Test Suites
├── Activities
│   ├── GET all activities              ✓
│   ├── GET activity by ID              ✓
│   ├── GET non-existent (404)          ✓
│   ├── POST create activity            ✓
│   ├── PUT update activity             ✓
│   └── DELETE activity                 ✓
│
├── Authors
│   ├── GET all authors                 ✓
│   ├── GET author by ID               ✓
│   ├── GET authors by book ID          ✓
│   ├── POST create author              ✓
│   ├── PUT update author               ✓
│   └── DELETE author                   ✓
│
├── Books
│   ├── GET all books                   ✓
│   ├── GET book by ID                  ✓
│   ├── POST create book                ✓
│   ├── PUT update book                 ✓
│   └── DELETE book                     ✓
│
└── Users
    ├── GET all users                   ✓
    ├── GET user by ID                  ✓
    ├── POST create user                ✓
    ├── PUT update user                 ✓
    └── DELETE user                     ✓
```

### Report Flow

```
Playwright API Context
        ↓
Pytest Execution
        ↓
Allure Results (JSON)
        ↓
Allure Generate
        ↓
Interactive HTML Report
        ↓
GitHub Actions Artifact
```

## CI/CD

GitHub Actions workflow runs automatically on:
- Push to `main` / `develop`
- Pull Request to `main`
- Manual trigger (workflow_dispatch)

CI generates Allure + HTML reports as downloadable artifacts.

> **Note:** Unlike the web automation tests, API tests run perfectly in CI since FakeREST API has no Cloudflare WAF or bot detection.

## Design Decisions

1. **Playwright API Context** - Uses Playwright's built-in HTTP client (not `requests` library) for consistency with broader test ecosystem
2. **Session-scoped fixture** - API context shared across all tests for performance
3. **Centralized test data** - All payloads in `test_data.py` for easy maintenance
4. **Allure integration** - `@allure.step()` for detailed step-by-step reporting
5. **Markers** - `@pytest.mark.smoke` and `@pytest.mark.crud` for selective execution

## Author

**Bagas Dimas Saputra** - QA Engineer
