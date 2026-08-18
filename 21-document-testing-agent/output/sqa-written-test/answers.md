# SQA Written Test — Answers

---

## Q1. Test Cases for demo.midtrans.com

> Cart Functionality, Checkout Flow, Payment Page — including Negative and Edge Cases.

---

### A. Cart Functionality

**Positive Cases**

| ID | Test Case |
|----|-----------|
| CART-001 | Add a single item to cart — verify item appears with correct name, price, and quantity |
| CART-002 | Add multiple different items — verify all items display with individual prices |
| CART-003 | Increase item quantity — verify unit price × quantity = subtotal |
| CART-004 | Decrease item quantity — verify subtotal updates accordingly |
| CART-005 | Remove item from cart — verify item disappears, total recalculates |
| CART-006 | Cart total equals sum of all item subtotals |
| CART-007 | Cart persists after page refresh |
| CART-008 | Cart badge/count updates when items are added/removed |

**Negative Cases**

| ID | Test Case |
|----|-----------|
| CART-009 | Set quantity to 0 — item should be removed or blocked |
| CART-010 | Attempt to add item when out of stock (if applicable) — appropriate error message |
| CART-011 | Set quantity to negative number — system should reject |
| CART-012 | Proceed to checkout with empty cart — should be blocked with user feedback |
| CART-013 | Remove last item while on checkout — behavior when cart becomes empty mid-flow |

**Edge Cases**

| ID | Test Case |
|----|-----------|
| CART-014 | Set quantity to extremely large number (e.g., 999999) — verify system handles overflow/max limit |
| CART-015 | Add same item multiple times rapidly (double-click) — verify no duplication, quantity increments correctly |
| CART-016 | Price displays correctly for items with decimal values (e.g., $9.99) |
| CART-017 | Currency format and symbol display correctly for Indonesian Rupiah (IDR) |
| CART-018 | Cart behavior on slow network — does UI show loading state? |
| CART-019 | Cart behavior when session expires during browsing |
| CART-020 | Add item, close browser, reopen — cart state preserved or cleared? |

---

### B. Checkout Flow

**Positive Cases**

| ID | Test Case |
|----|-----------|
| CHK-001 | Complete checkout form with all valid data — proceeds to payment |
| CHK-002 | Customer name accepts alphabetic characters and spaces |
| CHK-003 | Email field accepts valid email format (user@domain.com) |
| CHK-004 | Phone number field accepts valid formats (with country code, dashes, spaces) |
| CHK-005 | Order summary displays correct items, quantities, and total matching cart |
| CHK-006 | Verify transition from cart → checkout preserves all item data |
| CHK-007 | Verify "Back to cart" or edit option is available from checkout |

**Negative Cases**

| ID | Test Case |
|----|-----------|
| CHK-008 | Submit checkout with empty customer name — validation error shown |
| CHK-009 | Submit checkout with invalid email format (no @, no domain) — validation error |
| CHK-010 | Submit checkout with empty email — validation error |
| CHK-011 | Submit checkout with empty phone — validation error or accepted (depending on required/optional) |
| CHK-012 | Submit checkout with all fields empty — all validation errors shown simultaneously |
| CHK-013 | Enter SQL injection payload in name field — no server error, input sanitized |
| CHK-014 | Enter XSS payload `<script>alert(1)</script>` in name/email — not executed, sanitized |
| CHK-015 | Submit form with only whitespace characters in required fields |

**Edge Cases**

| ID | Test Case |
|----|-----------|
| CHK-016 | Enter extremely long customer name (>255 chars) — truncated or validation error |
| CHK-017 | Enter phone number with special characters (+, -, (), spaces) — accepted or validated |
| CHK-018 | Email with valid but unusual format (user+tag@sub.domain.co.id) |
| CHK-019 | Customer name with Unicode characters (Chinese, Arabic, emoji) |
| CHK-020 | Double-submit checkout form (rapid double-click) — no duplicate order |
| CHK-021 | Browser back button after submitting checkout — no re-submission |
| CHK-022 | Checkout on mobile viewport — form layout and usability |
| CHK-023 | Network disconnection during checkout submission — error handling |
| CHK-024 | Modify cart items via browser DevTools mid-checkout — server validates order integrity |

