# Test Strategy Document

**Project:** E-Commerce Web Application  
**Author:** Bagas Dimas Saputra  
**Version:** 1.0  
**Last Updated:** August 2026

---

## 1. Purpose

This document defines the overall testing approach, principles, and decision framework for the E-Commerce Web Application. It guides the team on when to use which test type, how to assess risk, and how to allocate effort across the testing pyramid.

---

## 2. Testing Principles

| Principle | Description |
|-----------|-------------|
| Shift-Left | Start testing early — write tests during development, not after |
| Risk-Based | Focus effort where business impact is highest |
| Automation-First | Automate repetitive tests; manual testing for exploratory & UX |
| Fast Feedback | Keep CI pipeline under 15 minutes for core tests |
| Quality Gates | Define clear pass/fail criteria at each stage |

---

## 3. Test Pyramid Strategy

```
         /‾‾‾‾‾‾‾\
        /  Manual   \        ← Exploratory, UAT (5%)
       /  (E2E UI)   \       ← Critical flows only (10%)
      /  Integration   \     ← API tests, contracts (25%)
     /    Unit Tests     \   ← Fast, isolated (60%)
    /______________________\
```

### Allocation Per Layer

| Layer | % of Tests | Speed | Tools | What to Test |
|-------|:----------:|-------|-------|--------------|
| Unit | 60% | <1s each | JUnit, pytest | Business logic, utilities, validators |
| Integration/API | 25% | <5s each | RestAssured, Playwright | Endpoints, DB queries, service communication |
| E2E UI | 10% | 10-30s each | Selenium, Playwright | Critical user journeys (login, checkout, payment) |
| Manual/Exploratory | 5% | Human | Brain + Tools | UX flows, edge cases, new features |

---

## 4. Risk-Based Testing Matrix

### Risk Assessment Criteria

| Factor | Weight | Scale |
|--------|--------|-------|
| Business Impact | 40% | 1-5 (1=low, 5=critical) |
| Frequency of Use | 30% | 1-5 (1=rare, 5=every session) |
| Complexity | 20% | 1-5 (1=simple, 5=complex) |
| Change Frequency | 10% | 1-5 (1=stable, 5=changes often) |

### Feature Risk Scores

| Feature | Impact | Frequency | Complexity | Change | Score | Test Priority |
|---------|:------:|:---------:|:----------:|:------:|:-----:|:-------------:|
| Payment/Checkout | 5 | 4 | 5 | 3 | 4.5 | P0 - Exhaustive |
| Login/Auth | 5 | 5 | 3 | 2 | 4.2 | P0 - Exhaustive |
| Product Search | 3 | 5 | 3 | 3 | 3.6 | P1 - Thorough |
| Cart Management | 4 | 4 | 3 | 2 | 3.6 | P1 - Thorough |
| User Profile | 2 | 2 | 2 | 1 | 1.9 | P2 - Basic |
| Static Pages | 1 | 3 | 1 | 1 | 1.7 | P3 - Smoke only |

### Test Depth Per Priority

| Priority | Unit | API | E2E | Manual | Security | Performance |
|----------|:----:|:---:|:---:|:------:|:--------:|:-----------:|
| P0 | Full | Full | Full | Exploratory | Pen test | Load + Stress |
| P1 | Full | Full | Happy path | Spot check | Scan | Load |
| P2 | Core paths | Core paths | - | On change | - | - |
| P3 | - | - | - | Visual check | - | - |

---

## 5. Test Types & When to Use

| Test Type | Trigger | Duration | Blocker? |
|-----------|---------|----------|----------|
| Smoke Test | Every deploy | <2 min | Yes — rollback if fail |
| Regression Suite | PR merge to main | <15 min | Yes — block release |
| Load Test | Weekly / pre-release | 5-10 min | Warning only |
| Security Scan | Weekly / pre-release | 5-15 min | Fail on critical findings |
| Visual Regression | PR with UI changes | <3 min | Warning only |
| Exploratory Testing | New feature / sprint end | 1-2 hours | No — report findings |
| UAT | Pre-release | 1-2 days | Yes — stakeholder sign-off |

