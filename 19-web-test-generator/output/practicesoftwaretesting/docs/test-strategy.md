# Test Strategy — Practice Software Testing (Toolshop)

## Application Overview

- **URL**: https://practicesoftwaretesting.com (Sprint 5)
- **Alt URL**: https://testsmith-io.github.io/practice-software-testing/#/
- **Type**: E-commerce (tool shop) — practice application by TestSmith.io
- **Stack**: Angular SPA (frontend) + REST API backend
- **API Docs**: https://api.practicesoftwaretesting.com/api/documentation (Swagger)
- **Users**: Public practice app — multiple concurrent testers (shared database)
- **Business Context**: Full e-commerce flow — browse products, add to cart, checkout with multiple payment methods. Revenue simulation via checkout pipeline.

## Default Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@practicesoftwaretesting.com | welcome01 |
| Customer 1 | customer@practicesoftwaretesting.com | welcome01 |
| Customer 2 | customer2@practicesoftwaretesting.com | welcome01 |

> Note: Database is shared across all users of the practice site. Do not use real personal information.

---

## Application Feature Map

| # | Feature | Page/Route | Description |
|---|---------|-----------|-------------|
| 1 | Homepage / Product Listing | `/` | Browse all products, filter, sort, search |
| 2 | Product Detail | `/product/{id}` | View product info, add to cart, related products |
| 3 | Search & Filter | `/` (sidebar + search bar) | Category filter, brand filter, price range, sort, keyword search |
| 4 | Shopping Cart | `/checkout` | View cart, update quantity, remove items, proceed to checkout |
| 5 | Checkout Flow | `/checkout` (multi-step) | Address → Payment → Confirmation |
| 6 | User Login | `/auth/login` | Email + password authentication, token-based |
| 7 | User Registration | `/auth/register` | Full registration form with validation |
| 8 | User Profile | `/account` | View/edit profile, view orders, view invoices |
| 9 | Contact Form | `/contact` | Submit support message (subject, message, attachment) |
| 10 | Admin Dashboard | `/admin/dashboard` | Reports, user management, product management, brand/category management |
| 11 | Favorites/Wishlist | `/account/favorites` | Add/remove favorite products |
| 12 | Invoices | `/account/invoices` | View past order invoices |
| 13 | Messages | `/account/messages` | View contact form messages (admin) |

---

## Risk Assessment Matrix

| # | Feature | Business Impact (40%) | Usage Frequency (25%) | Complexity (20%) | Change Velocity (15%) | **Risk Score** | **Coverage Level** |
|---|---------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1 | Checkout Flow | 5 | 5 | 5 | 3 | **4.70** | Exhaustive |
| 2 | Shopping Cart | 5 | 5 | 4 | 3 | **4.50** | Exhaustive |
| 3 | User Login | 5 | 5 | 2 | 2 | **3.90** | Thorough |
| 4 | Product Listing + Search | 4 | 5 | 3 | 3 | **3.90** | Thorough |
| 5 | User Registration | 4 | 3 | 3 | 2 | **3.25** | Thorough |
| 6 | Product Detail | 3 | 4 | 2 | 2 | **2.90** | Standard |
| 7 | User Profile | 3 | 3 | 2 | 2 | **2.65** | Standard |
| 8 | Contact Form | 2 | 2 | 2 | 1 | **1.85** | Minimal |
| 9 | Favorites | 2 | 2 | 1 | 1 | **1.65** | Minimal |
| 10 | Admin Dashboard | 4 | 2 | 4 | 2 | **3.20** | Thorough |
| 11 | Invoices | 2 | 2 | 1 | 1 | **1.65** | Minimal |

### Coverage Level Definitions

| Risk Score | Level | Depth |
|------------|-------|-------|
| 4.0 - 5.0 | **Exhaustive** | All positive + all negative + edge + performance + a11y + visual + API |
| 3.0 - 3.9 | **Thorough** | Happy path + key negative + boundary + a11y |
| 2.0 - 2.9 | **Standard** | Happy path + critical negative only |
| 1.0 - 1.9 | **Minimal** | Single smoke test (happy path) |

---

## Automation Scope

