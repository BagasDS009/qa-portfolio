"""Configuration management for test environment."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Test configuration loaded from environment variables."""

    BASE_URL = os.getenv("BASE_URL", "https://booking.kai.id")
    USERNAME = os.getenv("KAI_USER", "testuser@example.com")
    PASSWORD = os.getenv("KAI_PASSWORD", "TestPassword123!")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "reports/screenshots")
    SLOWMO = int(os.getenv("SLOWMO", "0"))

    # Test data defaults
    DEFAULT_ORIGIN = "GAMBIR"
    DEFAULT_DESTINATION = "BANDUNG"
