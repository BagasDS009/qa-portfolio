"""Configuration loader — picks environment from ENV variable."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Determine which .env to load: ENV=dev|sit|staging (default: sit)
ENV = os.getenv("ENV", "sit")
env_file = Path(__file__).parent / f".env.{ENV}"

if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(Path(__file__).parent / ".env.sit")


class Config:
    """Centralized configuration from environment variables."""

    BASE_URL: str = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOWMO: int = int(os.getenv("SLOWMO", "0"))
    SCREENSHOT_DIR: str = os.getenv("SCREENSHOT_DIR", "reports/screenshots")
    BROWSER: str = os.getenv("BROWSER", "firefox")
