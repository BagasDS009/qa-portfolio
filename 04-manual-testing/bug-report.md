# Bug Report

---

## BUG-001: Order confirmation email not sent after successful checkout

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-001 |
| **Title** | Order confirmation email not sent after successful checkout |
| **Module** | Checkout / Email |
| **Severity** | Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Reported By** | QA Engineer |
| **Reported Date** | 2024-01-15 |
| **Environment** | Staging (v2.1.0) |
| **Browser** | Chrome 120 |

### Steps to Reproduce
1. Login with valid credentials
2. Add any product to cart
3. Proceed to checkout
4. Fill shipping information
5. Complete payment
6. Check registered email inbox

### Expected Result
Order confirmation email should be received within 5 minutes after successful order placement.

### Actual Result
No confirmation email received after 10+ minutes. Order is created successfully in the system.

### Attachments
- Screenshot: Order success page
- Log: Email service logs showing no trigger

---

## BUG-002: Cart quantity allows negative values

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-002 |
| **Title** | Cart quantity field accepts negative numbers |
| **Module** | Shopping Cart |
| **Severity** | High |
| **Priority** | P1 |
| **Status** | Fixed |
| **Reported By** | QA Engineer |
| **Reported Date** | 2024-01-12 |
| **Fixed Date** | 2024-01-14 |
| **Environment** | Staging (v2.1.0) |
| **Browser** | Chrome 120, Firefox 121 |

### Steps to Reproduce
1. Login and add product to cart
2. Go to cart page
3. Edit quantity field manually
4. Enter -1 as quantity
5. Click Update

### Expected Result
System should validate input and only accept positive integers (min: 1).

### Actual Result
Negative value is accepted, resulting in negative total price displayed.

### Attachments
- Screenshot: Cart showing -1 quantity with negative price

---

## BUG-003: Search returns no results for partial product name

| Field | Details |
|-------|---------|
| **Bug ID** | BUG-003 |
| **Title** | Search does not support partial keyword matching |
| **Module** | Product Search |
| **Severity** | Low |
| **Priority** | P3 |
| **Status** | Open |
| **Reported By** | QA Engineer |
| **Reported Date** | 2024-01-16 |
| **Environment** | Staging (v2.1.0) |

### Steps to Reproduce
1. Navigate to products page
2. Type "Lap" in search bar (partial word for "Laptop")
3. Press Enter

### Expected Result
Products containing "Lap" should be displayed (e.g., "Laptop Pro", "Laptop Air").

### Actual Result
"No results found" message displayed. Only exact full-word matches work.
