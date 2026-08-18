"""Base Page Object with common actions for all pages."""

from playwright.sync_api import Locator, Page, expect

from config.settings import Config


class BasePage:
    """Base class for all Page Objects. Uses Playwright auto-wait — no hard sleeps."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = Config.BASE_URL

    # ============================
    # Navigation
    # ============================

    def navigate(self, path: str = "") -> None:
        """Navigate to a specific path relative to base URL."""
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def wait_for_load(self) -> None:
        """Wait for page to be fully loaded (network idle)."""
        self.page.wait_for_load_state("networkidle")

    # ============================
    # data-test Helpers (preferred)
    # ============================

    def get_by_test(self, test_id: str) -> Locator:
        """Get element by data-test attribute."""
        return self.page.locator(f"[data-test='{test_id}']")

    def click_test(self, test_id: str) -> None:
        """Click element by data-test."""
        self.get_by_test(test_id).click()

    def fill_test(self, test_id: str, value: str) -> None:
        """Fill input by data-test."""
        self.get_by_test(test_id).fill(value)

    def get_text_test(self, test_id: str) -> str:
        """Get text by data-test."""
        return self.get_by_test(test_id).text_content() or ""

    def is_visible_test(self, test_id: str) -> bool:
        """Check visibility by data-test."""
        return self.get_by_test(test_id).is_visible()

    # ============================
    # General Element Actions
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

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(selector).is_visible()

    def get_count(self, selector: str) -> int:
        """Count matching elements."""
        return self.page.locator(selector).count()

    def select_option(self, selector: str, *, label: str = "", value: str = "") -> None:
        """Select option from dropdown."""
        if label:
            self.page.locator(selector).select_option(label=label)
        elif value:
            self.page.locator(selector).select_option(value=value)

    # ============================
    # Assertions
    # ============================

    def expect_visible(self, selector: str, timeout: int = 5000) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

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
        path = f"{Config.SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=path)
        return path
