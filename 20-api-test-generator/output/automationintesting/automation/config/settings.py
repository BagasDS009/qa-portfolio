"""Configuration loader — reads from .env file based on ENV variable."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Determine environment and load corresponding .env
ENV = os.getenv("ENV", "sit")
env_file = Path(__file__).parent / f".env.{ENV}"

if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(Path(__file__).parent / ".env.sit")


class Config:
    """Application configuration loaded from environment."""

    BASE_URL: str = os.getenv("BASE_URL", "https://automationintesting.online/api")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "password")
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    RESPONSE_TIME_BUDGET_MS: int = int(os.getenv("RESPONSE_TIME_BUDGET_MS", "5000"))
    ENV: str = ENV
