"""User credentials and login test data for KAI Booking."""

VALID_USER = {
    "username": "testuser@gmail.com",   # Replace with actual test account
    "password": "TestPassword123!",
}

INVALID_LOGIN = {
    "wrong_password": {"username": "testuser@gmail.com", "password": "WrongPass!"},
    "unregistered": {"username": "nobody@fake.com", "password": "fake123"},
    "empty_both": {"username": "", "password": ""},
    "empty_username": {"username": "", "password": "test123"},
    "empty_password": {"username": "testuser@gmail.com", "password": ""},
    "sql_injection": {"username": "' OR '1'='1' --", "password": "test"},
    "xss_attempt": {"username": "<script>alert(1)</script>", "password": "test"},
}
