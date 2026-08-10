"""
Pytest configuration and shared fixtures for KAI Booking automation tests.
Anti-detection: stealth mode + fresh browser per test + human-like delays.
"""

import os
import random
from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright, Page, Browser
from playwright_stealth import Stealth

from pages.login_page import LoginPage
from tests.test_data import (
    CONTACT_PERSON,
    PASSENGER_1,
    VALID_SEARCH,
)


# ============================================================================
# Configuration (from .env)
# ============================================================================

BASE_URL = os.getenv("BASE_URL", "https://booking.kai.id")
VALID_USER = os.getenv("KAI_USER", "testuser@example.com")
VALID_PASSWORD = os.getenv("KAI_PASSWORD", "TestPassword123!")


# ============================================================================
# Pytest Hooks - Override default playwright fixtures
# ============================================================================

def pytest_addoption(parser):
    """Custom CLI options."""
    pass


# ============================================================================
# Fixtures - Fresh Browser Per Test (close & reopen to avoid detection)
# ============================================================================

@pytest.fixture
def browser():
    """Launch a fresh browser for each test, then close it completely."""
    with sync_playwright() as p:
        bwr = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
            ],
        )
        yield bwr
        bwr.close()


@pytest.fixture
def page(browser: Browser):
    """Create a fresh page with stealth + anti-detection per test."""
    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        locale="id-ID",
        timezone_id="Asia/Jakarta",
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        java_script_enabled=True,
        ignore_https_errors=True,
    )
    pg = context.new_page()

    # Apply stealth
    Stealth().apply_stealth_sync(pg)

    # Initial delay before navigating (look human)
    pg.wait_for_timeout(random.randint(2000, 4000))

    yield pg

    # Cleanup: close context (fresh for next test)
    context.close()


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
    """Perform login with human-like delays."""
    login_page = LoginPage(page)
    login_page.login(
        username=credentials["valid_user"],
        password=credentials["valid_password"],
    )
    # Extra wait after login to let page fully load
    page.wait_for_timeout(random.randint(3000, 5000))
    assert login_page.is_logged_in(), "Pre-test login failed"
    yield


# ============================================================================
# Fixtures - Test Data
# ============================================================================

@pytest.fixture
def search_data():
    """Provide train search data."""
    return VALID_SEARCH


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
    """Capture screenshot on test failure and attach to Allure report."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        page.screenshot(path=screenshot_path)

        # Attach screenshot to Allure report
        import allure
        allure.attach.file(
            screenshot_path,
            name=f"Screenshot - {test_name}",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate Allure report after test session completes."""
    import subprocess
    import shutil

    allure_results = "reports/allure-results"
    allure_report = "reports/allure-report"

    # Check if allure CLI is available
    if shutil.which("allure") is None:
        print("\n⚠️  Allure CLI not installed. Install with: brew install allure")
        print(f"   Run manually: allure serve {allure_results}")
        return

    # Generate static report
    try:
        subprocess.run(
            ["allure", "generate", allure_results, "-o", allure_report, "--clean"],
            check=True,
            capture_output=True,
        )
        report_path = os.path.abspath(f"{allure_report}/index.html")
        print(f"\n{'='*70}")
        print(f"📊 ALLURE REPORT GENERATED")
        print(f"{'='*70}")
        print(f"   📁 file://{report_path}")
        print(f"   🌐 Run: allure open {allure_report}")
        print(f"{'='*70}\n")
    except subprocess.CalledProcessError:
        print(f"\n⚠️  Failed to generate Allure report.")
        print(f"   Run manually: allure serve {allure_results}")
