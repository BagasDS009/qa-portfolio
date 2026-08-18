"""Train List (Search Results) Page Object for KAI Booking."""

from pages.base_page import BasePage


class TrainListPage(BasePage):
    """Page Object for search results — available train list."""

    XPATH_TRAIN_CARD = "//*[@class='data-wrapper']/div/form/a[@class='card-schedule']"
    XPATH_TRAIN_NAME = ".//div[@class='name']"
    XPATH_TRAIN_PRICE = ".//input[@name='harga']"
    XPATH_DEPARTURE_TIME = ".//input[@name='timestart']"
    XPATH_ARRIVAL_TIME = ".//input[@name='timeend']"
    XPATH_TRAIN_CLASS = ".//input[@name='kelas']"
    XPATH_SEAT_STATUS = ".//*[contains(@class,'sisa-kursi')]"
    XPATH_SELECT_BTN = ".//a[contains(@onclick,'submit')]"
    XPATH_NO_RESULT = "//p[@style='text-align:center;']"
    XPATH_LOADING = "//*[contains(@class,'loading') or contains(@class,'spinner')]"
    XPATH_ALL_FORMS = "//*[@class='data-wrapper']//form"

    # Actions

    def wait_for_results(self) -> None:
        """Wait for train list or no-result to appear."""
        try:
            self.page.locator(f"xpath={self.XPATH_LOADING}").wait_for(state="hidden", timeout=15000)
        except Exception:
            pass
        self.page.wait_for_timeout(2000)

    def select_first_train(self) -> None:
        """Select the first available train."""
        form = self.page.locator(f"xpath={self.XPATH_ALL_FORMS}").first
        form.locator(f"xpath={self.XPATH_SELECT_BTN}").click()
        self.human_delay(2000, 3000)

    def select_cheapest_train(self) -> None:
        """Select the cheapest train from results (lowest price).
        
        Reads hidden input[name='harga'] from each form, picks lowest.
        """
        forms = self.page.locator(f"xpath={self.XPATH_ALL_FORMS}")
        count = forms.count()
        
        if count == 0:
            return
        
        cheapest_idx = 0
        cheapest_price = float("inf")
        
        for i in range(count):
            form = forms.nth(i)
            price_el = form.locator(f"xpath={self.XPATH_TRAIN_PRICE}")
            if price_el.count() > 0:
                price_str = price_el.get_attribute("value") or "999999999"
                try:
                    price = int(price_str.replace(".", "").replace(",", ""))
                    if price < cheapest_price:
                        cheapest_price = price
                        cheapest_idx = i
                except ValueError:
                    pass
        
        # Click the select button on the cheapest train
        forms.nth(cheapest_idx).locator(f"xpath={self.XPATH_SELECT_BTN}").click()
        self.human_delay(2000, 3000)

    def select_train_by_index(self, index: int) -> None:
        """Select train by index (0-based)."""
        forms = self.page.locator(f"xpath={self.XPATH_ALL_FORMS}")
        forms.nth(index).locator(f"xpath={self.XPATH_SELECT_BTN}").click()
        self.human_delay(2000, 3000)

    # Verifications

    def is_results_displayed(self) -> bool:
        """Check if train results are shown."""
        try:
            self.page.locator(f"xpath={self.XPATH_TRAIN_CARD}").first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def get_train_count(self) -> int:
        """Count available trains in results."""
        return self.count_xpath(self.XPATH_TRAIN_CARD)

    def get_first_train_name(self) -> str:
        """Get name of first train in list."""
        form = self.page.locator(f"xpath={self.XPATH_ALL_FORMS}").first
        return form.locator(f"xpath={self.XPATH_TRAIN_NAME}").text_content() or ""

    def is_no_result(self) -> bool:
        """Check if truly no trains available (0 cards AND no-result message)."""
        # Must have 0 train cards — "connecting train" text is NOT no-result
        if self.get_train_count() > 0:
            return False
        return self.is_visible_xpath(self.XPATH_NO_RESULT)

    def get_no_result_message(self) -> str:
        """Get the no-result message text."""
        return self.get_text_xpath(self.XPATH_NO_RESULT)
