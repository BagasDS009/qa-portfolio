# 08 - API Automation Testing with Cypress

![Cypress](https://img.shields.io/badge/Cypress-13.x-17202C?logo=cypress)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
![Allure](https://img.shields.io/badge/Allure-Report-orange)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

API automation testing project targeting **FakeREST API** ([fakerestapi.azurewebsites.net](https://fakerestapi.azurewebsites.net/api/v1)) using **Cypress**. This project covers full CRUD operations across 4 API modules with 22 comprehensive test cases.

## Tech Stack

| Technology | Purpose |
|---|---|
| Cypress 13.x | Test automation framework |
| JavaScript (ES6+) | Programming language |
| cy.request() | HTTP API testing |
| Allure Reporter | Test reporting |
| Cypress Fixtures | Test data management |

## Test Cases

### Activities API (6 tests)

| # | Test Case | Method | Endpoint | Expected |
|---|---|---|---|---|
| 1 | Get all activities | GET | /Activities | 200, array |
| 2 | Get activity by ID | GET | /Activities/1 | 200, has id/title/dueDate |
| 3 | Non-existent activity | GET | /Activities/99999 | 404 |
| 4 | Create new activity | POST | /Activities | 200, body matches |
| 5 | Update activity | PUT | /Activities/{id} | 200, updated fields |
| 6 | Delete activity | DELETE | /Activities/{id} | 200 |

### Authors API (7 tests)

| # | Test Case | Method | Endpoint | Expected |
|---|---|---|---|---|
| 1 | Get all authors | GET | /Authors | 200, array |
| 2 | Get author by ID | GET | /Authors/1 | 200, has id/firstName/lastName |
| 3 | Get authors by book | GET | /Authors/authors/books/1 | 200, array |
| 4 | Non-existent author | GET | /Authors/99999 | 404 |
| 5 | Create new author | POST | /Authors | 200, body matches |
| 6 | Update author | PUT | /Authors/{id} | 200, updated fields |
| 7 | Delete author | DELETE | /Authors/{id} | 200 |

### Books API (6 tests)

| # | Test Case | Method | Endpoint | Expected |
|---|---|---|---|---|
| 1 | Get all books | GET | /Books | 200, array |
| 2 | Get book by ID | GET | /Books/1 | 200, has id/title/pageCount |
| 3 | Non-existent book | GET | /Books/99999 | 404 |
| 4 | Create new book | POST | /Books | 200, body matches |
| 5 | Update book | PUT | /Books/{id} | 200, updated fields |
| 6 | Delete book | DELETE | /Books/{id} | 200 |

### Users API (6 tests)

| # | Test Case | Method | Endpoint | Expected |
|---|---|---|---|---|
| 1 | Get all users | GET | /Users | 200, array |
| 2 | Get user by ID | GET | /Users/1 | 200, has id/userName/password |
| 3 | Non-existent user | GET | /Users/99999 | 404 |
| 4 | Create new user | POST | /Users | 200, body matches |
| 5 | Update user | PUT | /Users/{id} | 200, updated fields |
| 6 | Delete user | DELETE | /Users/{id} | 200 |

## Test Execution Summary

```
  Activities API - CRUD
    ✓ GET - Get all activities
    ✓ GET - Get activity by ID
    ✓ GET - Non-existent activity returns 404
    ✓ POST - Create a new activity
    ✓ PUT - Update an existing activity
    ✓ DELETE - Delete an activity

  Authors API - CRUD
    ✓ GET - Get all authors
    ✓ GET - Get author by ID
    ✓ GET - Get authors by book ID
    ✓ GET - Non-existent author returns 404
    ✓ POST - Create a new author
    ✓ PUT - Update an existing author
    ✓ DELETE - Delete an author

  Books API - CRUD
    ✓ GET - Get all books
    ✓ GET - Get book by ID
    ✓ GET - Non-existent book returns 404
    ✓ POST - Create a new book
    ✓ PUT - Update an existing book
    ✓ DELETE - Delete a book

  Users API - CRUD
    ✓ GET - Get all users
    ✓ GET - Get user by ID
    ✓ GET - Non-existent user returns 404
    ✓ POST - Create a new user
    ✓ PUT - Update an existing user
    ✓ DELETE - Delete a user

  25 passing
```

## Project Structure

```
08-api-test-cypress/
├── cypress/
│   ├── e2e/
│   │   ├── activities.cy.js      # Activities CRUD tests
│   │   ├── authors.cy.js         # Authors CRUD tests
│   │   ├── books.cy.js           # Books CRUD tests
│   │   └── users.cy.js           # Users CRUD tests
│   ├── fixtures/
│   │   └── testData.json          # Test data for all endpoints
│   └── support/
│       ├── commands.js            # Custom commands & plugins
│       └── e2e.js                 # Support file
├── cypress.config.js              # Cypress configuration
├── package.json                   # Dependencies & scripts
├── .gitignore
└── README.md
```

## Setup & Installation

### Prerequisites

- Node.js 16+ installed
- npm or yarn

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd 08-api-test-cypress

# Install dependencies
npm install
```

## Running Tests

```bash
# Run all tests (headless)
npm test

# Run specific module
npm run test:activities
npm run test:authors
npm run test:books
npm run test:users

# Open Cypress Test Runner (interactive)
npm run test:open

# Generate Allure report
npm run report
```

## Reports

### Allure Report

```bash
# Generate and serve Allure report
npm run report
```

Reports include:
- Test execution timeline
- Request/Response details
- Pass/Fail status per endpoint
- Execution duration metrics

## CI/CD Integration

This project is CI-ready and can be integrated with GitHub Actions:

```yaml
name: API Tests
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm install
      - run: npm test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-results
          path: allure-results/
```

## Key Design Decisions

- **cy.request()**: Direct HTTP requests without browser overhead for faster API testing
- **Fixtures**: Centralized test data management
- **failOnStatusCode: false**: Allows testing negative scenarios (404, 400)
- **Allure Integration**: Detailed reporting with request/response logging

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating API automation testing skills with Cypress*
