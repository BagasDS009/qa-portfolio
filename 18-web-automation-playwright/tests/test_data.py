"""
Centralized test data for Practice Software Testing (Toolshop) automation.
All test data is maintained here for easy management.
"""


# ============================================================
# User Credentials
# ============================================================
VALID_CUSTOMER = {
    "email": "customer@practicesoftwaretesting.com",
    "password": "welcome01",
}

VALID_ADMIN = {
    "email": "admin@practicesoftwaretesting.com",
    "password": "welcome01",
}

INVALID_CREDENTIALS = {
    "wrong_password": {
        "email": "customer@practicesoftwaretesting.com",
        "password": "WrongPassword123!",
    },
    "unregistered_email": {
        "email": "nobody@nonexistent.com",
        "password": "SomePassword123!",
    },
    "empty": {
        "email": "",
        "password": "",
    },
}


# ============================================================
# Registration Data
# ============================================================
NEW_USER = {
    "first_name": "Test",
    "last_name": "Automation",
    "dob": "1990-01-15",
    "address": "123 Automation Street",
    "city": "Jakarta",
    "state": "DKI Jakarta",
    "country": "ID",
    "postcode": "12345",
    "phone": "081234567890",
    "password": "Welcome01!",
}


# ============================================================
# Product Search & Filter
# ============================================================
SEARCH_QUERIES = {
    "valid": "pliers",
    "valid_alt": "hammer",
    "no_results": "xyznonexistent123",
}

CATEGORIES = {
    "hand_tools": "Hand Tools",
    "power_tools": "Power Tools",
    "other": "Other",
}

SORT_OPTIONS = {
    "name_asc": "Name (A - Z)",
    "name_desc": "Name (Z - A)",
    "price_asc": "Price (Low - High)",
    "price_desc": "Price (High - Low)",
}


# ============================================================
# Checkout / Billing Address
# ============================================================
BILLING_ADDRESS = {
    "street": "123 Test Street",
    "house_number": "42",
    "city": "Amsterdam",
    "state": "Noord-Holland",
    "country": "NL",
    "postcode": "1234AB",
}

PAYMENT_METHODS = {
    "bank_transfer": "Bank Transfer",
    "cash_on_delivery": "Cash on Delivery",
    "credit_card": "Credit Card",
    "buy_now_pay_later": "Buy Now Pay Later",
    "gift_card": "Gift Card",
}


# ============================================================
# Contact Form Data
# ============================================================
VALID_CONTACT = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "subject": "Webmaster",
    "message": "This is an automated test message for the contact form. "
               "Please disregard this submission.",
}

INVALID_CONTACT = {
    "empty": {
        "first_name": "",
        "last_name": "",
        "email": "",
        "subject": "",
        "message": "",
    },
    "invalid_email": {
        "first_name": "Test",
        "last_name": "User",
        "email": "not-an-email",
        "subject": "Webmaster",
        "message": "Test message with invalid email format.",
    },
}
