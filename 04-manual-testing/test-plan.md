# Test Plan

## 1. Introduction
This document describes the test plan for the E-Commerce Web Application.

## 2. Scope

### In Scope
- User Registration & Login
- Product Search & Browsing
- Shopping Cart Management
- Checkout & Payment
- Order History

### Out of Scope
- Third-party payment gateway internals
- Mobile native applications

## 3. Test Strategy

| Test Type | Tool | Environment |
|-----------|------|-------------|
| Functional | Manual | Staging |
| Regression | Manual + Automated | Staging |
| Smoke | Manual | Production |
| UAT | Manual | Pre-production |

## 4. Entry Criteria
- Build deployed to staging environment
- Test data prepared
- All P1 bugs from previous build are fixed

## 5. Exit Criteria
- All planned test cases executed
- No open P1/P2 bugs
- Test pass rate >= 95%

## 6. Schedule

| Phase | Start | End |
|-------|-------|-----|
| Test Planning | Week 1 | Week 1 |
| Test Case Design | Week 2 | Week 2 |
| Test Execution | Week 3 | Week 4 |
| Bug Fix Verification | Week 4 | Week 5 |
| Sign-off | Week 5 | Week 5 |

## 7. Resources
- QA Lead: 1
- QA Engineers: 2
- Test Environment: Staging server

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Delayed build delivery | High | Prioritize critical test cases |
| Incomplete requirements | Medium | Early review sessions with BA |
| Environment instability | High | Backup test environment |
