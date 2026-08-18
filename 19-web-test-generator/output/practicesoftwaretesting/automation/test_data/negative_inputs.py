"""Negative, boundary, and security test data."""

BOUNDARY_DATA = {
    "min_password": "Aa1!",
    "short_password": "Ab1",
    "weak_password": "password",
    "max_length_255": "A" * 255,
    "max_length_256": "A" * 256,
    "unicode_name": "Te\u0301st U\u0308ser",
    "emoji_name": "Test 🔧",
    "html_injection": "<h1>Injected</h1>",
    "xss_script": "<script>alert('XSS')</script>",
    "sql_injection": "'; DROP TABLE users; --",
    "path_traversal": "../../etc/passwd",
    "very_long_email": "a" * 200 + "@test.com",
}

CONTACT_NEGATIVE = {
    "short_message": "Too short",
    "valid_long_message": (
        "This is a test message that exceeds the minimum fifty character "
        "requirement for the contact form validation rule."
    ),
}
