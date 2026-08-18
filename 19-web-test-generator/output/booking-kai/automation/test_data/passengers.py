"""Passenger and contact person test data for KAI Booking."""

VALID_CONTACT = {
    "name": "Test Automation",
    "phone": "081234567890",
    "email": "testkai@gmail.com",
    "id_number": "3201234567890001",  # Valid NIK: 16 digits
}

VALID_PASSENGER = {
    "name": "Penumpang Satu",
    "id_number": "3201234567890002",
}

INVALID_PASSENGER = {
    "empty_name": {"name": "", "id_number": "3201234567890001"},
    "empty_id": {"name": "Test User", "id_number": ""},
    "short_id": {"name": "Test User", "id_number": "12345"},
    "alpha_id": {"name": "Test User", "id_number": "ABCDEFGHIJKLMNOP"},
    "empty_email": {"name": "Test", "phone": "081234567890", "email": ""},
}

BOUNDARY_DATA = {
    "nik_15_digits": "320123456789000",
    "nik_17_digits": "32012345678900012",
    "nik_valid_16": "3201234567890001",
    "xss_name": "<script>alert(1)</script>",
    "sql_name": "'; DROP TABLE users; --",
}
