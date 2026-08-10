"""Helper utility functions for test automation."""

import os
import random
import string
from datetime import datetime, timedelta


def get_future_date(days_ahead: int = 7) -> str:
    """Get a future date in YYYY-MM-DD format."""
    future = datetime.now() + timedelta(days=days_ahead)
    return future.strftime("%Y-%m-%d")


def get_timestamp() -> str:
    """Get current timestamp string for unique naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_random_string(length: int = 8) -> str:
    """Generate random alphanumeric string."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_phone() -> str:
    """Generate random Indonesian phone number."""
    return f"08{random.randint(1000000000, 9999999999)}"


def generate_random_ktp() -> str:
    """Generate random 16-digit KTP number."""
    return "".join([str(random.randint(0, 9)) for _ in range(16)])


def ensure_dir(directory: str):
    """Create directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)
