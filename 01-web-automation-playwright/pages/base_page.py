"""Base Page class with common methods and human-like behavior."""

import random
from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects. Anti-detection with human delays."""

    BASE_URL = "https://booking.kai.id"

    def __init__(self, page: Page):
        self.page = page

    # ============================
    # Navigation
    # ============================

    def navigate(self, path: str = ""):
        """Navigate to a specific path with human delay."""
        url = f"{self.BASE_URL}/{path}" if path else self.BASE_URL
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.human_delay(3000, 5000)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def wait_for_load(self):
        """Wait for page to be usable (not networkidle which can timeout on Cloudflare)."""
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=30000)
        except Exception:
            pass
        self.human_delay(2000, 4000)

    # ============================
    # Human-like Behavior
    # ============================

    def human_delay(self, min_ms: int = 500, max_ms: int = 1500):
        """Random delay to mimic human behavior."""
        self.page.wait_for_timeout(random.randint(min_ms, max_ms))

    def human_type(self, locator, text: str):
        """Type text character by character with random delays (like a human)."""
        locator.click()
        self.human_delay(300, 600)
        for char in text:
            locator.press(char)
            self.page.wait_for_timeout(random.randint(50, 150))
        self.human_delay(300, 500)

    def take_screenshot(self, name: str):
        """Take screenshot for reporting."""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")

    # ============================
    # XPath-based element actions (with delays)
    # ============================

    def click_xpath(self, xpath: str):
        """Click element by XPath with human delay."""
        self.page.locator(f"xpath={xpath}").click()
        self.human_delay(500, 1000)

    def fill_xpath(self, xpath: str, value: str):
        """Fill input by XPath with human-like behavior."""
        locator = self.page.locator(f"xpath={xpath}")
        locator.click()
        self.human_delay(300, 600)
        locator.fill(value)
        self.human_delay(500, 1000)

    def type_xpath(self, xpath: str, value: str):
        """Type into input character by character (more human-like than fill)."""
        locator = self.page.locator(f"xpath={xpath}")
        self.human_type(locator, value)

    def get_text_xpath(self, xpath: str) -> str:
        """Get text content by XPath."""
        return self.page.locator(f"xpath={xpath}").text_content() or ""

    def is_visible_xpath(self, xpath: str) -> bool:
        """Check if element is visible by XPath."""
        return self.page.locator(f"xpath={xpath}").is_visible()

    def wait_for_xpath(self, xpath: str, timeout: int = 15000):
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
        self.human_delay(500, 1000)

    def fill(self, selector: str, value: str):
        """Fill input field by CSS selector."""
        self.page.locator(selector).fill(value)
        self.human_delay(300, 600)

    def get_text(self, selector: str) -> str:
        """Get text content of element."""
        return self.page.locator(selector).text_content() or ""

    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible on page."""
        return self.page.locator(selector).is_visible()

    def get_element_count(self, selector: str) -> int:
        """Get count of matching elements."""
        return self.page.locator(selector).count()