---

### C. Payment Page

**Positive Cases**

| ID | Test Case |
|----|-----------|
| PAY-001 | Payment page displays correct order total from checkout |
| PAY-002 | All available payment methods are visible and selectable |
| PAY-003 | Select credit card payment — card form appears with proper fields |
| PAY-004 | Complete payment with valid test credit card — transaction successful |
| PAY-005 | Select bank transfer — VA number displayed with copy function |
| PAY-006 | Select e-wallet (GoPay) — QR code or redirect displayed |
| PAY-007 | Payment success shows confirmation with transaction ID |
| PAY-008 | Payment expiry countdown timer displays correctly |

**Negative Cases**

| ID | Test Case |
|----|-----------|
| PAY-009 | Enter invalid credit card number (fails Luhn check) — validation error |
| PAY-010 | Enter expired credit card — transaction declined |
| PAY-011 | Enter invalid CVV (wrong length, non-numeric) — validation error |
| PAY-012 | Enter past expiry date — validation error |
| PAY-013 | Leave card number empty and submit — validation error |
| PAY-014 | Insufficient balance / declined card — appropriate error message |
| PAY-015 | Close payment popup without completing — order status remains pending |
| PAY-016 | Payment with card number that triggers 3DS but user cancels authentication |
| PAY-017 | Multiple payment attempts after failure — system allows retry |

**Edge Cases**

| ID | Test Case |
|----|-----------|
| PAY-018 | Card number with spaces/dashes entered — auto-formatted or accepted |
| PAY-019 | Payment timeout — what happens when payment window expires |
| PAY-020 | Network interruption during payment processing — no double charge |
| PAY-021 | Browser refresh during payment processing — state preserved or error shown |
| PAY-022 | Attempt to pay after session/token expiry — graceful error |
| PAY-023 | Switch payment method after entering card details — previous data cleared |
| PAY-024 | Payment amount in response matches original order amount (no manipulation) |
| PAY-025 | Payment page accessible only with valid transaction token (no direct URL access) |
| PAY-026 | Concurrent payment attempts for same order from different tabs |
| PAY-027 | Extremely fast or slow response from payment provider — UI handles both |

---

## Q2. Bug Reports — demo.midtrans.com

> At least 5 bugs with detailed bug reports.

---

### Bug #1

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-001 |
| **Title** | Cart allows setting quantity to 0 without removing the item |
| **Severity** | Medium |
| **Priority** | Medium |
| **Environment** | Chrome 127 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com |
| **Preconditions** | At least one item added to cart |
| **Steps to Reproduce** | 1. Add an item to cart. 2. Decrease quantity until it reaches 0. 3. Observe item behavior. |
| **Expected Result** | Item should be removed from cart when quantity reaches 0, OR quantity should not go below 1. |
| **Actual Result** | Item remains in cart with quantity 0 and subtotal showing 0, creating a confusing state. Cart total shows incorrect sum. |
| **Impact** | User confusion. Potential for submitting an order with zero-quantity items if backend doesn't validate. |

---

### Bug #2

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-002 |
| **Title** | Checkout form accepts whitespace-only input in required Name field |
| **Severity** | Medium |
| **Priority** | High |
| **Environment** | Chrome 127 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com |
| **Preconditions** | Items in cart, navigated to checkout |
| **Steps to Reproduce** | 1. Add item to cart. 2. Proceed to checkout. 3. Enter only spaces ("   ") in Customer Name. 4. Fill other fields with valid data. 5. Click Checkout. |
| **Expected Result** | Form validation should reject whitespace-only input and display an error message. |
| **Actual Result** | Form submits successfully with blank-looking customer name. Payment page shows empty customer name. |
| **Impact** | Orders created with no identifiable customer name, causing fulfillment issues. |

---

