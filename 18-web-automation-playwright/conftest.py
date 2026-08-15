"""
Pytest configuration and shared fixtures for Toolshop automation tests.
Uses pytest-playwright for browser lifecycle management.
"""

import os
from datetime import datetime

import pytest
from playwright.sync_api import Page

# Config import triggers load_dotenv()
from utils.config import Config
from pages.login_page import LoginPage
from tests.test_data import VALID_CUSTOMER, BILLING_ADDRESS


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Set Allure environment properties."""
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)
        env_file = os.path.join(allure_dir, "environment.properties")
        with open(env_file, "w") as f:
            f.write(f"Base.URL={Config.BASE_URL}\n")
            f.write(f"Browser=Firefox\n")
            f.write(f"Headless={Config.HEADLESS}\n")


# ============================================================================
# Fixtures - Browser Configuration (overrides pytest-playwright defaults)
# ============================================================================

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Override pytest-playwright browser launch args."""
    return {
        "headless": Config.HEADLESS or os.getenv("CI", "false").lower() == "true",
        "slow_mo": Config.SLOWMO,
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Override pytest-playwright browser context args."""
    return {
        "viewport": {"width": 1366, "height": 768},
        "locale": "en-US",
        "timezone_id": "Europe/Amsterdam",
        "ignore_https_errors": True,
    }


# ============================================================================
# Fixtures - Authentication
# ============================================================================

@pytest.fixture
def logged_in_page(page: Page):
    """Provide a page that is already logged in as customer."""
    login_page = LoginPage(page)
    login_page.login(
        email=VALID_CUSTOMER["email"],
        password=VALID_CUSTOMER["password"],
    )
    page.wait_for_load_state("networkidle")
    yield page


# ============================================================================
# Fixtures - Test Data
# ============================================================================

@pytest.fixture
def customer_credentials():
    """Provide customer login credentials."""
    return VALID_CUSTOMER


@pytest.fixture
def billing_address():
    """Provide billing address for checkout."""
    return BILLING_ADDRESS


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
        screenshot_dir = Config.SCREENSHOT_DIR
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        page.screenshot(path=screenshot_path)

        try:
            import allure
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot - {test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except ImportError:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
