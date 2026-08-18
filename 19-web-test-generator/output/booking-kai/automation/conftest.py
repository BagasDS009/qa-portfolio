"""Pytest configuration, fixtures, and hooks for KAI Booking tests."""

import os
import sys
from datetime import datetime

import pytest
from playwright.sync_api import Page
from playwright_stealth import Stealth

sys.path.insert(0, os.path.dirname(__file__))

from config.settings import Config

# Register booking flow fixtures (available to all tests)
pytest_plugins = ["fixtures.booking_flow"]


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)
        with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
            f.write(f"Base.URL={Config.BASE_URL}\n")
            f.write(f"Browser={Config.BROWSER}\n")
            f.write(f"Headless={Config.HEADLESS}\n")


# ============================================================================
# Browser Configuration — with Stealth (anti-bot bypass)
# ============================================================================

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "headless": Config.HEADLESS or os.getenv("CI", "false").lower() == "true",
        "slow_mo": Config.SLOWMO,
    }


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1366, "height": 768},
        "locale": "id-ID",
        "timezone_id": "Asia/Jakarta",
        "ignore_https_errors": True,
        "user_agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }


@pytest.fixture(autouse=True)
def apply_stealth(page: Page):
    """Apply playwright-stealth to every page to bypass bot detection."""
    stealth = Stealth()
    stealth.apply_stealth_sync(page)
    yield


# ============================================================================
# Reporting — Auto-screenshot per step + on failure + auto-serve report
# ============================================================================

@pytest.fixture(autouse=True)
def auto_screenshot_steps(request, page: Page):
    """Capture full-page screenshot after every allure step and on failure."""
    import allure

    _original_step = allure.step

    class ScreenshotStep:
        def __init__(self, title):
            self.title = title
            self._cm = _original_step(title)

        def __enter__(self):
            return self._cm.__enter__()

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(screenshot, name=f"Step: {self.title}",
                             attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
            return self._cm.__exit__(exc_type, exc_val, exc_tb)

    allure.step = ScreenshotStep
    yield
    allure.step = _original_step

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        path = f"{Config.SCREENSHOT_DIR}/{request.node.name}_{timestamp}.png"
        page.screenshot(path=path, full_page=True)
        allure.attach.file(path, name=f"FAILURE — {request.node.name}",
                          attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate and open Allure report after tests complete."""
    import subprocess
    import shutil

    allure_results = os.path.join(os.path.dirname(__file__), "reports", "allure-results")
    if not os.path.isdir(allure_results):
        return

    allure_bin = shutil.which("allure")
    if not allure_bin:
        print(f"\n⚠️  Install allure: brew install allure")
        return

    try:
        print(f"\n📊 Opening Allure report...")
        subprocess.Popen([allure_bin, "serve", allure_results])
    except (FileNotFoundError, OSError):
        print(f"\n   Run manually: allure serve {allure_results}")
