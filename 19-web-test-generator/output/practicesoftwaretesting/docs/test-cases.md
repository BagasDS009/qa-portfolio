# Test Cases — Practice Software Testing (Toolshop)

## Summary

- **URL**: https://practicesoftwaretesting.com
- **Total test cases**: 55
- **Critical**: 7 | **Positive**: 13 | **Negative**: 22 | **Edge**: 13
- **Automation priority**: Wave 1 (30 tests) → Wave 2 (15 tests) → Wave 3 (10 tests)

---

## Test Data

```python
# === Valid Credentials ===
VALID_CUSTOMER = {
    "email": "customer@practicesoftwaretesting.com",
    "password": "welcome01",
}

VALID_ADMIN = {
    "email": "admin@practicesoftwaretesting.com",
    "password": "welcome01",
}

# === Invalid Credentials ===
INVALID_CREDENTIALS = {
    "wrong_password": {"email": "customer@practicesoftwaretesting.com", "password": "WrongPass123!"},
    "unregistered": {"email": "nobody@nonexistent.com", "password": "test123"},
    "empty_email": {"email": "", "password": "welcome01"},
    "empty_password": {"email": "customer@practicesoftwaretesting.com", "password": ""},
    "empty_both": {"email": "", "password": ""},
    "invalid_email_format": {"email": "not-an-email", "password": "welcome01"},
    "sql_injection": {"email": "' OR '1'='1' --", "password": "test"},
    "xss_attempt": {"email": "<script>alert(1)</script>", "password": "test"},
}

# === Registration Data ===
VALID_REGISTRATION = {
    "first_name": "Test",
    "last_name": "Automation",
    "dob": "1990-05-15",
    "address": "123 Test Street",
    "city": "Jakarta",
    "state": "DKI Jakarta",
    "country": "ID",
    "postcode": "12345",
    "phone": "081234567890",
    "email": "test_{timestamp}@test.com",  # unique per run
    "password": "Welcome01!",
}

# === Search Data ===
SEARCH_QUERIES = {
    "valid_exact": "pliers",
    "valid_partial": "ham",
    "valid_multi_result": "tool",
    "no_results": "xyznonexistent999",
    "special_chars": "<%>",
    "sql_wildcard": "%",
    "empty": "",
}

# === Billing Address ===
VALID_ADDRESS = {
    "street": "123 Test Street",
    "house_number": "42",
    "city": "Amsterdam",
    "state": "Noord-Holland",
    "country": "NL",
    "postcode": "1234AB",
}

# === Payment Data ===
VALID_BANK_TRANSFER = {
    "bank_name": "Test Bank",
    "account_name": "Test Account",
    "account_number": "1234567890",
}

# === Contact Data ===
VALID_CONTACT = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "subject": "Webmaster",
    "message": "This is an automated test message for verification. It needs to be at least fifty characters long to pass validation.",
}

# === Boundary & Security ===
BOUNDARY_DATA = {
    "min_password": "Aa1!",
    "max_length_255": "A" * 255,
    "max_length_256": "A" * 256,
    "unicode_name": "Tes\u0301t U\u0308ser",
    "emoji_name": "Test User 🔧",
    "html_injection": "<h1>Injected</h1>",
    "xss_script": "<script>alert('XSS')</script>",
    "sql_injection": "'; DROP TABLE users; --",
    "path_traversal": "../../etc/passwd",
    "very_long_email": "a" * 200 + "@test.com",
    "short_message": "Too short",
}
```

---

## LOGIN

### CRITICAL

#### TC-LOGIN-001: Login with valid credentials succeeds
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/auth/login`
  2. Enter email: `customer@practicesoftwaretesting.com`
  3. Enter password: `welcome01`
  4. Click Login button
- **Expected**: User redirected to `/account`, no error displayed
- **Test Data**: `VALID_CUSTOMER`

---

### POSITIVE

#### TC-LOGIN-002: Login as admin user
- **Severity**: NORMAL
- **Priority**: P2 (regression)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/auth/login`
  2. Enter admin credentials
  3. Click Login
