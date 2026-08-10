"""
Pytest configuration and shared fixtures for KAI Booking automation tests.
"""

import os
from datetime import datetime

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from tests.test_data import (
    CONTACT_PERSON,
    PASSENGER_1,
    VALID_SEARCH,
    get_departure_date,
)


# ============================================================================
# Configuration (from .env)
# ============================================================================

BASE_URL = os.getenv("BASE_URL", "https://booking.kai.id")
VALID_USER = os.getenv("KAI_USER", "testuser@example.com")
VALID_PASSWORD = os.getenv("KAI_PASSWORD", "TestPassword123!")


# ============================================================================
# Pytest Hooks
# ============================================================================


def pytest_addoption(parser):
    """Custom CLI options (--base-url already registered by pytest-playwright)."""
    pass


# ============================================================================
# Fixtures - Browser
# ============================================================================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "id-ID",
        "timezone_id": "Asia/Jakarta",
    }


# ============================================================================
# Fixtures - Authentication
# ============================================================================


@pytest.fixture
def credentials():
    """Provide login credentials from environment."""
    return {
        "valid_user": VALID_USER,
        "valid_password": VALID_PASSWORD,
    }


@pytest.fixture
def login(page: Page, credentials):
    """Perform login before test."""
    login_page = LoginPage(page)
    login_page.login(
        username=credentials["valid_user"],
        password=credentials["valid_password"],
    )
    assert login_page.is_logged_in(), "Pre-test login failed"
    yield


# ============================================================================
# Fixtures - Test Data (centralized from test_data.py)
# ============================================================================


@pytest.fixture
def search_data():
    """Provide train search data with fresh departure date."""
    return {
        **VALID_SEARCH,
        "departure_date": get_departure_date(7),
    }


@pytest.fixture
def passenger_data():
    """Provide passenger form data."""
    return {
        "contact_name": CONTACT_PERSON["name"],
        "contact_phone": CONTACT_PERSON["phone"],
        "contact_email": CONTACT_PERSON["email"],
        "passenger_name": PASSENGER_1["name"],
        "id_type": PASSENGER_1["id_type"],
        "id_number": PASSENGER_1["id_number"],
        "passenger_phone": PASSENGER_1["phone"],
    }


# ============================================================================
# Fixtures - Reporting
# ============================================================================


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Capture screenshot on test failure."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        page.screenshot(path=f"{screenshot_dir}/{test_name}_{timestamp}.png")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
