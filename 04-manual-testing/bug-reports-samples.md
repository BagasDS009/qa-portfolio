# Bug Report Samples

> Professional bug reports demonstrating proper severity classification, clear reproduction steps, and root cause analysis. Each report follows a consistent format suitable for Jira, Azure DevOps, or any defect tracking tool.

---

## BUG-101: Payment fails silently when credit card expires during checkout

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-101 |
| **Title** | Payment fails silently when credit card expires during checkout |
| **Severity** | S1 - Critical |
| **Priority** | P1 - Highest |
| **Module** | Checkout → Payment |
| **Status** | Open |
| **Reported By** | Bagas Dimas Saputra |
| **Date** | 2026-08-10 |
| **Environment** | Staging (v3.2.1) |
| **Browser/Device** | Chrome 127 / macOS |
| **Assignee** | Backend Team |

### Description
When a user's credit card expires between adding items to cart and completing payment, the payment API returns a 402 error but the UI shows a blank screen with no error message. The user's cart is cleared but no order is created, resulting in lost sale.

### Steps to Reproduce
1. Login with user account that has a card expiring this month
2. Add any product to cart
3. Proceed to checkout
4. Wait until card expiry date passes (or simulate with test card `4000000000004001`)
5. Click "Place Order"
6. **Observe:** Blank white screen, no error message displayed

### Expected Result
- Display clear error message: "Payment declined — your card has expired. Please update your payment method."
- Retain items in cart
- Redirect to payment method update page

### Actual Result
- Blank white screen (no UI feedback)
- Cart is emptied
- No order created
- Console shows: `Uncaught TypeError: Cannot read property 'status' of undefined`

### Evidence
```
Console Error:
  payment-handler.js:142 - Uncaught TypeError: Cannot read property 'status' of undefined
  
Network Tab:
  POST /api/payments → 402 Payment Required
  Response body: {"error": "card_expired", "message": "Your card ending in 4001 has expired"}
```

### Impact
- Users lose their cart contents without explanation
- Potential revenue loss (user may not re-attempt purchase)
- Support tickets likely increase

### Root Cause Analysis
The `payment-handler.js` line 142 expects `response.data.status` but the 402 error response structure has `response.error` instead. The error boundary doesn't catch this exception type.

### Suggested Fix
Add try-catch in `handlePaymentResponse()` and render the API error message to the user. Preserve cart state on payment failure.

---

## BUG-102: Search results show deleted products for 5 minutes after deletion

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-102 |
| **Title** | Search results show deleted products for ~5 minutes after admin deletion |
| **Severity** | S2 - Major |
| **Priority** | P2 - High |
| **Module** | Search / Product Catalog |
| **Status** | In Progress |
| **Reported By** | Bagas Dimas Saputra |
| **Date** | 2026-08-08 |
| **Environment** | Staging (v3.2.1) |
| **Browser/Device** | Firefox 128 / Ubuntu |

### Description
After an admin deletes a product, the product continues to appear in search results for approximately 5 minutes. Clicking on the deleted product's link results in a 404 error page.

### Steps to Reproduce
1. Login as admin → Navigate to Product Management
2. Note the name of any product (e.g., "Blue Wireless Headphones")
3. Delete the product → Confirm deletion
4. Immediately search for "Blue Wireless Headphones" as a regular user
5. **Observe:** Product still appears in search results
6. Click on the product link
7. **Observe:** 404 error page

### Expected Result
- Deleted products should not appear in search results within 30 seconds
- Or: Show a graceful "Product no longer available" message if clicked

### Actual Result
- Product remains in search results for ~5 minutes (cache TTL)
- Clicking leads to raw 404 error page (not user-friendly)

### Evidence
- Tested 5 times: average disappearance time = 4 min 52 sec
- Redis cache key `search:index:*` still contains deleted product ID after deletion

### Root Cause Analysis
Search index uses Redis cache with 5-minute TTL. Product deletion does not invalidate the search cache. The cache needs explicit invalidation on product CRUD operations.

### Suggested Fix
1. Invalidate search cache keys on product deletion
2. Add a soft-delete check in search results rendering (defensive)
3. Replace raw 404 with "Product unavailable" page

---

## BUG-103: Mobile hamburger menu overlaps with notification badge

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-103 |
| **Title** | Hamburger menu icon overlaps with notification badge on mobile (< 375px) |
| **Severity** | S3 - Minor |
| **Priority** | P3 - Medium |
| **Module** | UI / Navigation |
| **Status** | Open |
| **Reported By** | Bagas Dimas Saputra |
| **Date** | 2026-08-09 |
| **Environment** | Staging (v3.2.1) |
| **Device** | iPhone SE (375×667), Samsung Galaxy A10 (360×740) |

