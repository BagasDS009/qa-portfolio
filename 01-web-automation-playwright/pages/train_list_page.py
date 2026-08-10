"""Train List/Search Results Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class TrainListPage(BasePage):
    """Page Object for search results - available train list using XPath."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_TRAIN_LIST = "//*[@class='data-wrapper']/div"
    XPATH_TRAIN_CARD = "//*[@class='data-wrapper']/div/form/a[@class='card-schedule']"
    XPATH_TRAIN_NAME = "//*[@class='name']"
    XPATH_DEPARTURE_TIME = "//*[contains(@class,'departure') or contains(@class,'depart-time')]"
    XPATH_ARRIVAL_TIME = "//*[contains(@class,'arrival') or contains(@class,'arrive-time')]"
    XPATH_TRAIN_PRICE = "//*[contains(@class,'price') or contains(@class,'fare') or contains(@class,'harga')]"
    XPATH_SELECT_BUTTON = "//button[contains(text(),'Pilih') or contains(text(),'Select') or contains(@class,'btn-select')]"
    XPATH_NO_RESULT = "//p[@style='text-align:center;']"
    XPATH_LOADING = "//*[contains(@class,'loading') or contains(@class,'spinner')]"

    def is_train_list_displayed(self) -> bool:
        """Check if train list results are displayed."""
        try:
            self.page.locator(f"xpath={self.XPATH_TRAIN_CARD}").first.wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False

    def get_available_trains_count(self) -> int:
        """Get number of available trains in results."""
        return self.count_xpath(self.XPATH_TRAIN_CARD)

    def select_first_train(self):
        """Select the first available train from the list."""
        self.page.locator(f"xpath={self.XPATH_SELECT_BUTTON}").first.click()
        self.page.wait_for_load_state("networkidle")

    def select_train_by_index(self, index: int):
        """Select train by index (0-based)."""
        self.page.locator(f"xpath={self.XPATH_SELECT_BUTTON}").nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def get_train_name(self, index: int = 0) -> str:
        """Get train name by index."""
        return (
            self.page.locator(f"xpath={self.XPATH_TRAIN_NAME}").nth(index).text_content()
            or ""
        )

    def get_train_price(self, index: int = 0) -> str:
        """Get train price by index."""
        return (
            self.page.locator(f"xpath={self.XPATH_TRAIN_PRICE}").nth(index).text_content()
            or ""
        )

    def get_departure_time(self, index: int = 0) -> str:
        """Get departure time by index."""
        return (
            self.page.locator(f"xpath={self.XPATH_DEPARTURE_TIME}").nth(index).text_content()
            or ""
        )

    def get_arrival_time(self, index: int = 0) -> str:
        """Get arrival time by index."""
        return (
            self.page.locator(f"xpath={self.XPATH_ARRIVAL_TIME}").nth(index).text_content()
            or ""
        )

    def is_no_result(self) -> bool:
        """Check if no result message is shown."""
        return self.is_visible_xpath(self.XPATH_NO_RESULT)

    def get_no_result_message(self) -> str:
        """Get the no result message text."""
        return self.page.locator(f"xpath={self.XPATH_NO_RESULT}").inner_text()

    def wait_for_results(self):
        """Wait for search results to load (spinner disappears)."""
        try:
            self.page.locator(f"xpath={self.XPATH_LOADING}").wait_for(
                state="hidden", timeout=15000
            )
        except Exception:
            pass
        self.page.wait_for_timeout(2000)

    def find_train_by_name(self, train_name: str) -> bool:
        """Check if a specific train is in the results."""
        xpath = f"//*[@class='name' and contains(normalize-space(text()), '{train_name}')]"
        return self.is_visible_xpath(xpath)
