"""Base Page class with common methods for Toolshop automation."""

from playwright.sync_api import Locator, Page, expect

from utils.config import Config


class BasePage:
    """Base class for all page objects. Uses Playwright auto-wait (no artificial delays)."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = Config.BASE_URL

    # ============================
    # Navigation
    # ============================

    def navigate(self, path: str = "") -> None:
        """Navigate to a specific path."""
        url = f"{self.base_url}/{path}" if path else self.base_url
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def wait_for_load(self) -> None:
        """Wait for page to be fully loaded."""
        self.page.wait_for_load_state("networkidle")

    # ============================
    # data-test attribute helpers
    # ============================

    def get_by_test(self, test_id: str) -> Locator:
        """Get element by data-test attribute (preferred selector for Toolshop)."""
        return self.page.locator(f"[data-test='{test_id}']")

    def click_test(self, test_id: str) -> None:
        """Click element by data-test attribute."""
        self.get_by_test(test_id).click()

    def fill_test(self, test_id: str, value: str) -> None:
        """Fill input by data-test attribute."""
        self.get_by_test(test_id).fill(value)

    def get_text_test(self, test_id: str) -> str:
        """Get text content by data-test attribute."""
        return self.get_by_test(test_id).text_content() or ""

    def is_visible_test(self, test_id: str) -> bool:
        """Check if element is visible by data-test attribute."""
        return self.get_by_test(test_id).is_visible()

    # ============================
    # General element actions
    # ============================

    def click(self, selector: str) -> None:
        """Click element by CSS selector."""
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        """Fill input by CSS selector."""
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        """Get text content of element."""
        return self.page.locator(selector).text_content() or ""

    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(selector).is_visible()

    def get_element_count(self, selector: str) -> int:
        """Count matching elements."""
        return self.page.locator(selector).count()

    def select_option(self, selector: str, value: str) -> None:
        """Select option from dropdown by visible text."""
        self.page.locator(selector).select_option(label=value)

    # ============================
    # Assertions
    # ============================

    def expect_visible(self, selector: str) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_url_contains(self, path: str) -> None:
        """Assert current URL contains path."""
        expect(self.page).to_have_url(f"*{path}*")

    # ============================
    # Screenshots
    # ============================

    def take_screenshot(self, name: str) -> str:
        """Take screenshot and return path."""
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path)
        return path
