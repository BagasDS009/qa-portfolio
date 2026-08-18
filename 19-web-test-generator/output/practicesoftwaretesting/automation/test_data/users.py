"""User credential test data for Practice Software Testing (Toolshop)."""

import time

VALID_CUSTOMER = {
    "email": "customer@practicesoftwaretesting.com",
    "password": "welcome01",
}

VALID_ADMIN = {
    "email": "admin@practicesoftwaretesting.com",
    "password": "welcome01",
}

INVALID_CREDENTIALS = {
    "wrong_password": {"email": "customer@practicesoftwaretesting.com", "password": "WrongPass123!"},
    "unregistered": {"email": "nobody@nonexistent.com", "password": "test123"},
    "empty_email": {"email": "", "password": "welcome01"},
    "empty_password": {"email": "customer@practicesoftwaretesting.com", "password": ""},
    "empty_both": {"email": "", "password": ""},
    "invalid_format": {"email": "not-an-email", "password": "welcome01"},
    "sql_injection": {"email": "' OR '1'='1' --", "password": "test"},
    "xss_attempt": {"email": "<script>alert(1)</script>", "password": "test"},
}


def generate_unique_email() -> str:
    """Generate unique email for registration tests."""
    return f"test_{int(time.time())}@test.com"


VALID_REGISTRATION = {
    "first_name": "Test",
    "last_name": "Automation",
    "dob": "1990-05-15",
    "street": "123 Test Street",
    "city": "Jakarta",
    "state": "DKI Jakarta",
    "country": "ID",
    "postcode": "12345",
    "phone": "081234567890",
    "password": "T3stAut0m@te2026!",  # Unique password not in data leak databases
    "house_number": "42",
}
