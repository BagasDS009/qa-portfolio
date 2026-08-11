# Web Automation - Automation Exercise (Selenium + Java)

![Java](https://img.shields.io/badge/Java-17-red?logo=openjdk)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green?logo=selenium)
![TestNG](https://img.shields.io/badge/TestNG-7.9-orange)
![Maven](https://img.shields.io/badge/Maven-3+-blue?logo=apachemaven)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)

## Overview

E-commerce web automation testing for **automationexercise.com** using Selenium WebDriver + Java with TestNG, Page Object Model, and Allure reporting.

**Target Website:** [https://automationexercise.com](https://automationexercise.com)

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Java 17 | Programming language |
| Selenium 4.18 | Browser automation |
| TestNG 7.9 | Test framework |
| Maven | Build & dependency management |
| WebDriverManager | Auto browser driver setup |
| Allure | Test reporting |
| Firefox | Browser (via GeckoDriver) |

## Test Cases (7 Total)

### Login & Signup (LoginTest.java)

| Test | Description | Severity |
|------|-------------|----------|
| TC-03 | Login with incorrect credentials → error shown | Critical |
| TC-05 | Signup with existing email → error shown | Critical |
| TC-04 | Verify Login & Signup forms visible | Normal |

### Products & Search (SearchTest.java)

| Test | Description | Severity |
|------|-------------|----------|
| TC-01 | Home page is visible | Blocker |
| TC-08 | All Products + product detail page | Critical |
| TC-09 | Search product ("Tshirt") | Critical |
| TC-10 | Subscription in home page | Normal |

## Project Structure

```
10-web-automation-selenium/
├── src/main/java/com/kai/pages/
│   ├── BasePage.java           # Base class (wait, click, type, isVisible)
│   ├── HomePage.java           # Home page actions
│   ├── LoginPage.java          # Login/Signup page
│   └── ProductsPage.java       # Products & search page
├── src/test/java/com/kai/tests/
│   ├── BaseTest.java           # WebDriver setup/teardown (Firefox)
│   ├── LoginTest.java          # Authentication tests
│   └── SearchTest.java         # Products & search tests
├── src/test/resources/
│   └── testng.xml              # TestNG suite config
├── pom.xml                     # Maven dependencies
├── .gitignore
└── README.md
```

## Setup & Run

### Prerequisites
- Java 17+ (`brew install openjdk@17`)
- Maven 3+ (`brew install maven`)
- Firefox (`brew install --cask firefox`)

### Run Tests

```bash
cd 10-web-automation-selenium
mvn clean test
```

### View Allure Report

```bash
allure serve target/allure-results
```

## Key Design Decisions

1. **Page Object Model** — Clean separation of page actions and test logic
2. **CSS + XPath selectors** — `data-qa` attributes when available, XPath for text matching
3. **Firefox** — Lightweight, no extra Chrome install needed
4. **Fresh browser per test** — `@BeforeMethod` creates new driver, `@AfterMethod` quits
5. **No WAF issues** — automationexercise.com is automation-friendly (no Cloudflare)
6. **Allure integration** — `@Step`, `@Epic`, `@Feature`, `@Story`, `@Severity`

## Author

**Bagas Dimas Saputra** - QA Engineer


## Known Limitations

- **CI (GitHub Actions):** automationexercise.com shows Google Consent/Ads overlay in headless mode on datacenter IPs, blocking page content from loading. Tests pass locally but fail in CI.
- **Local execution:** All 16 tests pass with headed Firefox on residential IP
- Google Ads iframes handled via `dismissAds()` method, but consent popup before page load cannot be bypassed in headless

| Environment | Result |
|-------------|--------|
| Local (Mac, headed) | All pass |
| GitHub Actions (headless) | Partial fail (consent overlay) |