### In Scope (Automate) — High ROI

| Feature | Justification |
|---------|---------------|
| Login | Stable UI, fast execution, gates all authenticated flows |
| Registration | Form validation rules provide excellent negative test variety |
| Product Search & Filter | Multiple combinations, easily parametrized |
| Add to Cart | Core revenue flow, multiple product types |
| Checkout (address + payment) | Most complex flow, highest business impact |
| Cart Management | Quantity update, remove, price calculation |

### In Scope (Automate) — Medium ROI

| Feature | Justification |
|---------|---------------|
| Product Detail | Related products, add to cart from detail |
| User Profile | Edit profile, view orders |
| Contact Form | Simple form validation |
| Admin Dashboard | Report data validation (admin-only) |

### Out of Scope / Limitations

| Feature | Reason | Recommendation |
|---------|--------|----------------|
| Image Upload (messages) | File upload UI — medium complexity | Automate with Playwright `set_input_files()` |
| Shared Database | Other users may modify data during test | Use unique data per run, assert on own data only |
| Real Payment | No real gateway — simulated | Test form submission + API mock only |
| Email Verification | No email service | Skip — mock if needed |

### Mock Required

| Scenario | Mock Strategy |
|----------|---------------|
| Payment failure | Intercept `/payment` endpoint → return 422/500 |
| Slow server response | Route delay on `/products` → test loading state |
| Network offline | `page.context.set_offline(True)` during checkout |
| API 500 errors | Mock any endpoint → verify friendly error in UI |

---

## Test Distribution (Test Pyramid)

| Layer | Count (Est.) | Percentage | Features |
|-------|:-----:|:-----:|---------|
| E2E UI (Functional) | 45 | 50% | Login, Register, Search, Cart, Checkout, Profile |
| API Intercept | 15 | 17% | Login payload, Cart API, Checkout API, Error handling |
| Accessibility | 12 | 13% | All critical pages (axe scan + keyboard nav) |
| Visual Regression | 10 | 11% | Homepage, Login, Product, Cart, Checkout (3 viewports) |
| Performance | 8 | 9% | Page load, API budgets, Web Vitals |
| **Total** | **~90** | 100% | |

---

## Execution Plan

| Suite | Tests | Trigger | Time Budget | Scope |
|-------|:-----:|---------|:-----------:|-------|
| **Smoke** | 8 | Every PR / commit | < 3 min | Login + Add to Cart + Checkout happy path |
| **Regression** | 55 | Nightly | < 15 min | All functional + API intercept |
| **Full** | 90 | Pre-release / Weekly | < 30 min | Regression + a11y + visual + performance |

### Smoke Suite Composition (8 tests)

1. Homepage loads with products visible
2. Login with valid credentials
3. Search product returns results
4. Add product to cart
5. Cart shows correct item & price
6. Checkout complete (bank transfer)
7. Logout successful
8. Registration happy path

---

## Quality Gates

```
RELEASE BLOCKED if:
  ✗ Any smoke test fails
  ✗ Any CRITICAL-severity test fails
  ✗ > 10% of regression tests fail
  ✗ Accessibility score < 85 on any critical page
  ✗ LCP > 3.0s on homepage or product listing
  ✗ Visual diff > 0.5% on checkout flow pages

RELEASE WARNING if:
  ⚠ Any NORMAL-severity test fails
  ⚠ New a11y violations introduced (moderate+)
  ⚠ CLS > 0.1 on any page
  ⚠ API response > 2s on any endpoint
  ⚠ Test execution time increased > 30% vs last run
```

---

## Browser & Device Matrix

| Browser | Desktop (1366x768) | Tablet (768x1024) | Mobile (375x812) | Priority |
|---------|:-----:|:-----:|:-----:|:-----:|
| Firefox | Yes | Yes | Yes | P1 (default) |
| Chromium | Yes | No | No | P2 |
| WebKit (Safari) | Yes | No | Yes | P3 |

**Default**: Firefox desktop — all tests run here.
**Extended**: Chromium + WebKit added for nightly/pre-release runs.

---

## Test Data Requirements

