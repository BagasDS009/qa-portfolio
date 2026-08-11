"""Train List/Search Results Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class TrainListPage(BasePage):
    """Page Object for search results - available train list using XPath."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_TRAIN_LIST = "//*[@class='data-wrapper']/div"
    XPATH_TRAIN_CARD = "//*[@class='data-wrapper']/div/form/a[@class='card-schedule']"
    XPATH_SELECT_TRAIN = (
        "//div[@class='name' "
        "and contains(normalize-space(text()), '{train_name}')]"
        "/ancestor::form[1]"
    )
    XPATH_TRAIN_NAME = ".//div[@class='name']"
    XPATH_TRAIN_NUMBER = ".//input[@name='nokereta']"
    XPATH_DEPARTURE_TIME = ".//input[@name='timestart']"
    XPATH_ARRIVAL_TIME = ".//input[@name='timeend']"
    XPATH_TRAIN_PRICE = ".//input[@name='harga']"
    XPATH_ORIGIN = ".//input[@name='asal']"
    XPATH_DESTINATION = ".//input[@name='tujuan']"
    XPATH_ORIGIN_CODE = ".//input[@name='kodeasal']"
    XPATH_DESTINATION_CODE = ".//input[@name='kodetujuan']"
    XPATH_TRAIN_CLASS = ".//input[@name='kelas']"
    XPATH_TRAIN_COACH_CLASS = ".//input[@name='kelas_gerbong']"
    XPATH_SUB_CLASS = ".//input[@name='subkelas']"
    XPATH_SEAT_STATUS = ".//*[contains(@class,'sisa-kursi')]"
    XPATH_SELECT_BUTTON = ".//a[contains(@onclick,'submit')]"
    XPATH_NO_RESULT = "//p[@style='text-align:center;']"
    XPATH_LOADING = "//*[contains(@class,'loading') or contains(@class,'spinner')]"

    # ============================================================
    # Methods
    # ============================================================

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

    def select_train_by_name(self, train_name: str):
        """
        Select train by name (e.g., "Cikuray").
        Finds the form containing that train name and submits it directly.
        """
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        train_form = self.page.locator(f"xpath={xpath}").first

        # Try clicking <a> with onclick submit first
        select_btn = train_form.locator(f"xpath={self.XPATH_SELECT_BUTTON}")
        if select_btn.count() > 0:
            select_btn.click()
        else:
            # Fallback: submit the form via JavaScript
            train_form.evaluate("form => form.submit()")
        self.human_delay(2000, 3000)

    def select_first_train(self):
        """Select the first available train from the list."""
        first_form = self.page.locator(f"xpath={self.XPATH_TRAIN_LIST}//form").first
        first_form.locator(f"xpath={self.XPATH_SELECT_BUTTON}").click()
        self.human_delay(2000, 3000)

    def select_train_by_index(self, index: int):
        """Select train by index (0-based)."""
        forms = self.page.locator(f"xpath={self.XPATH_TRAIN_LIST}//form")
        forms.nth(index).locator(f"xpath={self.XPATH_SELECT_BUTTON}").click()
        self.human_delay(2000, 3000)

    def get_train_name(self, index: int = 0) -> str:
        """Get train name by index."""
        forms = self.page.locator(f"xpath={self.XPATH_TRAIN_LIST}//form")
        return forms.nth(index).locator(f"xpath={self.XPATH_TRAIN_NAME}").text_content() or ""

    def get_train_price(self, train_name: str) -> str:
        """Get train price by train name (from hidden input)."""
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        train_form = self.page.locator(f"xpath={xpath}").first
        return train_form.locator(f"xpath={self.XPATH_TRAIN_PRICE}").get_attribute("value") or ""

    def get_departure_time(self, train_name: str) -> str:
        """Get departure time by train name (from hidden input)."""
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        train_form = self.page.locator(f"xpath={xpath}").first
        return train_form.locator(f"xpath={self.XPATH_DEPARTURE_TIME}").get_attribute("value") or ""

    def get_arrival_time(self, train_name: str) -> str:
        """Get arrival time by train name (from hidden input)."""
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        train_form = self.page.locator(f"xpath={xpath}").first
        return train_form.locator(f"xpath={self.XPATH_ARRIVAL_TIME}").get_attribute("value") or ""

    def get_seat_status(self, train_name: str) -> str:
        """Get seat availability status for a train."""
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        train_form = self.page.locator(f"xpath={xpath}").first
        return train_form.locator(f"xpath={self.XPATH_SEAT_STATUS}").text_content() or ""

    def is_no_result(self) -> bool:
        """Check if no result message is shown."""
        return self.is_visible_xpath(self.XPATH_NO_RESULT)

    def get_no_result_message(self) -> str:
        """Get the no result message text."""
        return self.page.locator(f"xpath={self.XPATH_NO_RESULT}").inner_text()

    def wait_for_results(self):
        """Wait for search results to load."""
        try:
            self.page.locator(f"xpath={self.XPATH_LOADING}").wait_for(
                state="hidden", timeout=15000
            )
        except Exception:
            pass
        self.page.wait_for_timeout(2000)

    def find_train_by_name(self, train_name: str) -> bool:
        """Check if a specific train is in the results."""
        xpath = self.XPATH_SELECT_TRAIN.replace("{train_name}", train_name)
        return self.page.locator(f"xpath={xpath}").count() > 0
