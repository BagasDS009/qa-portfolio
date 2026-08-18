"""Root conftest.py — Allure report, environment info, fixture registration."""

import os
import sys
import shutil

import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import Config  # noqa: E402

# Register all fixture modules
pytest_plugins = [
    "fixtures.auth_fixtures",
    "fixtures.room_fixtures",
    "fixtures.booking_fixtures",
    "fixtures.message_fixtures",
    "fixtures.branding_fixtures",
    "fixtures.report_fixtures",
]


def pytest_configure(config):
    """Write environment.properties for Allure report."""
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)
        env_file = os.path.join(allure_dir, "environment.properties")
        with open(env_file, "w") as f:
            f.write(f"Base.URL={Config.BASE_URL}\n")
            f.write(f"Environment={Config.ENV}\n")
            f.write(f"Timeout={Config.TIMEOUT}s\n")
            f.write(f"Response.Budget={Config.RESPONSE_TIME_BUDGET_MS}ms\n")


def pytest_sessionfinish(session, exitstatus):
    """Print Allure report command after test run."""
    allure_results = os.path.join(os.path.dirname(__file__), "reports", "allure-results")
    if not os.path.isdir(allure_results):
        return

    allure_bin = shutil.which("allure")
    if not allure_bin:
        print("\n⚠️  Install allure-commandline: brew install allure")
        return

    print(f"\n📊 View report: allure serve {allure_results}")
