# Website Analysis — Practice Software Testing (Toolshop)

## Page Overview

- **URL**: https://practicesoftwaretesting.com
- **Purpose**: E-commerce tool shop — browse, search, purchase tools with full checkout flow
- **Tech Stack**: Angular SPA (client-side rendering), REST API backend (Laravel)
- **API**: https://api.practicesoftwaretesting.com
- **Selector Strategy**: Site uses `data-test` attributes extensively — ideal for automation

---

## Page Map

| # | Route | Page Name | Auth Required |
|---|-------|-----------|:-----:|
| 1 | `/` | Homepage / Product Listing | No |
| 2 | `/product/{id}` | Product Detail | No |
| 3 | `/auth/login` | Login | No |
| 4 | `/auth/register` | Registration | No |
| 5 | `/auth/forgot-password` | Forgot Password | No |
| 6 | `/checkout` | Cart + Checkout (multi-step) | Partial (Step 2+) |
| 7 | `/contact` | Contact Form | No |
| 8 | `/account` | User Profile / Dashboard | Yes |
| 9 | `/account/favorites` | Favorites | Yes |
| 10 | `/account/invoices` | Invoices | Yes |
| 11 | `/admin/dashboard` | Admin Dashboard | Yes (admin) |

---

## Elements Inventory

### Global Navigation (all pages)

| Element | Type | Selector | Notes |
|---------|------|----------|-------|
| Home link | nav link | `[data-test='nav-home']` | Logo/brand link |
| Categories dropdown | nav dropdown | `[data-test='nav-categories']` | Submenu with categories |
| Contact link | nav link | `[data-test='nav-contact']` | |
| Sign In link | nav link | `[data-test='nav-sign-in']` | Changes to "My Account" when logged in |
| Cart icon | nav link + badge | `[data-test='nav-cart']` | Shows item count badge |
| Language selector | dropdown | `.lang-select` | EN/DE/FR/NL |

---

### Page: Homepage / Product Listing (`/`)

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Search input | text input | `[data-test='search-query']` | No | Keyword search |
| Search button | button | `[data-test='search-submit']` | — | Triggers search |
| Search reset | button | `[data-test='search-reset']` | — | Clear search |
| Sort dropdown | select | `[data-test='sort']` | No | Name A-Z/Z-A, Price Low-High/High-Low |
| Category filter | checkboxes | `[data-test='category-{id}']` | No | Hand Tools, Power Tools, Other |
| Brand filter | checkboxes | `[data-test='brand-{id}']` | No | Brand name filters |
| Price range slider | range input | `.ngx-slider` | No | Min/max price filter |
| Product card | link card | `a.card` | — | Clickable product tile |
| Product name | text | `[data-test='product-name']` | — | Within card |
| Product price | text | `[data-test='product-price']` | — | Within card, format: `$XX.XX` |
| Pagination next | button | `[data-test='pagination-next']` | — | 9 products per page |
| Pagination prev | button | `[data-test='pagination-prev']` | — | |
| Page indicators | buttons | `.page-item` | — | Page numbers |

**Behavior notes:**
- Products load via API (`GET /products`)
- 9 products per page (3x3 grid)
- Filters are additive (category + brand + price combined)
- Sort applies to filtered results
- Search is keyword-based, DB wildcard `%` supported
- Category IDs: 1=Hand Tools, 2=Power Tools, 3=Other (+ sub-categories)

---

### Page: Product Detail (`/product/{id}`)

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Product name | heading | `[data-test='product-name']` | — | |
| Unit price | text | `[data-test='unit-price']` | — | Format: `$XX.XX` |
| Description | paragraph | `[data-test='product-description']` | — | |
| Product image | image | `#product-image` | — | |
| Quantity input | number input | `[data-test='quantity']` | No | Default: 1, min: 1 |
| Increase qty | button | `[data-test='increase-quantity']` | — | +1 |
| Decrease qty | button | `[data-test='decrease-quantity']` | — | -1 (min 1) |
| Add to Cart | button | `[data-test='add-to-cart']` | — | Shows toast on success |
| Add to Favorites | button | `[data-test='add-to-favorites']` | — | Requires login |
| Related products | cards | `[data-test='related-product']` | — | Below product details |
| Toast notification | alert | `[role='alert']` | — | "Product added to shopping cart" |

**Behavior notes:**
- Add to Cart works without login (anonymous cart)
- Add to Favorites requires login (redirects to login if not authenticated)
- Quantity validates: min 1, max varies
- Toast auto-disappears after ~3 seconds
- Related products shown based on category

---

### Page: Login (`/auth/login`)

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Email input | email | `[data-test='email']` | Yes | Email format validation |
| Password input | password | `[data-test='password']` | Yes | |
| Login button | submit | `[data-test='login-submit']` | — | |
| Register link | link | `[data-test='register-link']` | — | → `/auth/register` |
| Forgot password link | link | `[data-test='forgot-password-link']` | — | → `/auth/forgot-password` |
| Error message | alert | `[data-test='login-error']` | — | "Invalid email or password" |