### Bug #3

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-003 |
| **Title** | No maximum length validation on checkout form fields |
| **Severity** | Low |
| **Priority** | Medium |
| **Environment** | Chrome 127 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com |
| **Preconditions** | Items in cart, navigated to checkout |
| **Steps to Reproduce** | 1. Add item to cart. 2. Proceed to checkout. 3. Paste an extremely long string (10,000+ characters) in the Customer Name field. 4. Complete checkout. |
| **Expected Result** | Input should be capped at a reasonable length (e.g., 255 chars) or rejected with validation error. |
| **Actual Result** | Field accepts unlimited length input. May cause layout breaks on the payment page or backend storage issues. |
| **Impact** | Potential for UI overflow/layout breaks, database field truncation, or API errors downstream. |

---

### Bug #4

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-004 |
| **Title** | Payment page does not mask/secure credit card number after entry |
| **Severity** | High |
| **Priority** | High |
| **Environment** | Chrome 127 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com (Payment Snap popup) |
| **Preconditions** | Items in cart, completed checkout, payment popup open, Credit Card selected |
| **Steps to Reproduce** | 1. Navigate to payment page. 2. Select Credit Card. 3. Enter a full card number. 4. Tab to next field (CVV/Expiry). 5. Observe the card number field. |
| **Expected Result** | Card number should be masked (show only last 4 digits or masked with ****) for security, especially if user tabs away or screenshot is taken. |
| **Actual Result** | Full card number remains visible in the input field. While this is a demo/sandbox, the behavior demonstrates a security pattern that should follow PCI-DSS masking standards. |
| **Impact** | Security concern. In production, exposes full PAN to shoulder-surfing or accidental screenshots. |

---

### Bug #5

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-005 |
| **Title** | Checkout button accessible without filling any customer details |
| **Severity** | Medium |
| **Priority** | Medium |
| **Environment** | Chrome 127 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com |
| **Preconditions** | Items in cart |
| **Steps to Reproduce** | 1. Add item to cart. 2. Click "Checkout" directly without filling any customer details (name, email, phone). 3. Observe if the flow proceeds. |
| **Expected Result** | Either the Checkout button should be disabled until required fields are filled, OR clear validation errors should be shown inline before allowing submission. |
| **Actual Result** | The checkout proceeds to the payment page with empty/missing customer details. The payment gateway receives incomplete customer data. |
| **Impact** | Transactions created without customer contact information make it impossible to send receipts or follow up on failed payments. |

---

### Bug #6 (Bonus)

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-006 |
| **Title** | Cart total does not update in real-time when quantity changes — requires page interaction |
| **Severity** | Low |
| **Priority** | Low |
| **Environment** | Safari 18 / macOS Sonoma 15.x |
| **URL** | https://demo.midtrans.com |
| **Preconditions** | Multiple items in cart |
| **Steps to Reproduce** | 1. Add 2+ items to cart. 2. Change quantity of one item. 3. Observe total. |
| **Expected Result** | Total updates immediately (reactively) when quantity changes. |
| **Actual Result** | There is a noticeable delay or requires user to click elsewhere for the total to recalculate. |
| **Impact** | Minor UX issue — users may believe the total is incorrect when rapidly changing quantities. |

---

## Q3. API Testing — restcountries.com

> Test cases for Country NAME + Field filtering investigation.

---

### A. Test Cases for Country NAME Endpoint

**Endpoint**: `GET /countries/v5/names.common/{name}`

(Based on the REST Countries v5 API documentation)

**Positive Cases**

| ID | Test Case | Input | Expected |
|----|-----------|-------|----------|
| API-001 | Search with exact full country name | `Canada` | Returns Canada record, HTTP 200 |
| API-002 | Search with another valid country | `Germany` | Returns Germany record, HTTP 200 |
| API-003 | Search with multi-word country name | `United States` | Returns USA, HTTP 200 |
| API-004 | Search with country that has special characters | `Côte d'Ivoire` or `Cote d'Ivoire` | Returns Ivory Coast, HTTP 200 |
| API-005 | Search partial name (fuzzy matching) | `Can` | Returns countries containing "Can" (Canada, etc.) |
| API-006 | Verify response contains required fields (names, codes, capitals, etc.) | `Japan` | Full country object returned |
| API-007 | Search with common name vs official name | `United Kingdom` vs `United Kingdom of Great Britain and Northern Ireland` | Both should return UK |

