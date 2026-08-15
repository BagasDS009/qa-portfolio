"""Helper utility functions for test automation."""

import random
import string
from datetime import datetime, timedelta


def get_timestamp() -> str:
    """Get current timestamp string for unique naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_random_email() -> str:
    """Generate a unique random email for registration tests."""
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"testuser_{suffix}@example.com"


def generate_random_string(length: int = 8) -> str:
    """Generate random alphanumeric string."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_phone() -> str:
    """Generate random phone number."""
    return f"08{random.randint(100000000, 999999999)}"


def get_future_date(days_ahead: int = 7) -> str:
    """Get a future date in YYYY-MM-DD format."""
    future = datetime.now() + timedelta(days=days_ahead)
    return future.strftime("%Y-%m-%d")
