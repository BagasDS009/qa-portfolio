# 🚆 Web Automation - KAI Booking (booking.kai.id)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.44-green?logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-8.2-orange?logo=pytest)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

End-to-end web automation testing untuk **PT Kereta Api Indonesia (KAI)** online booking system menggunakan Playwright + Python dengan Page Object Model pattern.

**Target Website:** [https://booking.kai.id](https://booking.kai.id)

## Test Flow

```
Login → Search Train → Select Train → Passenger Data → Seat Selection → Payment → Confirmation
```

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Programming language |
| Playwright | Browser automation framework |
| Pytest | Test runner & assertions |
| Page Object Model | Design pattern |
| GitHub Actions | CI/CD pipeline |
| pytest-html | HTML test reports |
| python-dotenv | Environment config |

## Project Structure

```
01-web-automation-playwright/
├── .github/
│   └── workflows/
│       └── test.yml            # CI pipeline (smoke + regression)
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py            # Base class with shared methods
│   ├── login_page.py           # Login page actions
│   ├── home_page.py            # Home/search page actions
│   ├── train_list_page.py      # Train search results
│   ├── passenger_page.py       # Passenger data form
│   ├── seat_page.py            # Seat selection
│   ├── payment_page.py         # Payment page
│   └── confirmation_page.py    # Booking confirmation
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_login.py           # TC-001, TC-002
│   ├── test_search.py          # TC-003
│   ├── test_booking.py         # TC-004, TC-005, TC-006
│   ├── test_validation.py      # TC-007
│   └── test_logout.py          # TC-008
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   └── helpers.py              # Helper functions
├── reports/                    # Generated test reports
├── conftest.py                 # Pytest fixtures & hooks
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── .gitignore
```

## Test Cases

| ID | Test Case | Priority | Module |
|----|-----------|----------|--------|
| TC-001 | Valid Login | High | Login |
| TC-002 | Invalid Login (wrong password, wrong email, empty fields) | High | Login |
| TC-003 | Search Train (valid route, swap stations, no results) | High | Search |
| TC-004 | Select Train (add to booking) | High | Booking |
| TC-005 | Change Train Selection (remove/change) | Medium | Booking |
| TC-006 | Complete Booking/Checkout Flow | High | Booking |
| TC-007 | Required Field Validation (passenger form) | High | Validation |
| TC-008 | Logout (session end, re-login) | Medium | Auth |

## Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/BagasDS009/qa-portfolio.git
cd qa-portfolio/01-web-automation-playwright

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your KAI credentials
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run specific test file
pytest tests/test_login.py

# Run with specific browser
pytest --browser chromium
pytest --browser firefox

# Run headed (visible browser)
pytest --headed

# Run with verbose output
pytest -v --tb=long

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

## CI/CD Pipeline

GitHub Actions workflow runs automatically on:
- **Push** to `main` / `develop` branch
- **Pull Request** to `main`
- **Scheduled** daily at 08:00 WIB (regression)
- **Manual trigger** via workflow_dispatch

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `BASE_URL` | Target URL (https://booking.kai.id) |
| `KAI_USER` | Test account email |
| `KAI_PASSWORD` | Test account password |

## Reports

Test reports are generated automatically:
- **HTML Report:** `reports/report.html`
- **Screenshots on failure:** `reports/screenshots/`
- **CI Artifacts:** Downloadable from GitHub Actions

## Design Decisions

1. **Page Object Model** - Separates page structure from test logic for better maintainability
2. **BasePage class** - Common methods (click, fill, wait) to reduce code duplication
3. **Fixtures** - Reusable test setup (login, test data) via pytest fixtures
4. **Screenshot on failure** - Auto-capture for debugging failed tests
5. **Environment config** - Secrets stored in `.env`, not hardcoded
6. **Multi-browser CI** - Tests run on Chromium & Firefox in parallel

## Author

**Bagas Dimas Saputra** - QA Engineer
