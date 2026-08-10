import pytest
from playwright.sync_api import Playwright

BASE_URL = "https://fakerestapi.azurewebsites.net"


@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()


import os
import subprocess
import shutil


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate Allure report and print link in terminal."""
    allure_results = "reports/allure-results"
    allure_report = "reports/allure-report"

    if shutil.which("allure") is None:
        print(f"\n⚠️  Allure CLI not installed. Run: brew install allure")
        print(f"   Manual: allure serve {allure_results}")
        return

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
        print(f"\n⚠️  Allure generate failed. Run: allure serve {allure_results}")