**Behavior notes:**
- On success: redirects to `/account` (or previous page)
- On failure: shows error message, stays on page
- Token stored in localStorage (Bearer token for API)
- Session expires after inactivity

**Validation rules:**
- Email: required, must be valid email format
- Password: required, no format restriction on input (backend validates)

---

### Page: Registration (`/auth/register`)

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| First name | text | `[data-test='first-name']` | Yes | |
| Last name | text | `[data-test='last-name']` | Yes | |
| Date of birth | date | `[data-test='dob']` | Yes | Format: YYYY-MM-DD |
| Address | text | `[data-test='address']` | Yes | |
| City | text | `[data-test='city']` | Yes | |
| State | text | `[data-test='state']` | Yes | |
| Country | select | `[data-test='country']` | Yes | Dropdown (ISO codes) |
| Postcode | text | `[data-test='postcode']` | Yes | |
| Phone | text | `[data-test='phone']` | Yes | |
| Email | email | `[data-test='email']` | Yes | Unique (not already registered) |
| Password | password | `[data-test='password']` | Yes | Min length required |
| Register button | submit | `[data-test='register-submit']` | — | |
| Error messages | text | `.help-block` | — | Per-field validation |

**Behavior notes:**
- On success: redirects to `/auth/login`
- On failure: inline error messages per field
- Email must be unique (API returns error if duplicate)
- Password: minimum 6 characters, must contain uppercase + lowercase + number

**Validation rules:**
- First/Last name: required, alpha characters
- DOB: required, valid date
- Address/City/State: required
- Country: required (select)
- Postcode: required
- Phone: required, numeric
- Email: required, valid format, unique
- Password: required, min 6 chars, complexity rules

---

### Page: Cart + Checkout (`/checkout`) — Multi-Step

**Step 1: Cart Review**

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Product title | text | `[data-test='product-title']` | — | Item name |
| Product quantity | number input | `[data-test='product-quantity']` | — | Editable |
| Remove button | button | `a.btn-danger` | — | Remove from cart |
| Cart total | text | `[data-test='cart-total']` | — | Format: `$XX.XX` |
| Proceed button | button | `[data-test='proceed-1']` | — | → Step 2 |

**Step 2: Sign In**

| Element | Type | Selector | Notes |
|---------|------|----------|-------|
| Proceed button | button | `[data-test='proceed-2']` | Auto-proceeds if logged in |

**Step 3: Billing Address**

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Street | text | `[data-test='street']` | Yes | |
| House number | text | `[data-test='house_number']` | Yes | |
| City | text | `[data-test='city']` | Yes | |
| State | text | `[data-test='state']` | Yes | |
| Country | select | `[data-test='country']` | Yes | |
| Postcode | text | `[data-test='postal_code']` | Yes | |
| Proceed button | button | `[data-test='proceed-3']` | — | → Step 4 |

**Step 4: Payment**

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| Payment method | select | `[data-test='payment-method']` | Yes | Bank Transfer, Cash on Delivery, Credit Card, Buy Now Pay Later, Gift Card |
| Bank name | text | `[data-test='bank_name']` | Conditional | Only for Bank Transfer |
| Account name | text | `[data-test='account_name']` | Conditional | Only for Bank Transfer |
| Account number | text | `[data-test='account_number']` | Conditional | Only for Bank Transfer |
| Credit card number | text | `[data-test='credit_card_number']` | Conditional | Only for Credit Card |
| Expiration date | text | `[data-test='expiration_date']` | Conditional | Only for Credit Card |
| CVV | text | `[data-test='cvv']` | Conditional | Only for Credit Card |
| Card holder | text | `[data-test='card_holder_name']` | Conditional | Only for Credit Card |
| Monthly installments | text | `[data-test='monthly_installments']` | Conditional | Only for Buy Now Pay Later |
| Gift card number | text | `[data-test='gift_card_number']` | Conditional | Only for Gift Card |
| Validation code | text | `[data-test='validation_code']` | Conditional | Only for Gift Card |
| Confirm button | button | `[data-test='finish']` | — | Submit payment |

**Step 5: Confirmation**

| Element | Type | Selector | Notes |
|---------|------|----------|-------|
| Success message | text | `[data-test='payment-success-message']` | "Payment was successful" |
| Invoice number | text | `[data-test='invoice-number']` | Order reference |

**Behavior notes:**
- Cart persists across sessions (stored in backend by session/token)
- Anonymous users can add to cart but must login at Step 2
- Payment fields change dynamically based on selected method
- Confirm button validates all payment fields before submit
- On success: shows confirmation + invoice number

---

### Page: Contact Form (`/contact`)

| Element | Type | Selector | Required | Notes |
|---------|------|----------|:-----:|-------|
| First name | text | `[data-test='first-name']` | Yes | |
| Last name | text | `[data-test='last-name']` | Yes | |
| Email | email | `[data-test='email']` | Yes | |
| Subject | select | `[data-test='subject']` | Yes | Customer Service, Webmaster, Return, Payments |
| Message | textarea | `[data-test='message']` | Yes | Min 50 characters |
| Attachment | file input | `[data-test='attachment']` | No | Optional file upload |
| Submit button | button | `[data-test='contact-submit']` | — | |
| Success message | alert | `.alert-success` | — | Confirmation after submit |
| Error messages | alert | `.alert.alert-danger` | — | Validation errors |

