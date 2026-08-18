# Prompt Guide — API Test Generator Agent

Panduan cara menggunakan agent ini untuk generate API automation testing.

---

## Quick Start

```
Generate API test suite lengkap untuk https://reqres.in/api
Cover: users CRUD, auth, contract validation, negative cases, performance.
```

---

## Contoh Prompt per Skill

### Skill 0 — API Strategy
```
Buat test strategy untuk API di https://petstore.swagger.io/v2
Business context: pet store management — CRUD pets, orders, users.
```

### Skill 1 — Analyze API
```
Analisis API di https://reqres.in/api
Fetch swagger/docs, list semua endpoints, request/response schema, auth requirement.
```

### Skill 2 — Generate Test Cases
```
Generate test case untuk https://jsonplaceholder.typicode.com
Cover: posts CRUD, users, comments. Include negative + security + contract.
```

### Skill 3 — Generate Automation
```
Generate automation code lengkap untuk https://reqres.in/api
Output: base_client, fixtures, test files, schemas, allure config.
```

### Skill 4 — Contract Testing
```
Generate contract tests (schema validation) untuk semua endpoints di https://reqres.in/api
Pastikan response selalu match schema, detect breaking changes.
```

### Skill 5 — Security Testing
```
Generate security tests (OWASP API Top 10) untuk https://reqres.in/api
Test: auth bypass, IDOR, injection, mass assignment, rate limiting.
```

### Skill 6 — Performance Testing
```
Generate performance tests untuk https://reqres.in/api
Budget: GET < 500ms, POST < 1500ms. Test concurrent requests (10 parallel).
```

### Skill 7 — Fix
```
@7-refactor-and-fix.md fix this #Terminal
@7-refactor-and-fix.md --fix-all
```

---

## Output Location

```
output/
├── reqres/                  ← dari reqres.in
├── petstore/                ← dari petstore.swagger.io
└── jsonplaceholder/          ← dari jsonplaceholder.typicode.com
```

## Execution

```bash
cd output/[api-name]/automation
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install allure

# Run + auto-report
pytest -v
pytest -m smoke -v
pytest -m contract -v
pytest -m security -v
```