### Description
On devices with viewport width ≤ 375px, the hamburger menu icon visually overlaps with the notification badge, making both elements difficult to tap accurately.

### Steps to Reproduce
1. Open application on device with viewport ≤ 375px (or use Chrome DevTools → iPhone SE)
2. Login with any account that has notifications
3. **Observe:** Hamburger menu (☰) and notification badge (🔴) overlap by ~8px

### Expected Result
- Both elements should have at least 8px gap between them
- Both elements should meet WCAG 2.2 target size (minimum 24×24px touch target)

### Actual Result
- Elements overlap by ~8px
- Tapping hamburger sometimes triggers notification dropdown instead

### Evidence
Screenshot attached showing overlap on iPhone SE viewport.

### Suggested Fix
```css
/* Add margin-right to hamburger or reduce notification badge position */
.nav-hamburger {
    margin-right: 12px; /* was 4px */
}
```

---

## BUG-104: "Remember Me" checkbox has no effect on session duration

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-104 |
| **Title** | "Remember Me" checkbox does not extend session beyond 30 minutes |
| **Severity** | S3 - Minor |
| **Priority** | P3 - Medium |
| **Module** | Authentication |
| **Status** | Verified |
| **Reported By** | Bagas Dimas Saputra |
| **Date** | 2026-08-07 |
| **Environment** | Staging + Production |

### Description
The "Remember Me" checkbox on the login page is non-functional. Whether checked or unchecked, the session always expires after 30 minutes. Users with "Remember Me" selected expect to remain logged in for 7-30 days.

### Steps to Reproduce
1. Navigate to login page
2. Enter valid credentials
3. Check "Remember Me" checkbox
4. Click Login
5. Wait 31 minutes (or set system clock forward)
6. Refresh any authenticated page
7. **Observe:** Redirected to login page (session expired)

### Expected Result
- Without "Remember Me": session = 30 min (correct)
- With "Remember Me": session = 30 days (using persistent cookie/token)

### Actual Result
- Session always expires at 30 minutes regardless of checkbox state
- No persistent token cookie is set when "Remember Me" is checked
- `document.cookie` shows only session cookie (`session_id=...`), no `remember_token`

### Root Cause Analysis
The backend `/api/auth/login` endpoint ignores the `rememberMe: true` parameter. The JWT is always issued with 30-minute expiry regardless.

---

## BUG-105: Product image alt text missing — accessibility violation

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-105 |
| **Title** | Product images missing alt text (WCAG 2.1 Level A violation) |
| **Severity** | S4 - Trivial (but compliance risk) |
| **Priority** | P2 - High (legal compliance) |
| **Module** | Product Catalog / Accessibility |
| **Status** | Open |
| **Reported By** | Bagas Dimas Saputra |
| **Date** | 2026-08-11 |
| **Environment** | Production |

### Description
All product images on the catalog and detail pages are rendered without `alt` attributes. This is a WCAG 2.1 Level A violation (Success Criterion 1.1.1 — Non-text Content) and makes the site inaccessible to screen reader users.

### Steps to Reproduce
1. Open any product listing page
2. Inspect product image elements in DevTools
3. **Observe:** `<img src="..." class="product-img">` — no `alt` attribute

### Expected Result
```html
<img src="/images/product-123.jpg" alt="Blue Wireless Headphones - Sony WH-1000XM5" class="product-img">
```

### Actual Result
```html
<img src="/images/product-123.jpg" class="product-img">
```

### Impact
- Screen reader users cannot identify products (announces "image" with no context)
- Potential legal liability (ADA compliance in US, EN 301 549 in EU)
- SEO penalty (Google ranks alt text for image search)

### Affected Pages
- `/products` — 48 images without alt text
- `/products/:id` — main product image + gallery images
- `/cart` — cart item thumbnails

### Suggested Fix
Populate `alt` from product `name` field in database:
```jsx
<img src={product.imageUrl} alt={product.name} className="product-img" />
```

---

## Summary Statistics

| Severity | Count | Target SLA |
|----------|:-----:|-----------|
| S1 - Critical | 1 | Fix within 4 hours |
| S2 - Major | 1 | Fix within 24 hours |
| S3 - Minor | 2 | Fix within current sprint |
| S4 - Trivial | 1 | Backlog (but P2 due to compliance) |

---

*These reports demonstrate structured defect reporting with clear impact analysis, reproducible steps, root cause hypothesis, and suggested fixes.*
