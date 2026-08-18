"""Base Page Object for KAI Booking — XPath-heavy site (jQuery, no data-test)."""

import random
import time
from playwright.sync_api import Page
from config.settings import Config


class BasePage:
    """Base class for all KAI Page Objects.
    
    This site is server-rendered with jQuery (NOT SPA).
    Full page reloads between steps — use wait_for_load_state("load").
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = Config.BASE_URL

    # Navigation
    def navigate(self, path: str = "") -> None:
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url, wait_until="load", timeout=60000)

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("load")

    # Human-like delay (for autocomplete/datepicker interactions)
    def human_delay(self, min_ms: int = 500, max_ms: int = 1500) -> None:
        delay = random.randint(min_ms, max_ms)
        self.page.wait_for_timeout(delay)

    # XPath helpers (primary selector strategy for this site)
    def click_xpath(self, xpath: str) -> None:
        self.page.locator(f"xpath={xpath}").click()

    def fill_xpath(self, xpath: str, value: str) -> None:
        self.page.locator(f"xpath={xpath}").fill(value)

    def get_text_xpath(self, xpath: str) -> str:
        return self.page.locator(f"xpath={xpath}").text_content() or ""

    def is_visible_xpath(self, xpath: str) -> bool:
        return self.page.locator(f"xpath={xpath}").is_visible()

    def count_xpath(self, xpath: str) -> int:
        return self.page.locator(f"xpath={xpath}").count()

    def get_input_value_xpath(self, xpath: str) -> str:
        return self.page.locator(f"xpath={xpath}").input_value()

    # CSS helpers (fallback)
    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    # Screenshot
    def take_screenshot(self, name: str) -> str:
        path = f"{Config.SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        return path