### Accounts
- Customer: `customer@practicesoftwaretesting.com` / `welcome01` (pre-seeded)
- Admin: `admin@practicesoftwaretesting.com` / `welcome01` (pre-seeded)
- New Registration: generate unique email per run (`test_[timestamp]@test.com`)

### Product Data
- Use pre-seeded products (IDs 1-50+)
- Products known to exist: pliers, hammer, saw, screwdriver, bolt cutters
- Price range: $5 - $200+

### Cleanup Strategy
- Registration tests: no cleanup needed (shared DB, disposable test accounts)
- Cart tests: each test starts fresh (new browser context = new session)
- Favorites: remove after test via API if needed

### State Dependencies

| Test | Precondition | Setup Method |
|------|--------------|--------------|
| Checkout | Logged in + items in cart | Fixture: login + add product via API |
| Profile edit | Logged in | Fixture: login |
| Order history | Has previous orders | Seed via API or use existing customer account |
| Admin reports | Logged in as admin | Fixture: admin login |

---

## Automation Feasibility & ROI

| Feature | Effort | Maintenance | Stability | ROI | Priority |
|---------|:-----:|:-----:|:-----:|:-----:|:-----:|
| Login | Low | Low | High | **Very High** | Wave 1 |
| Registration | Low | Low | High | **Very High** | Wave 1 |
| Product Search | Low | Low | High | **High** | Wave 1 |
| Add to Cart | Medium | Low | High | **High** | Wave 1 |
| Checkout | High | Medium | Medium | **High** | Wave 1 |
| Cart Management | Medium | Low | High | **High** | Wave 2 |
| Product Filter/Sort | Medium | Low | Medium | **Medium** | Wave 2 |
| Product Detail | Low | Low | High | **Medium** | Wave 2 |
| Contact Form | Low | Low | High | **Medium** | Wave 3 |
| User Profile | Medium | Medium | Medium | **Medium** | Wave 3 |
| Admin Dashboard | High | High | Medium | **Low** | Wave 3 |
| Favorites | Low | Low | High | **Low** | Wave 3 |

---

## Implementation Waves

### Wave 1 — Smoke + Critical Path (Week 1)
- Login (positive + negative)
- Registration (positive + validation)
- Product search + filter
- Add to cart
- Checkout end-to-end
- **Output**: 25-30 tests, smoke suite ready

### Wave 2 — Regression Expansion (Week 2)
- Cart management (quantity, remove, price calculation)
- Product detail + related products
- All filter/sort combinations
- API intercept (login, cart, checkout)
- Accessibility (all critical pages)
- **Output**: +20-25 tests, regression suite ready

### Wave 3 — Full Coverage (Week 3)
- Contact form
- User profile
- Admin dashboard (basic)
- Visual regression (all viewports)
- Performance budgets
- Edge cases & security inputs
- **Output**: +15-20 tests, full suite ready

---

## Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Shared database (other users modify data) | Test flakiness | Use own data, assert specifically, avoid hard-coded IDs |
| SPA dynamic rendering | Selector instability | Use `data-test` attributes where available, fallback to role/text |
| Session/token expiry | Auth failures mid-test | Fresh login per test via fixture (new browser context) |
| Site version updates (sprint changes) | Tests break | Pin test against Sprint 5, monitor for UI changes |
| Network latency (hosted app) | Timeout flakes | Generous timeouts (60s navigate, 30s element), retry policy |

---

## Next Steps

Execute in order:
1. `@1-analyze-website.md https://practicesoftwaretesting.com` — Deep element analysis for Wave 1 features
2. `@2-generate-test-cases.md https://practicesoftwaretesting.com --feature login,registration,search,cart,checkout` — Test case design for Wave 1
3. `@3-generate-automation.md https://practicesoftwaretesting.com --all` — Generate full code
4. `@4-accessibility-test.md https://practicesoftwaretesting.com` — a11y suite
5. `@5-api-intercept-test.md https://practicesoftwaretesting.com --feature login,cart,checkout` — API intercept
6. `@6-visual-regression.md https://practicesoftwaretesting.com` — Visual baselines

---

*Generated by Web Test Generator Agent — Skill 0 (Test Strategy)*
*Date: 2026-08-15*
