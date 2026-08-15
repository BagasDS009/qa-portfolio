"""Configuration management for test environment."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Test configuration loaded from environment variables."""

    BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
    API_URL = os.getenv("API_URL", "https://api.practicesoftwaretesting.com")

    # Test accounts
    CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "customer@practicesoftwaretesting.com")
    CUSTOMER_PASSWORD = os.getenv("CUSTOMER_PASSWORD", "welcome01")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@practicesoftwaretesting.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "welcome01")

    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOWMO = int(os.getenv("SLOWMO", "0"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

    # Directories
    SCREENSHOT_DIR = "reports/screenshots"
