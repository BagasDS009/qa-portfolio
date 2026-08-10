# Web Automation - KAI Booking (booking.kai.id)

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.49+-green?logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-8.2+-orange?logo=pytest)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)

## Overview

End-to-end web automation testing untuk **PT Kereta Api Indonesia (KAI)** online booking system menggunakan Playwright + Python dengan Page Object Model pattern.

**Target Website:** [https://booking.kai.id](https://booking.kai.id)

## Test Flow

```
Homepage → Search Train → Select Train → Passenger Data → Seat Selection → Payment → Confirmation
```

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Programming language |
| Playwright | Browser automation framework |
| Pytest | Test runner & assertions |
| Page Object Model | Design pattern |
| Allure Report | Test reporting |
| playwright-stealth | Anti-detection / bot bypass |
| GitHub Actions | CI/CD pipeline |
| pytest-html | HTML test reports |

## Project Structure

```
01-web-automation-playwright/
├── .github/workflows/test.yml      # CI pipeline
├── pages/                           # Page Object Model classes
│   ├── base_page.py                 # Base class (shared methods, human delay)
│   ├── login_page.py                # Login page
│   ├── home_page.py                 # Home/search page (datepicker, station dropdown)
│   ├── train_list_page.py           # Search results
│   ├── passenger_page.py            # Passenger data form
│   ├── seat_page.py                 # Seat selection
│   ├── payment_page.py              # Payment page
│   └── confirmation_page.py         # Booking confirmation
├── tests/                           # Test cases
│   ├── test_data.py                 # Centralized test data
│   ├── test_login.py                # TC-001, TC-002
│   ├── test_search.py               # TC-003
│   ├── test_booking.py              # TC-004, TC-005, TC-006
│   ├── test_validation.py           # TC-007
│   └── test_logout.py               # TC-008
├── reports/                         # Generated reports (gitignored)
├── conftest.py                      # Fixtures, stealth, fresh browser per test
├── pytest.ini                       # Pytest + Allure config
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
└── .gitignore
```

## Test Cases

### TC-001 & TC-002: Login (test_login.py)

| ID | Test Case | Severity |
|----|-----------|----------|
| TC-001 | Valid login with correct credentials | Critical |
| TC-002 | Invalid login - wrong password | Critical |
| TC-002b | Invalid login - unregistered email | Normal |
| TC-002c | Invalid login - empty fields | Normal |

### TC-003: Search Train (test_search.py)

| ID | Test Case | Severity |
|----|-----------|----------|
| TC-003 | Search train valid route (PSE → BD) | Critical |
| TC-003b | Search train alternative route (GMR → YK) | Normal |
| TC-003c | Search with multiple adult passengers (2 adults) | Normal |
| TC-003d | Search with date beyond booking window (no results) | Normal |
| TC-003e | Search form visible on homepage | Blocker |
| TC-003f | Baby cannot exceed adult passengers (tooltip validation) | Normal |

### TC-004, TC-005, TC-006: Booking Flow (test_booking.py)

| ID | Test Case | Severity |
|----|-----------|----------|
| TC-004 | Select train from search results | Critical |
| TC-005 | Change train selection (go back, pick another) | Normal |
| TC-006 | Complete end-to-end booking flow | Critical |

### TC-007: Form Validation (test_validation.py)

| ID | Test Case | Severity |
|----|-----------|----------|
| TC-007 | Submit empty passenger form - validation errors shown | Critical |
| TC-007b | Contact name required - empty name rejected | Normal |
| TC-007c | ID number required - empty ID rejected | Normal |
| TC-007d | Search without origin station - cannot proceed | Normal |

### TC-008: Logout (test_logout.py)

| ID | Test Case | Severity |
|----|-----------|----------|
| TC-008 | Successful logout | Critical |
| TC-008b | Cannot access protected pages after logout | Normal |
| TC-008c | Re-login after logout | Normal |

## Setup & Installation

### Prerequisites
- Python 3.10+
- pip
- Allure CLI (`brew install allure`)

### Installation

```bash
# Clone repository
git clone https://github.com/BagasDS009/qa-portfolio.git
cd qa-portfolio/01-web-automation-playwright

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your KAI credentials
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_search.py -v

# Run single test case
pytest tests/test_search.py::TestSearchTrain::test_search_train_valid_route -v

# Run smoke tests only
pytest -m smoke -v
```

## Reports

### Allure Report (auto-generated after each run)

```bash
# View report (auto-opens in browser)
allure open reports/allure-report

# Or serve live
allure serve reports/allure-results
```

### HTML Report

```bash
open reports/report.html
```

## Anti-Detection Strategy

booking.kai.id uses Cloudflare WAF. This project implements:

| Layer | Implementation |
|-------|---------------|
| Stealth Plugin | `playwright-stealth` - patches navigator.webdriver, chrome runtime |
| Fresh Browser | New browser instance per test (avoids session fingerprinting) |
| Human Delays | Random delays between actions (300-5000ms) |
| Custom User-Agent | Real Chrome user-agent string |
| Realistic Viewport | 1366x768 (common laptop resolution) |
| Locale/Timezone | id-ID, Asia/Jakarta |

## CI/CD Note

> **Known Limitation:** Some tests fail in GitHub Actions CI because booking.kai.id is protected by **Cloudflare Enterprise WAF**, which blocks requests from datacenter IPs (including GitHub-hosted runners). This is a real-world challenge when automating production websites.
>
> **Local execution passes all tests** using residential IP. The CI pipeline is configured to demonstrate the framework capability — partial failures are expected and documented.
>
> **Possible solutions for full CI pass:**
> - Self-hosted runner (uses your local machine IP)
> - Residential proxy integration (BrightData, Oxylabs)
> - Target a staging/test environment without WAF

| Environment | Result | Reason |
|-------------|--------|--------|
| Local (Mac) | All tests pass | Residential IP, not blocked |
| GitHub Actions | Partial pass (3/6) | Cloudflare blocks datacenter IPs |

## Design Decisions

1. **Page Object Model** - Separates page structure from test logic
2. **XPath Locators** - Real selectors from the actual website (inspected via DevTools)
3. **Centralized Test Data** - All data in `test_data.py` for easy maintenance
4. **Fresh Browser Per Test** - Close & reopen to avoid Cloudflare detection
5. **Allure Report** - Professional reporting with steps, screenshots, severity
6. **Screenshot on Failure** - Auto-capture & attach to Allure on failed tests

## Author

**Bagas Dimas Saputra** - QA Engineer