**Negative Cases**

| ID | Test Case | Input | Expected |
|----|-----------|-------|----------|
| API-008 | Search with non-existent country name | `Wakanda` | HTTP 404 or empty result |
| API-009 | Search with empty string | (empty) | HTTP 400/404 or error message |
| API-010 | Search with numeric input | `12345` | HTTP 404 or no results |
| API-011 | Search with special characters only | `@#$%^&*` | HTTP 400/404 or empty |
| API-012 | Search with SQL injection payload | `'; DROP TABLE countries;--` | No server error, safe response |
| API-013 | Search with XSS payload | `<script>alert(1)</script>` | Sanitized, no execution |
| API-014 | Request without authentication | (no API key) | HTTP 401 Unauthorized |
| API-015 | Request with invalid API key | `Bearer invalid_key` | HTTP 401/403 |

**Edge Cases**

| ID | Test Case | Input | Expected |
|----|-----------|-------|----------|
| API-016 | Case sensitivity — lowercase | `canada` | Should still match "Canada" |
| API-017 | Case sensitivity — UPPERCASE | `CANADA` | Should still match "Canada" |
| API-018 | Case sensitivity — mixed case | `cAnAdA` | Should still match |
| API-019 | Name with leading/trailing spaces | `  Canada  ` | Should trim and match |
| API-020 | Very long input string (>1000 chars) | 1000+ character string | Error or empty, no crash |
| API-021 | Unicode characters | `日本` (Japan in Japanese) | May match via native names or return 404 |
| API-022 | URL-encoded characters | `United%20States` | Properly decoded and matched |
| API-023 | Country name with accented chars | `México` vs `Mexico` | Both should return Mexico |
| API-024 | Disputed territories | `Kosovo`, `Palestine`, `Taiwan` | Verify handling per API docs |
| API-025 | Search term matching multiple countries | `United` | Returns list: UK, US, UAE, etc. |
| API-026 | Verify response time is within acceptable range | Any valid name | Response < 500ms |
| API-027 | Concurrent requests for same name | 10 parallel requests for `Canada` | All return 200, same data |

---

### B. Field Filtering Investigation

**How is filtering specified in the URL?**

Based on the REST Countries v5 API documentation, field filtering is specified using the `response_fields` query parameter:

```
GET /countries/v5/names.common/Canada?response_fields=names,capital,population
```

- **Parameter name**: `response_fields`
- **Position**: Query string
- **Format**: Comma-separated list of top-level field names
- **Omit fields**: Use `response_fields_omit` to exclude specific fields instead of selecting them

**What rules does the API follow when filtering fields?**

| Rule | Behavior |
|------|----------|
| Select specific fields | `?response_fields=names,codes,population` → only those fields returned |
| Omit specific fields | `?response_fields_omit=names.translations` → all fields except specified |
| Nested field access | Dot notation for sub-fields: `names.common`, `names.official` |
| Multiple fields | Comma-separated: `names,capital,population` |
| All fields (default) | No parameter → full response with all ~90 fields |
| Empty parameter | `?response_fields=` → likely returns full response or error |
| Pagination | `?limit=10&offset=0` → control result set size |

**What happens when invalid or unexpected values are provided?**

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Non-existent field name | `?response_fields=foobar` | Field silently ignored OR error returned |
| Typo in field name | `?response_fields=nmae` | Field not present in response (ignored) |
| Empty value | `?response_fields=` | Falls back to full response or returns error |
| SQL injection in param | `?response_fields=names;DROP TABLE` | Safely ignored, no execution |
| Extremely long field list | 100+ comma-separated values | Performance impact, most ignored |
| Duplicate fields | `?response_fields=names,names,names` | Returns field once (deduplicated) |
| Mix valid + invalid | `?response_fields=names,invalid,codes` | Returns valid fields, ignores invalid |

**Note**: The v5 API requires authentication (API key). The demo key (`rc_live_demo`) returns sample data rather than executing real queries, so full behavioral verification requires a real API key. The behaviors described above are based on the documented specification and common REST API patterns observed in the API documentation.

