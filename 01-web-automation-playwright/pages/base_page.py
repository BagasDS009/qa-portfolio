"""Base Page class with common methods shared across all pages."""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects. Uses XPath locators strategy."""

    BASE_URL = "https://booking.kai.id"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        """Navigate to a specific path."""
        url = f"{self.BASE_URL}/{path}" if path else self.BASE_URL
        self.page.goto(url)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def wait_for_load(self):
        """Wait for page to fully load."""
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str):
        """Take screenshot for reporting."""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")

    # ============================
    # XPath-based element actions
    # ============================

    def click_xpath(self, xpath: str):
        """Click element by XPath."""
        self.page.locator(f"xpath={xpath}").click()

    def fill_xpath(self, xpath: str, value: str):
        """Fill input by XPath."""
        self.page.locator(f"xpath={xpath}").fill(value)

    def get_text_xpath(self, xpath: str) -> str:
        """Get text content by XPath."""
        return self.page.locator(f"xpath={xpath}").text_content() or ""

    def is_visible_xpath(self, xpath: str) -> bool:
        """Check if element is visible by XPath."""
        return self.page.locator(f"xpath={xpath}").is_visible()

    def wait_for_xpath(self, xpath: str, timeout: int = 10000):
        """Wait for element to be visible by XPath."""
        self.page.locator(f"xpath={xpath}").wait_for(state="visible", timeout=timeout)

    def count_xpath(self, xpath: str) -> int:
        """Count elements matching XPath."""
        return self.page.locator(f"xpath={xpath}").count()

    # ============================
    # CSS selector-based actions (fallback)
    # ============================

    def click(self, selector: str):
        """Click on element by CSS selector."""
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        """Fill input field by CSS selector."""
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        """Get text content of element."""
        return self.page.locator(selector).text_content() or ""

    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible on page."""
        return self.page.locator(selector).is_visible()

    def get_element_count(self, selector: str) -> int:
        """Get count of matching elements."""
        return self.page.locator(selector).count()
