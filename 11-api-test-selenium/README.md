# 11 - API Automation Testing with Java (RestAssured + TestNG)

![Java](https://img.shields.io/badge/Java-17-red?logo=openjdk)
![RestAssured](https://img.shields.io/badge/RestAssured-5.4-green)
![TestNG](https://img.shields.io/badge/TestNG-7.9-orange)
![Maven](https://img.shields.io/badge/Maven-3+-blue?logo=apachemaven)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)

## Overview

API automation testing project targeting **FakeREST API** ([fakerestapi.azurewebsites.net](https://fakerestapi.azurewebsites.net/api/v1)) using **Java + RestAssured + TestNG**. This project covers full CRUD operations across 4 API modules with 25 comprehensive test cases.

## Tech Stack

| Technology | Purpose |
|---|---|
| Java 17 | Programming language |
| RestAssured 5.4 | HTTP API testing library |
| TestNG 7.9 | Test framework |
| Maven | Build & dependency management |
| Jackson | JSON data parsing |
| Allure 2.25 | Test reporting |

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
  Activities API Tests
    ✓ GET - Get all activities
    ✓ GET - Get activity by ID
    ✓ GET - Non-existent activity returns 404
    ✓ POST - Create a new activity
    ✓ PUT - Update an existing activity
    ✓ DELETE - Delete an activity

  Authors API Tests
    ✓ GET - Get all authors
    ✓ GET - Get author by ID
    ✓ GET - Get authors by book ID
    ✓ GET - Non-existent author returns 404
    ✓ POST - Create a new author
    ✓ PUT - Update an existing author
    ✓ DELETE - Delete an author

  Books API Tests
    ✓ GET - Get all books
    ✓ GET - Get book by ID
    ✓ GET - Non-existent book returns 404
    ✓ POST - Create a new book
    ✓ PUT - Update an existing book
    ✓ DELETE - Delete a book

  Users API Tests
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
11-api-test-selenium/
├── src/test/java/com/kai/tests/
│   ├── BaseTest.java              # RestAssured config & test data loader
│   ├── ActivitiesTest.java        # Activities CRUD tests
│   ├── AuthorsTest.java           # Authors CRUD tests
│   ├── BooksTest.java             # Books CRUD tests
│   └── UsersTest.java             # Users CRUD tests
├── src/test/resources/
│   ├── testData.json              # Test data for all endpoints
│   └── testng.xml                 # TestNG suite configuration
├── pom.xml                        # Maven dependencies & build config
├── .gitignore
└── README.md
```

## Setup & Installation

### Prerequisites

- Java 17+ (`brew install openjdk@17`)
- Maven 3+ (`brew install maven`)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd 11-api-test-selenium

# Install dependencies
mvn clean install -DskipTests
```

## Running Tests

```bash
# Run all tests
mvn clean test

# Run specific test class
mvn test -Dtest=ActivitiesTest
mvn test -Dtest=AuthorsTest
mvn test -Dtest=BooksTest
mvn test -Dtest=UsersTest

# Run with specific TestNG suite
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
- Test execution timeline
- Request/Response details (logged via AllureRestAssured filter)
- Pass/Fail status per endpoint
- Epic/Feature/Story categorization
- Severity levels

## CI/CD Integration

This project is CI-ready and can be integrated with GitHub Actions:

```yaml
name: API Tests (Java)
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
      - run: mvn clean test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-results
          path: target/allure-results/
```

## Key Design Decisions

- **RestAssured**: Industry-standard Java library for API testing with fluent BDD-style syntax
- **TestNG**: Flexible test framework with priorities, groups, and parallel execution support
- **Jackson ObjectMapper**: Type-safe JSON test data loading from external file
- **Allure RestAssured Filter**: Automatic request/response logging in reports
- **RequestSpecification**: Centralized request configuration (base URL, content type, filters)
- **Priority ordering**: Tests run in logical CRUD order (GET → POST → PUT → DELETE)

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating API automation testing skills with Java + RestAssured*