- **Expected**: Redirected to account/admin area
- **Test Data**: `VALID_ADMIN`

---

### NEGATIVE

#### TC-LOGIN-003: Login with wrong password shows error
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/auth/login`
  2. Enter valid email, wrong password
  3. Click Login
- **Expected**: Error message "Invalid email or password" displayed, user stays on login page
- **Test Data**: `INVALID_CREDENTIALS["wrong_password"]`

#### TC-LOGIN-004: Login with unregistered email shows error
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: None
- **Steps**:
  1. Enter unregistered email + any password
  2. Click Login
- **Expected**: Error message displayed
- **Test Data**: `INVALID_CREDENTIALS["unregistered"]`

#### TC-LOGIN-005: Login with empty email field
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: None
- **Steps**:
  1. Leave email empty, enter password
  2. Click Login
- **Expected**: Validation prevents submission or shows error
- **Test Data**: `INVALID_CREDENTIALS["empty_email"]`

#### TC-LOGIN-006: Login with empty password field
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter valid email, leave password empty
  2. Click Login
- **Expected**: Validation prevents submission or shows error
- **Test Data**: `INVALID_CREDENTIALS["empty_password"]`

---

### EDGE CASES

#### TC-LOGIN-007: Login with SQL injection in email field
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter `' OR '1'='1' --` as email
  2. Enter any password
  3. Click Login
- **Expected**: Login fails safely, no unauthorized access, no server error
- **Test Data**: `INVALID_CREDENTIALS["sql_injection"]`

#### TC-LOGIN-008: Login with XSS attempt in email field
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter `<script>alert(1)</script>` as email
  2. Click Login
- **Expected**: Input is sanitized, no script execution, safe error message
- **Test Data**: `INVALID_CREDENTIALS["xss_attempt"]`

---

## REGISTRATION

### CRITICAL

#### TC-REG-001: Registration with all valid fields succeeds
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: Email not already registered
- **Steps**:
  1. Navigate to `/auth/register`
  2. Fill all 11 fields with valid data
  3. Click Register
- **Expected**: Redirected to `/auth/login`, account created
- **Test Data**: `VALID_REGISTRATION` (with unique timestamp email)

---

### POSITIVE

#### TC-REG-002: Registration and then login with new account
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: None
- **Steps**:
  1. Register with unique email
  2. Navigate to login
  3. Login with new credentials
- **Expected**: Login successful, account accessible
- **Test Data**: Generated unique email

#### TC-REG-003: Registration with minimum valid password
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Fill all fields with minimum valid values
  2. Password: exactly meets minimum requirements (6 chars + uppercase + lowercase + number)
  3. Submit
- **Expected**: Registration successful
- **Test Data**: Password `"Abc123"`

---

### NEGATIVE

#### TC-REG-004: Registration with duplicate email
- **Severity**: CRITICAL
- **Priority**: P1
- **Steps**:
  1. Register with `customer@practicesoftwaretesting.com` (already exists)
  2. Fill all other fields validly
  3. Submit
- **Expected**: Error message indicating email already exists
- **Test Data**: Existing customer email

#### TC-REG-005: Registration with empty required fields
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Leave all fields empty
  2. Click Register
- **Expected**: Validation errors shown for all required fields
- **Test Data**: All empty

#### TC-REG-006: Registration with invalid email format
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter "not-an-email" as email
  2. Fill other fields validly
  3. Submit
- **Expected**: Email validation error
- **Test Data**: Email `"not-an-email"`

#### TC-REG-007: Registration with weak password
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter password without uppercase/number: `"password"`
  2. Fill other fields validly
  3. Submit
- **Expected**: Password complexity error
- **Test Data**: Password `"password"`

#### TC-REG-008: Registration with too short password
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter password shorter than 6 chars: `"Ab1"`
  2. Submit
- **Expected**: Password length error
- **Test Data**: Password `"Ab1"`

---

### EDGE CASES

#### TC-REG-009: Registration with unicode characters in name
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. First name: `"Tést Üser"`
  2. Fill all other fields validly
  3. Submit