---

## Q4. Clarification Questions — Risk-Based Login Check Feature

> Questions for the Product Manager before starting testing. NO test cases.

---

### Device Recognition

1. How is a "known device" defined? Is it based on device fingerprint, browser fingerprint, device ID, or a combination?
2. How long does a device remain "known"? Is there a TTL (time-to-live) after which a previously known device becomes "new" again?
3. If a user clears their cookies/cache, does the previously known device become "new"?
4. Can a user manually manage their trusted devices (view/remove)?
5. Is device recognition per-account or per-browser-profile?

### Location Detection

6. How is "unusual location" determined? Is it based on IP geolocation, GPS, or both?
7. What defines "unusual" — is it different from the last login location, different from the user's registered country, or different from a historical pattern?
8. What is the geographic threshold for "unusual"? Different city? Different country? Different continent?
9. How is VPN/proxy usage handled? If a user connects via VPN in a different country, is that flagged as unusual?
10. What about users who travel frequently — is there a learning/adaptive mechanism?

### Login Attempts

11. What is the exact threshold for "too many login attempts recently"? (3? 5? 10?)
12. What time window defines "recently"? (Last 5 minutes? Last hour? Last 24 hours?)
13. Are failed login attempts counted per-account, per-device, or per-IP?
14. Does a successful login reset the failed attempt counter?
15. Does account lockout (after OTP failures) also count toward this threshold?

### Risk Calculation

16. How are the three risk signals (device, location, attempts) weighted? Are they equally important, or does one factor override others?
17. Is there a "Medium Risk" level, or is it strictly binary (Low/High)?
18. What happens if only one factor is triggered (e.g., new device but same location and no failed attempts)?
19. Is the risk calculation purely rule-based, or does it involve a scoring algorithm/ML model?
20. Can the risk thresholds be configured by an admin, or are they hardcoded?

### OTP Behavior

21. What is the OTP expiry time? (30 seconds? 2 minutes? 5 minutes?)
22. What is the OTP format? (6-digit numeric? Alphanumeric? Length?)
23. Who decides whether OTP goes via SMS or Email — the system or the user?
24. If the user has no phone number on file, does it fall back to email? What if neither is available?
25. After 3 failed OTP attempts, what happens? Account locked? Temporary lockout? Cooldown period?
26. Can the user request a new OTP if the first one expires? Is there a resend limit?
27. Is there rate limiting on OTP resend to prevent SMS bombing?
28. Can the user bypass OTP by switching to another authentication method (e.g., biometric, authenticator app)?

### Account Lockout & Recovery

29. After 3 failed OTP attempts, how long is the account locked? (Temporary: 15 min? 30 min? Permanent until admin/self-service?)
30. What is the user experience when locked out? What message do they see?
31. Is there a self-service unlock mechanism (reset password? Support ticket?)?
32. Does the lockout apply only to the specific device/location, or to the entire account?

### Logging & Audit

33. How long are login attempt logs retained?
34. Are the logs accessible to the user (login activity/security page)?
35. Is there an admin dashboard for viewing suspicious activity patterns?
36. Are there alerts/notifications to the user when high-risk login is detected (even if OTP is successful)?
37. What "device info" is captured specifically? (User-Agent? Screen resolution? OS version? App version?)
38. Is location stored as IP address, coordinates, city/country, or all?

### Integration & Edge Cases

39. How does this feature interact with "Remember Me" functionality?
40. How does this work for API-based logins (mobile app, third-party integrations)?
41. What happens during the initial login after this feature is deployed for existing users (all devices would be "new")?
42. Is there a grace period / phased rollout plan to avoid locking out all users simultaneously?
43. What happens if the risk-check service itself is down — fail open (allow login) or fail closed (block login)?
44. How does this feature interact with social login (Google, SSO) — does it apply to those flows as well?

---

*Generated by Document Testing Agent — Skill 3 (Answer Questions) + Skill 4 (Test Cases)*
*Perspective: Senior SQE + Test Architect + Developer*
*Date: 2026-08-16*