---

## 6. Environment Strategy

| Environment | Purpose | Data | Deploy Frequency |
|-------------|---------|------|-----------------|
| Local/Dev | Unit + integration tests | Mock/seeded | On every commit |
| Staging | Full regression + E2E | Synthetic | On PR merge |
| Pre-production | UAT + performance | Production-like | Pre-release |
| Production | Smoke + monitoring | Real | Post-deploy |

---

## 7. Defect Management

### Severity Classification

| Severity | Definition | SLA | Example |
|----------|-----------|-----|---------|
| S1 - Critical | System unusable, data loss | Fix within 4h | Payment processing crash |
| S2 - Major | Core feature broken, no workaround | Fix within 24h | Cannot add to cart |
| S3 - Minor | Feature works but degraded | Fix within 1 sprint | Slow search response |
| S4 - Trivial | Cosmetic issue | Backlog | Typo in footer |

### Exit Criteria

| Milestone | Criteria |
|-----------|----------|
| Sprint Release | 0 S1, 0 S2, all P0 tests pass |
| Major Release | 0 S1, 0 S2, <3 S3, 95% test pass rate |
| Hotfix | Targeted fix verified, no regression |

---

## 8. Test Data Strategy

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| Factory Pattern | Unit tests | Fast, isolated | Not realistic |
| Seed Scripts | Integration/API | Repeatable, realistic | Setup time |
| Fixtures/JSON | E2E tests | Version controlled | Maintenance |
| Production Clone | Performance/UAT | Most realistic | Privacy concerns, slow |

---

## 9. CI/CD Quality Gates

```
Developer Commit
      │
      ▼
┌─────────────┐
│  Lint/Build │ ← Fail fast on syntax/compile errors
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Unit Tests  │ ← Must pass 100%
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  API Tests  │ ← Must pass 100%
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  E2E Tests  │ ← Must pass 95%+ (flake tolerance)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Security    │ ← No critical/high findings
│ Performance │ ← p95 < threshold
│ Visual      │ ← No unintended diffs
└──────┬──────┘
       │
       ▼
   ✅ Deploy
```

---

## 10. Tools & Framework Selection

| Category | Selected Tool | Alternatives Considered | Rationale |
|----------|--------------|------------------------|-----------|
| Web UI (Python) | Playwright | Selenium, Cypress | Auto-wait, fast, multi-browser |
| Web UI (Java) | Selenium | - | Industry standard, portfolio diversity |
| API (Python) | Playwright API | requests + pytest | Same tool as UI, built-in assertions |
| API (Java) | RestAssured | HttpClient | Fluent API, BDD-style, Allure integration |
| API (JS) | Cypress | Supertest | cy.request() integrates with UI tests |
| Performance | k6 | JMeter, Gatling | Code-first, lightweight, CI-native |
| Security | OWASP ZAP | Burp Suite | Open-source, Docker support, CI-friendly |
| Visual | BackstopJS | Percy, Chromatic | Free, self-hosted, good enough |
| Reporting | Allure | ExtentReports | Multi-framework, GitHub Pages deploy |
| CI/CD | GitHub Actions | Jenkins, GitLab CI | Native to GitHub, free for open-source |

---

## 11. Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Coverage (code) | >80% unit, >60% integration | SonarQube / coverage tools |
| Test Pass Rate | >95% per run | CI dashboard |
| Defect Escape Rate | <5% to production | Prod bugs / total bugs found |
| Mean Time to Detect (MTTD) | <1 hour | Time from deploy to test failure |
| Flaky Test Rate | <2% | Tests that pass/fail inconsistently |
| CI Pipeline Duration | <15 min (core), <30 min (full) | Workflow duration |

---

## 12. Continuous Improvement

- **Sprint Retrospective**: Review test failures, missed defects, flaky tests
- **Monthly Audit**: Check coverage gaps, outdated tests, unmaintained fixtures
- **Quarterly Review**: Reassess risk matrix, update strategy if features change
- **Automation Debt**: Track manual tests that should be automated (target: move 5 per sprint)

---

*This document is a living artifact. Review and update quarterly or when major architectural changes occur.*