- **Expected**: Registration succeeds (or clear error if not supported)
- **Test Data**: `BOUNDARY_DATA["unicode_name"]`

#### TC-REG-010: Registration with max-length fields
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Fill first name with 255 characters
  2. Fill other fields normally
  3. Submit
- **Expected**: Either succeeds or shows max-length validation
- **Test Data**: `BOUNDARY_DATA["max_length_255"]`

#### TC-REG-011: Registration with HTML in name field
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. First name: `"<h1>Injected</h1>"`
  2. Submit with other fields valid
- **Expected**: HTML is escaped/sanitized, not rendered
- **Test Data**: `BOUNDARY_DATA["html_injection"]`

---

## PRODUCT SEARCH & FILTER

### CRITICAL

#### TC-SEARCH-001: Search by keyword returns matching products
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: Products exist with keyword "pliers"
- **Steps**:
  1. Navigate to homepage
  2. Enter "pliers" in search field
  3. Click Search
- **Expected**: Products containing "pliers" in name are displayed
- **Test Data**: `SEARCH_QUERIES["valid_exact"]`

---

### POSITIVE

#### TC-SEARCH-002: Search with partial keyword
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Search "ham"
- **Expected**: Products matching partial keyword (e.g., "hammer") displayed
- **Test Data**: `SEARCH_QUERIES["valid_partial"]`

#### TC-SEARCH-003: Filter by category
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Click "Hand Tools" category checkbox
- **Expected**: Only hand tools shown, count reduced from total

#### TC-SEARCH-004: Sort products by price low to high
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Select "Price (Low - High)" from sort dropdown
- **Expected**: Products ordered by ascending price

---

### NEGATIVE

#### TC-SEARCH-005: Search with non-existent keyword shows no results
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Search "xyznonexistent999"
- **Expected**: No products displayed, appropriate message or empty grid
- **Test Data**: `SEARCH_QUERIES["no_results"]`

#### TC-SEARCH-006: Search with empty query
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Click search without entering text
- **Expected**: All products remain visible (no filter applied)
- **Test Data**: `SEARCH_QUERIES["empty"]`

---

### EDGE CASES

#### TC-SEARCH-007: Search with SQL wildcard character
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Search "%"
- **Expected**: Either shows all results or handles gracefully (no server error)
- **Test Data**: `SEARCH_QUERIES["sql_wildcard"]`

#### TC-SEARCH-008: Search with special characters
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Search "<%>"
- **Expected**: No crash, safe handling
- **Test Data**: `SEARCH_QUERIES["special_chars"]`

---

## SHOPPING CART

### CRITICAL

#### TC-CART-001: Add product to cart from product detail page
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: On product detail page
- **Steps**:
  1. Navigate to any product detail page
  2. Click "Add to Cart"
  3. Wait for toast confirmation
- **Expected**: Toast "Product added to shopping cart" appears, cart badge shows 1
- **Test Data**: Any product

---

### POSITIVE

#### TC-CART-002: Add multiple different products to cart
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Add product A to cart
  2. Navigate to different product B
  3. Add product B to cart
  4. Go to cart page
- **Expected**: Both products listed, quantities correct, total = sum of prices

#### TC-CART-003: Update product quantity in cart
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: 1 item in cart
- **Steps**:
  1. Go to cart
  2. Change quantity from 1 to 3
  3. Tab out of field
- **Expected**: Total recalculates (unit_price × 3)

---

### NEGATIVE

#### TC-CART-004: Proceed to checkout with empty cart
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: Cart is empty
- **Steps**:
  1. Navigate to `/checkout`
  2. Attempt to proceed
- **Expected**: Cannot proceed, appropriate message or disabled button

#### TC-CART-005: Set quantity to 0
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: 1 item in cart
- **Steps**:
  1. Change quantity to 0
- **Expected**: Item removed from cart OR validation error

#### TC-CART-006: Set negative quantity
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Enter -1 as quantity
- **Expected**: Validation prevents negative quantity

---

### EDGE CASES

#### TC-CART-007: Add same product multiple times
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Add product A to cart
  2. Go back to product A detail
  3. Add to cart again
