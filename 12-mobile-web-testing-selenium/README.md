# 12 - Mobile Web Testing - Device Emulation (Selenium + Java + Firefox)

![Java](https://img.shields.io/badge/Java-17-red?logo=openjdk)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green?logo=selenium)
![Firefox](https://img.shields.io/badge/Firefox-Headless-FF7139?logo=firefox)
![TestNG](https://img.shields.io/badge/TestNG-7.9-orange)
![Maven](https://img.shields.io/badge/Maven-3+-blue?logo=apachemaven)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)

## Overview

Mobile responsive testing using **Selenium WebDriver Firefox headless** with viewport resizing and user agent override. No physical devices needed — Firefox's responsive design capabilities emulate real device viewports, user agents, touch events, and pixel density.

**Target Application:** [SauceDemo](https://www.saucedemo.com) — a demo e-commerce site for practicing test automation.

## Tech Stack

| Technology | Purpose |
|---|---|
| Java 17 | Programming language |
| Selenium 4.18 | Browser automation with viewport emulation |
| Firefox (Headless) | Browser with responsive design mode |
| TestNG 7.9 | Test framework with DataProvider |
| Maven | Build & dependency management |
| WebDriverManager | Auto browser driver setup |
| Allure 2.25 | Test reporting |

## Emulated Devices

| Device | Viewport | Scale Factor | Platform |
|--------|----------|--------------|----------|
| iPhone 13 | 390 x 844 | 3x | iOS 15 |
| iPhone 14 Pro | 393 x 852 | 3x | iOS 16 |
| Pixel 7 | 412 x 915 | 2.625x | Android 13 |
| Samsung Galaxy S21 | 360 x 800 | 3x | Android 12 |
| iPad Pro 11 | 834 x 1194 | 2x | iPadOS 15 |

## Test Cases

### Responsive Design (5 tests × devices)

| # | Test Case | Devices | Severity |
|---|---|---|---|
| 1 | Login page renders correctly on mobile | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 2 | Page viewport matches device width | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 3 | Touch events are enabled on mobile | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 4 | Login page renders correctly on tablet | iPad Pro | Normal |
| 5 | Tablet viewport is between mobile and desktop | iPad Pro | Normal |

### Mobile Navigation (4 tests × 3 devices)

| # | Test Case | Devices | Severity |
|---|---|---|---|
| 6 | User can login on mobile device | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 7 | Products are scrollable on mobile | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 8 | Add to cart works with touch/tap | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 9 | Hamburger menu works on mobile | iPhone 13, Pixel 7, Galaxy S21 | Normal |

### Mobile Checkout (4 tests × 3 devices)

| # | Test Case | Devices | Severity |
|---|---|---|---|
| 10 | Complete checkout flow on mobile | iPhone 13, Pixel 7, Galaxy S21 | Critical |
| 11 | Cart persists after page refresh | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 12 | Remove item from cart on mobile | iPhone 13, Pixel 7, Galaxy S21 | Normal |
| 13 | Checkout validation - empty fields | iPhone 13, Pixel 7, Galaxy S21 | Normal |

### Orientation & Layout (4 tests)

| # | Test Case | Severity |
|---|---|---|
| 14 | Portrait vs Landscape layout | Normal |
| 15 | Small phone vs Large phone comparison | Minor |
| 16 | Mobile user agent is set correctly | Minor |
| 17 | Device pixel ratio > 1 | Minor |

> **Total parameterized runs:** 13 tests × 3 devices + 2 tablet + 4 orientation = **45 test executions**

## Project Structure

```
12-mobile-web-testing-selenium/
├── src/test/java/com/kai/
│   ├── config/
│   │   └── DeviceConfig.java          # Device profiles (viewport, UA, DPR)
│   └── tests/
│       ├── BaseTest.java              # WebDriver setup with mobile emulation
│       ├── ResponsiveTest.java        # Viewport, rendering, touch tests
│       ├── MobileNavigationTest.java  # Login, scroll, cart, menu flows
│       ├── MobileCheckoutTest.java    # Full checkout, cart persist, validation
│       └── MobileOrientationTest.java # Portrait/landscape, DPR, UA tests
├── src/test/resources/
│   └── testng.xml                     # TestNG suite configuration
├── pom.xml                            # Maven dependencies & build config
├── .gitignore
└── README.md
```

## Setup & Installation

### Prerequisites

- Java 17+ (`brew install openjdk@17`)
- Maven 3+ (`brew install maven`)
- Firefox (`brew install --cask firefox`)

### Installation

```bash
cd 12-mobile-web-testing-selenium
mvn clean install -DskipTests
```

## Running Tests

```bash
# Run all tests
mvn clean test

# Run specific test class
mvn test -Dtest=ResponsiveTest
mvn test -Dtest=MobileNavigationTest
mvn test -Dtest=MobileCheckoutTest
mvn test -Dtest=MobileOrientationTest

# Run with TestNG suite
mvn test -DsuiteXmlFile=src/test/resources/testng.xml
```

## Reports

### Allure Report

```bash
# Generate and serve Allure report
mvn allure:serve

# Or generate report only
mvn allure:report
```

Reports include:
- Test execution per device
- Epic/Feature/Story categorization
- Severity levels
- Step-by-step execution flow
- Screenshot on failure (can be added)

## CI/CD Integration

```yaml
name: Mobile Web Tests (Selenium)
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: browser-actions/setup-firefox@v1
      - run: mvn clean test
        working-directory: 12-mobile-web-testing-selenium
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-results
          path: 12-mobile-web-testing-selenium/target/allure-results/
```

## Key Design Decisions

- **Firefox Headless**: Lightweight, no Chrome dependency, excellent responsive mode support
- **Viewport Resizing + User Agent Override**: Emulates mobile devices via window size and UA string
- **FirefoxProfile Preferences**: `dom.w3c_touch_events.enabled` for touch, `layout.css.devPixelsPerPx` for DPR
- **DataProvider**: TestNG DataProvider enables parameterized testing across multiple devices
- **WebDriverManager**: Automatic GeckoDriver version management
- **Fresh driver per test**: Each test method gets a clean browser instance
- **Allure Steps**: Structured step reporting for debugging
- **No physical devices needed**: All emulation done through Firefox responsive capabilities

## Device Emulation vs Physical Devices

| Aspect | Device Emulation (This Project) | Physical Devices |
|--------|--------------------------------|------------------|
| Setup Cost | Free, no hardware needed | Expensive device lab |
| Speed | Fast, runs in CI/CD | Slow, sequential |
| Device Coverage | Unlimited device profiles | Limited to owned devices |
| Touch Events | Emulated via Chrome | Native touch |
| Rendering Engine | Chromium-based | Native browser engine |
| Best For | Responsive layout, viewport testing | Native gesture accuracy |
| CI/CD Integration | Seamless | Requires BrowserStack/device farm |

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating mobile web testing skills with Selenium + Java device emulation*
