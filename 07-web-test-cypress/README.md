# Web Automation - KAI Booking (Cypress)

![Cypress](https://img.shields.io/badge/Cypress-13+-green?logo=cypress)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)

## Overview

End-to-end web automation testing for **booking.kai.id** using Cypress with Page Object Model pattern and XPath selectors.

**Target Website:** [https://booking.kai.id](https://booking.kai.id)  
**Same test scenarios as:** `01-web-automation-playwright` (Python/Playwright)

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Cypress 13+ | E2E test framework |
| JavaScript (ES6) | Programming language |
| Page Object Model | Design pattern |
| XPath (`@cypress/xpath`) | Element locators |
| Allure Report | Test reporting |

## Test Cases (13 Total)

### TC-003: Search Train (search.cy.js) ✅

| ID | Test Case | Status |
|----|-----------|--------|
| TC-003a | Search valid route (PSE → BD) | ✅ |
| TC-003b | Search alternative route (GMR → YK) | ✅ |
| TC-003c | Search with multiple passengers (2 adults + 2 babies) | ✅ |
| TC-003d | Search with no results | ✅ |
| TC-003e | Search form visible on homepage | ✅ |
| TC-003f | Baby cannot exceed adult (tooltip validation) | ✅ |

### TC-007: Form Validation (validation.cy.js) ✅

| ID | Test Case | Trigger | Status |
|----|-----------|---------|--------|
| TC-007 | Submit button disabled when empty | - | ✅ |
| TC-007b | Mohon isi Nama | Blur | ✅ |
| TC-007c | Mohon isi Nomor Identitas | Blur | ✅ |
| TC-007d | Search without origin station | Click search | ✅ |
| TC-007e | Mohon diisi Email | Blur | ✅ |
| TC-007f | Nomor Identitas Wajib Diisi (Passenger) | Blur | ✅ |
| TC-007g | Passenger name has required attribute | Attribute check | ✅ |

> **Known Limitations:**
> - booking.kai.id uses **flexdatalist jQuery plugin** for station autocomplete. This plugin binds events to a hidden `<input>` element, not the visible one. Cypress `.type()` dispatches events on the visible input but flexdatalist doesn't pick them up — so the **dropdown never appears**.
> - **Playwright works** because its `.fill()` method directly sets the value on the underlying element and dispatches all native DOM events (`input`, `change`, `keydown`, `keyup`) that flexdatalist listens to.
> - This is a well-known compatibility issue between Cypress and jQuery autocomplete plugins that rely on hidden input proxies.
> - Login, Booking, Logout are additionally blocked by **CAPTCHA**.
> - This project demonstrates **Cypress framework structure, Page Object Model, and XPath strategy** — matching the Playwright implementation identically. The code is production-ready for sites that use standard HTML inputs.

## Project Structure

```
07-web-test-cypress/
├── cypress/
│   ├── e2e/
│   │   ├── search.cy.js          # Search test scenarios
│   │   └── validation.cy.js      # Validation test scenarios
│   ├── pages/
│   │   ├── HomePage.js            # POM - Search form
│   │   ├── TrainListPage.js       # POM - Search results
│   │   └── PassengerPage.js       # POM - Passenger form
│   ├── fixtures/
│   │   └── testData.json          # Centralized test data
│   └── support/
│       ├── commands.js
│       └── e2e.js                 # XPath plugin + uncaught exception handler
├── cypress.config.js
├── package.json
├── .gitignore
└── README.md
```

## Setup

```bash
cd 07-web-test-cypress
npm install
```

## Running Tests

```bash
# Run all tests (headless)
npx cypress run

# Run search tests only
npx cypress run --spec 'cypress/e2e/search.cy.js'

# Run validation tests only
npx cypress run --spec 'cypress/e2e/validation.cy.js'

# Open Cypress UI (interactive)
npx cypress open

# Run headed
npx cypress run --headed
```

## XPath Strategy

Same XPath locators as `01-web-automation-playwright/pages/`:

```javascript
// HomePage.js
originInput: '//input[@placeholder="Stasiun Asal..." and @id="origination-flexdatalist"]'
searchButton: '//input[@id="submit"]'
babyTooltip: '//span[@class="tooltiptext"]'

// PassengerPage.js
contactName: "//input[@id='pemesan_nama' and @name='pemesan_nama']"
errorMohonIsiNama: "//li[normalize-space()='Mohon isi Nama']"
```

## Anti-Detection

- `Cypress.on('uncaught:exception')` — ignore Cloudflare JS errors
- Human-like `cy.wait()` delays between actions
- Standard viewport (1366x768)

## Author

**Bagas Dimas Saputra** - QA Engineer