- **Expected**: Quantity increments (doesn't create duplicate row)

#### TC-CART-008: Remove all items from cart
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: 2+ items in cart
- **Steps**:
  1. Remove first item
  2. Remove second item
- **Expected**: Cart shows empty state

---

## CHECKOUT

### CRITICAL

#### TC-CHECKOUT-001: Complete checkout with bank transfer
- **Severity**: CRITICAL
- **Priority**: P1 (smoke)
- **Precondition**: Logged in, 1+ items in cart
- **Steps**:
  1. Proceed from cart (Step 1)
  2. Proceed past sign-in (Step 2)
  3. Fill billing address
  4. Proceed to payment (Step 3)
  5. Select "Bank Transfer"
  6. Fill bank details
  7. Click Confirm
- **Expected**: "Payment was successful" message displayed
- **Test Data**: `VALID_ADDRESS` + `VALID_BANK_TRANSFER`

---

### POSITIVE

#### TC-CHECKOUT-002: Checkout with Cash on Delivery
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: Logged in, items in cart
- **Steps**:
  1. Complete checkout selecting "Cash on Delivery"
- **Expected**: Payment successful, no additional fields needed

#### TC-CHECKOUT-003: Checkout with different billing address
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Fill billing with different country (e.g., US)
  2. Complete payment
- **Expected**: Checkout succeeds regardless of address country

---

### NEGATIVE

#### TC-CHECKOUT-004: Checkout with empty billing address
- **Severity**: CRITICAL
- **Priority**: P1
- **Precondition**: Logged in, items in cart
- **Steps**:
  1. Proceed to billing step
  2. Leave all fields empty
  3. Click Proceed
- **Expected**: Validation errors shown, cannot proceed to payment

#### TC-CHECKOUT-005: Checkout with empty payment fields (bank transfer)
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Fill billing correctly
  2. Select Bank Transfer
  3. Leave bank fields empty
  4. Click Confirm
- **Expected**: Validation errors, payment not processed

#### TC-CHECKOUT-006: Checkout without login
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: NOT logged in, items in cart
- **Steps**:
  1. Proceed from cart
  2. At sign-in step, attempt to proceed without logging in
- **Expected**: Must login before continuing (blocked at Step 2)

#### TC-CHECKOUT-007: Checkout with invalid postal code format
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Enter "!@#$%" as postal code
  2. Submit billing
- **Expected**: Validation error on postal code

---

### EDGE CASES

#### TC-CHECKOUT-008: Back button during checkout flow
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Proceed to payment step
  2. Click browser Back button
  3. Go forward again
- **Expected**: Data preserved or user returned to correct step

#### TC-CHECKOUT-009: Double-click confirm button
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Fill all checkout steps
  2. Double-click Confirm rapidly
- **Expected**: Only one order created, no duplicate payment

---

## CONTACT FORM

### CRITICAL

#### TC-CONTACT-001: Submit contact form with valid data
- **Severity**: NORMAL
- **Priority**: P2
- **Precondition**: None
- **Steps**:
  1. Navigate to `/contact`
  2. Fill all fields (first name, last name, email, subject, message 50+ chars)
  3. Click Submit
- **Expected**: Success message displayed
- **Test Data**: `VALID_CONTACT`

---

### POSITIVE

#### TC-CONTACT-002: Submit with different subject options
- **Severity**: MINOR
- **Priority**: P3
- **Steps**:
  1. Submit form with subject "Return"
  2. Submit form with subject "Payments"
- **Expected**: All subject options work correctly

---

### NEGATIVE

#### TC-CONTACT-003: Submit with all empty fields
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Click Submit without filling any field
- **Expected**: Validation errors for all required fields

#### TC-CONTACT-004: Submit with invalid email format
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter "not-an-email" as email
  2. Fill other fields validly
  3. Submit
- **Expected**: Email validation error

#### TC-CONTACT-005: Submit with message shorter than 50 characters
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter "Too short" as message (9 chars)
  2. Fill other fields validly
  3. Submit
- **Expected**: Message length validation error
- **Test Data**: `BOUNDARY_DATA["short_message"]`

---

### EDGE CASES

#### TC-CONTACT-006: Submit with XSS in message field
- **Severity**: NORMAL
- **Priority**: P2
- **Steps**:
  1. Enter `<script>alert('XSS')</script>` in message (padded to 50+ chars)
  2. Submit
- **Expected**: Submitted safely, script not executed, content sanitized

---

## Priority Matrix (Automation Waves)

### Wave 1 — Smoke + Critical (30 tests)

| TC-ID | Feature | Title |
|-------|---------|-------|
| TC-LOGIN-001 | Login | Valid login |
| TC-LOGIN-003 | Login | Wrong password error |
| TC-LOGIN-004 | Login | Unregistered email error |
| TC-LOGIN-005 | Login | Empty email |
| TC-LOGIN-006 | Login | Empty password |
| TC-REG-001 | Registration | Valid registration |
| TC-REG-004 | Registration | Duplicate email |
| TC-REG-005 | Registration | Empty fields |
| TC-REG-006 | Registration | Invalid email |
| TC-REG-007 | Registration | Weak password |
| TC-REG-008 | Registration | Short password |
| TC-SEARCH-001 | Search | Valid search |
| TC-SEARCH-002 | Search | Partial keyword |
| TC-SEARCH-003 | Search | Category filter |
| TC-SEARCH-004 | Search | Sort by price |
| TC-SEARCH-005 | Search | No results |
| TC-CART-001 | Cart | Add to cart |
| TC-CART-002 | Cart | Multiple products |
| TC-CART-003 | Cart | Update quantity |
| TC-CART-004 | Cart | Empty cart proceed |
| TC-CART-005 | Cart | Quantity zero |
| TC-CHECKOUT-001 | Checkout | Bank transfer success |
| TC-CHECKOUT-002 | Checkout | Cash on delivery |
| TC-CHECKOUT-004 | Checkout | Empty billing |
| TC-CHECKOUT-005 | Checkout | Empty payment |
| TC-CHECKOUT-006 | Checkout | Without login |
| TC-CONTACT-001 | Contact | Valid submit |
| TC-CONTACT-003 | Contact | Empty fields |
| TC-CONTACT-004 | Contact | Invalid email |
| TC-CONTACT-005 | Contact | Short message |

### Wave 2 — Extended Regression (15 tests)

| TC-ID | Feature | Title |
|-------|---------|-------|
| TC-LOGIN-002 | Login | Admin login |
| TC-LOGIN-007 | Login | SQL injection |
| TC-LOGIN-008 | Login | XSS attempt |
| TC-REG-002 | Registration | Register then login |
| TC-REG-003 | Registration | Minimum password |
| TC-REG-009 | Registration | Unicode name |
| TC-REG-011 | Registration | HTML injection |
| TC-SEARCH-006 | Search | Empty query |
| TC-SEARCH-007 | Search | SQL wildcard |
| TC-CART-006 | Cart | Negative quantity |
| TC-CART-007 | Cart | Add same product twice |
| TC-CART-008 | Cart | Remove all items |
| TC-CHECKOUT-003 | Checkout | Different address |
| TC-CHECKOUT-008 | Checkout | Back button |
| TC-CONTACT-006 | Contact | XSS in message |

### Wave 3 — Edge & Boundary (10 tests)

| TC-ID | Feature | Title |
|-------|---------|-------|
| TC-REG-010 | Registration | Max-length fields |
| TC-SEARCH-008 | Search | Special characters |
| TC-CHECKOUT-007 | Checkout | Invalid postal code |
| TC-CHECKOUT-009 | Checkout | Double-click confirm |
| TC-CONTACT-002 | Contact | Different subjects |
| + 5 accessibility/visual/performance tests from Skills 4-6 |

---

## Next Steps

```
@3-generate-automation.md https://practicesoftwaretesting.com --all
```

---

*Generated by Web Test Generator Agent — Skill 2 (Generate Test Cases)*
*Date: 2026-08-15*
