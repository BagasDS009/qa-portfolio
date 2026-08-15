# 18 - Web Automation with Playwright (Python)

E2E test automation framework for [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com) using **Playwright + Python + Pytest**.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Browser Automation | Playwright |
| Test Framework | Pytest + pytest-playwright |
| Reporting | Allure |
| Design Pattern | Page Object Model (POM) |
| Config | python-dotenv |

## Project Structure

```
18-web-automation-playwright/
├── conftest.py                    # Shared fixtures (browser, auth, reporting)
├── pytest.ini                     # Pytest configuration & markers
├── requirements.txt               # Python dependencies
├── .env                           # Environment config (not committed)
├── .gitignore
├── pages/                         # Page Object Model layer
│   ├── base_page.py               # Base class with common methods
│   ├── home_page.py               # Product grid, search, filter, sort
│   ├── login_page.py              # Login form
│   ├── register_page.py           # Registration form
│   ├── product_detail_page.py     # Product detail + add to cart
│   ├── cart_page.py               # Shopping cart operations
│   ├── checkout_page.py           # Multi-step checkout
│   └── contact_page.py            # Contact form
├── tests/                         # Test cases
│   ├── test_data.py               # Centralized test data
│   ├── test_login.py              # TC-001, TC-002: Authentication
│   ├── test_products.py           # TC-003: Product browsing & search
│   ├── test_cart.py               # TC-004: Cart operations
│   ├── test_checkout.py           # TC-005: E2E checkout flow
│   └── test_contact.py            # TC-006: Contact form
├── utils/                         # Utilities
│   ├── config.py                  # Config class (reads .env)
│   └── helpers.py                 # Helper functions
└── reports/                       # Generated reports
    ├── allure-results/
    └── screenshots/
```

## Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run specific test file
pytest tests/test_login.py

# Run with headed browser (visible)
HEADLESS=false pytest

# Run specific marker
pytest -m "cart or checkout"
```

## Reporting

```bash
# Generate and open Allure report
allure serve reports/allure-results

# Or generate static report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Test Accounts (Pre-registered)

| Role | Email | Password |
|------|-------|----------|
| Customer | customer@practicesoftwaretesting.com | welcome01 |
| Admin | admin@practicesoftwaretesting.com | welcome01 |

## Test Coverage

| ID | Area | Tests |
|----|------|-------|
| TC-001 | Valid Login | 1 |
| TC-002 | Invalid Login | 3 |
| TC-003 | Product Search/Sort | 6 |
| TC-004 | Cart Operations | 4 |
| TC-005 | Checkout Flow | 2 |
| TC-006 | Contact Form | 3 |
| **Total** | | **19 tests** |
