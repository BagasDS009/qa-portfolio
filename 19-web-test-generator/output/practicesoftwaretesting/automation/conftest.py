"""Pytest configuration, shared fixtures, and hooks."""

import os
import sys
from datetime import datetime

import pytest
from playwright.sync_api import Page

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import Config


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Set Allure environment properties."""
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)
        with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
            f.write(f"Base.URL={Config.BASE_URL}\n")
            f.write(f"Browser={Config.BROWSER}\n")
            f.write(f"Headless={Config.HEADLESS}\n")
            f.write(f"Environment={os.getenv('ENV', 'sit')}\n")


# ============================================================================
# Browser Configuration (overrides pytest-playwright defaults)
# ============================================================================

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Browser launch arguments."""
    return {
        "headless": Config.HEADLESS or os.getenv("CI", "false").lower() == "true",
        "slow_mo": Config.SLOWMO,
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context arguments."""
    return {
        "viewport": {"width": 1366, "height": 768},
        "locale": "en-US",
        "timezone_id": "Europe/Amsterdam",
        "ignore_https_errors": True,
    }


# ============================================================================
# Authentication Fixtures
# ============================================================================

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Page already logged in as customer."""
    from pages.login_page import LoginPage
    from test_data.users import VALID_CUSTOMER

    login_page = LoginPage(page)
    login_page.login(VALID_CUSTOMER["email"], VALID_CUSTOMER["password"])
    page.wait_for_load_state("networkidle")
    return page


# ============================================================================
# Reporting — Screenshot at Every Step + on Failure
# ============================================================================

@pytest.fixture(autouse=True)
def auto_screenshot_steps(request, page: Page):
    """Capture screenshot after every allure step and on failure.
    
    Uses Playwright's page events to detect navigation/action completion,
    then attaches screenshot to current Allure step.
    """
    import allure
    
    # Patch allure.step to auto-screenshot after each step completes
    _original_step = allure.step

    class ScreenshotStep:
        """Context manager that takes screenshot after step body executes."""

        def __init__(self, title):
            self.title = title
            self._cm = _original_step(title)

        def __enter__(self):
            return self._cm.__enter__()

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Take screenshot at end of step (before exiting context)
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"Step: {self.title}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass  # Page may be closed or navigating
            return self._cm.__exit__(exc_type, exc_val, exc_tb)

    # Replace allure.step with our screenshot version
    allure.step = ScreenshotStep

    yield

    # Restore original
    allure.step = _original_step

    # Screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        path = f"{Config.SCREENSHOT_DIR}/{request.node.name}_{timestamp}.png"
        page.screenshot(path=path, full_page=True)
        allure.attach.file(
            path,
            name=f"FAILURE — {request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate Allure report as single HTML file and open in browser."""
    import subprocess
    import shutil

    allure_results = os.path.join(os.path.dirname(__file__), "reports", "allure-results")
    allure_report_dir = os.path.join(os.path.dirname(__file__), "reports", "allure-report")
    single_file = os.path.join(os.path.dirname(__file__), "reports", "allure-report.html")

    if not os.path.isdir(allure_results):
        return

    allure_bin = shutil.which("allure")
    if not allure_bin:
        print("\n⚠️  Allure CLI not installed. Install with: brew install allure")
        return

    try:
        # Step 1: Generate static report folder
        subprocess.run(
            [allure_bin, "generate", allure_results, "-o", allure_report_dir, "--clean"],
            capture_output=True, timeout=30,
        )

        # Step 2: Combine into single HTML file (opens without server)
        combine_bin = shutil.which("allure-combine")
        if not combine_bin:
            # Try via python module
            result = subprocess.run(
                [sys.executable, "-m", "allure_combine.combine", allure_report_dir,
                 "--dest", os.path.dirname(single_file),
                 "--file-name", "allure-report.html"],
                capture_output=True, timeout=30,
            )
            if result.returncode != 0:
                # Fallback: just open via allure serve
                subprocess.Popen([allure_bin, "serve", allure_results])
                return
        else:
            subprocess.run(
                [combine_bin, allure_report_dir,
                 "--dest", os.path.dirname(single_file),
                 "--file-name", "allure-report.html"],
                capture_output=True, timeout=30,
            )

        # Step 3: Open the single HTML file directly in browser
        if os.path.exists(single_file):
            subprocess.Popen(["open", single_file])
            print(f"\n📊 Report: {single_file}")
        else:
            # Fallback to serve
            subprocess.Popen([allure_bin, "serve", allure_results])

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        print(f"\n📁 Results saved to: {allure_results}")
        print(f"   Run manually: allure serve {allure_results}")