**Validation rules:**
- First name: required
- Last name: required
- Email: required, valid format
- Subject: required (select from dropdown)
- Message: required, minimum 50 characters

---

## User Flows

### Flow 1: Browse & Purchase (Critical — Revenue Path)
1. User lands on homepage → products grid visible
2. User searches/filters products → results update
3. User clicks product → detail page loads
4. User sets quantity → clicks "Add to Cart"
5. Toast confirms addition → cart badge updates
6. User navigates to cart → verifies items & total
7. User proceeds to checkout → login step (login if needed)
8. User fills billing address → proceeds
9. User selects payment → fills payment details
10. User confirms → "Payment was successful" displayed
- **Failure points**: Login fails, address validation, payment validation, network error

### Flow 2: User Registration
1. Navigate to `/auth/register`
2. Fill all fields (11 fields)
3. Submit → redirect to login page
4. Login with new credentials → success
- **Failure points**: Duplicate email, password complexity, field validation

### Flow 3: Product Search & Filter
1. Enter keyword in search → products filter
2. Apply category checkbox → results narrow
3. Apply sort → order changes
4. Paginate → next page loads
5. Reset → all products shown again
- **Failure points**: Empty results, no results for invalid query

### Flow 4: Contact Support
1. Navigate to `/contact`
2. Fill form (5 fields)
3. Submit → success message displayed
- **Failure points**: Message too short, invalid email

### Flow 5: Cart Management
1. Add multiple products from different pages
2. Go to cart → verify all items present
3. Change quantity → total recalculates
4. Remove item → cart updates
5. Proceed to checkout
- **Failure points**: Quantity = 0, negative quantity, empty cart proceed

---

## Element Selector Strategy Summary

This site uses `data-test` attributes on almost all interactive elements — making it ideal for stable, maintainable test selectors.

| Priority | Count | Strategy | Usage |
|:-----:|:-----:|----------|-------|
| 1 | ~80% | `[data-test='xxx']` | All forms, buttons, nav, products |
| 2 | ~10% | `[role='alert']` | Toast notifications |
| 3 | ~5% | CSS class | `.alert-success`, `.help-block`, `a.card` |
| 4 | ~3% | Text content | Fallback for dynamic labels |
| 5 | ~2% | ID | `#product-image` |
| 6 | 0% | XPath | Not needed |

---

## Test Boundaries

### Required Fields Summary

| Page | Required Fields |
|------|----------------|
| Login | email, password |
| Registration | first_name, last_name, dob, address, city, state, country, postcode, phone, email, password (11 fields) |
| Contact | first_name, last_name, email, subject, message |
| Billing Address | street, house_number, city, state, country, postcode |
| Payment (Bank) | bank_name, account_name, account_number |
| Payment (Card) | credit_card_number, expiration_date, cvv, card_holder_name |

### Validation Rules

| Field | Rule |
|-------|------|
| Email (all forms) | Valid email format, `@` required |
| Password (register) | Min 6 chars, uppercase + lowercase + number |
| Phone (register) | Numeric only |
| Message (contact) | Min 50 characters |
| Quantity (product) | Min 1, integer |
| DOB (register) | Valid date, format YYYY-MM-DD |

### State Dependencies

| Action | Required State |
|--------|---------------|
| Checkout (Step 2+) | Must be logged in |
| Add to Favorites | Must be logged in |
| View Invoices | Must be logged in + have past orders |
| Admin Dashboard | Must be admin role |
| Cart review | Must have items in cart |

### Business Rules

| Rule | Description |
|------|-------------|
| Cart persistence | Cart items persist per session (cookie/token based) |
| Payment methods | Fields change dynamically per selected method |
| Product stock | No visible stock limit (always in stock) |
| Price calculation | Total = sum(unit_price × quantity) per item |
| Registration uniqueness | Email must not already exist in system |

---

## Recommended Test Coverage (from Risk Assessment)

| Feature | Critical | Positive | Negative | Edge | Total |
|---------|:-----:|:-----:|:-----:|:-----:|:-----:|
| Login | 1 | 1 | 4 | 2 | 8 |
| Registration | 1 | 2 | 5 | 3 | 11 |
| Product Search | 1 | 3 | 2 | 2 | 8 |
| Product Detail | 1 | 2 | 1 | 1 | 5 |
| Cart | 1 | 2 | 3 | 2 | 8 |
| Checkout | 1 | 2 | 4 | 2 | 9 |
| Contact | 1 | 1 | 3 | 1 | 6 |
| **Total** | **7** | **13** | **22** | **13** | **55** |

---

## Next Steps

```
@2-generate-test-cases.md https://practicesoftwaretesting.com --feature login,registration,search,cart,checkout,contact
```

---

*Generated by Web Test Generator Agent — Skill 1 (Analyze Website)*
*Date: 2026-08-15*
