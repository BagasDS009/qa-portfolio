# 02 - API Testing (Postman + Newman)

## Overview
API testing using Postman collections with automated execution via Newman.

## Tech Stack
- Postman
- Newman (CLI runner)
- JavaScript (test scripts)

## Project Structure
```
02-api-testing-postman/
├── collection.json      # Postman collection with requests & tests
├── environment.json     # Environment variables
└── test-report/         # Newman HTML reports
```

## How to Run
```bash
npm install -g newman newman-reporter-htmlextra
newman run collection.json -e environment.json -r htmlextra --reporter-htmlextra-export test-report/report.html
```

## Test Coverage
- User CRUD operations
- Authentication endpoints
- Error handling & status codes
- Response schema validation
