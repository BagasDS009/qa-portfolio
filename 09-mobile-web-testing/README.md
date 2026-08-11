# Mobile Web Testing - Device Emulation (Playwright)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.49+-2EAD33?logo=playwright&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B35?logo=allure&logoColor=white)

## Overview

Testing mobile responsive behavior using **Playwright device emulation**. No physical devices needed — Playwright emulates real device viewports, user agents, touch events, and pixel density directly in the browser.

**Target Application:** [SauceDemo](https://www.saucedemo.com) — a demo e-commerce site for practicing test automation.

## Emulated Devices

| Device | Viewport | Scale Factor | Platform |
|--------|----------|--------------|----------|
| iPhone 13 | 390 x 844 | 3x | iOS 15 |
| iPhone 14 Pro | 393 x 852 | 3x | iOS 16 |
| Pixel 7 | 412 x 915 | 2.625x | Android 13 |
| Samsung Galaxy S21 | 360 x 800 | 3x | Android 12 |
| iPad Pro 11 | 834 x 1194 | 2x | iPadOS 15 |

## Test Cases

| # | Test | Category | Devices | Priority |
|---|------|----------|---------|----------|
| 1 | Login page renders correctly on mobile | Responsive | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 2 | Page viewport matches device width | Responsive | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 3 | Touch events are enabled on mobile | Responsive | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 4 | Login page renders correctly on tablet | Responsive | iPad Pro | Normal |
| 5 | Tablet viewport is between mobile and desktop | Responsive | iPad Pro | Normal |
| 6 | User can login on mobile device | Navigation | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 7 | Products are scrollable on mobile | Navigation | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 8 | Add to cart works with touch/tap | Navigation | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 9 | Hamburger menu works on mobile | Navigation | iPhone 13, Pixel 7, Galaxy S21 | Normal |

> **Total parameterized runs:** 9 tests × 3 mobile devices + 2 tablet tests = **29 test executions**

## Project Structure

```
09-mobile-web-testing/
├── tests/
│   ├── __init__.py
│   ├── test_responsive.py        # Viewport, rendering, touch emulation
│   └── test_mobile_navigation.py # Login, scroll, cart, menu flows
├── conftest.py                   # Device configs & fixtures
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Dependencies
├── .gitignore
└── README.md
```

## Setup & Run

### Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Run Tests

```bash
# Run all mobile tests
pytest -m mobile

# Run tablet tests only
pytest -m tablet

# Run all tests (mobile + tablet)
pytest

# Run with HTML report
pytest --html=reports/report.html --self-contained-html
```

### Generate Allure Report

```bash
pytest
allure serve reports/allure-results
```

## Key Approach: Device Emulation vs Physical Devices

| Aspect | Device Emulation (This Project) | Physical Devices |
|--------|--------------------------------|------------------|
| Setup Cost | Free, no hardware needed | Expensive device lab |
| Speed | Fast, runs in CI/CD | Slow, sequential |
| Device Coverage | Unlimited device profiles | Limited to owned devices |
| Touch Events | Emulated via Playwright | Native touch |
| Rendering Engine | Chromium-based | Native browser engine |
| Network Conditions | Can throttle programmatically | Real network |
| Best For | Responsive layout, viewport testing | Native gesture accuracy |
| CI/CD Integration | Seamless | Requires device farm (BrowserStack, etc.) |

## What This Proves

- Ability to test mobile responsive behavior without physical devices
- Proficiency with Playwright's device emulation API
- Understanding of mobile-specific interactions (touch, tap, scroll)
- Parameterized testing across multiple device profiles
- Viewport and responsive design validation

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** Pytest + Playwright
- **Reporting:** Allure + pytest-html
- **Devices:** Emulated via Playwright (Chromium)

## Author

**Bagas Dimas Saputra**
