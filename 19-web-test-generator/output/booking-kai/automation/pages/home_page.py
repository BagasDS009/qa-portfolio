"""Homepage / Search Form Page Object for KAI Booking."""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for KAI search form — uses Flexdatalist + jQuery Datepicker."""

    # Station inputs (Flexdatalist autocomplete)
    XPATH_ORIGIN = '//input[@id="origination-flexdatalist"]'
    XPATH_DESTINATION = '//input[@id="destination-flexdatalist"]'
    XPATH_STATION_OPTION = "//span[text()='{station}']"
    XPATH_FIRST_OPTION = '(//span[contains(@class,"station") or parent::li])[1]'

    # Datepicker
    XPATH_DATE_INPUT = '//input[@name="tanggal"]'
    XPATH_DATE_NEXT_MONTH = '//a[contains(@class,"ui-datepicker-next")]'
    XPATH_DATE_PREV_MONTH = '//a[contains(@class,"ui-datepicker-prev")]'
    XPATH_DATE_DAY = '//a[@class="ui-state-default" and normalize-space()="{day}"]'

    # Passengers
    XPATH_ADULT_PLUS = '//button[@data-type="plus" and @data-field="dewasa"]'
    XPATH_ADULT_MINUS = '//button[@data-type="minus" and @data-field="dewasa"]'
    XPATH_ADULT_COUNT = '//input[@id="dewasa"]'
    XPATH_BABY_PLUS = '//button[@data-type="plus" and @data-field="infant"]'
    XPATH_BABY_MINUS = '//button[@data-type="minus" and @data-field="infant"]'
    XPATH_BABY_COUNT = '//input[@id="infant"]'
    XPATH_BABY_TOOLTIP = '//span[@class="tooltiptext"]'

    # Actions
    XPATH_SEARCH_BTN = '//input[@id="submit"]'
    XPATH_SWAP_BTN = '//*[contains(@class,"swap")]'

    # Actions

    def navigate_to_home(self) -> None:
        """Navigate to homepage and wait for search form."""
        self.navigate()
        self.page.locator(f"xpath={self.XPATH_ORIGIN}").wait_for(state="visible", timeout=30000)

    def select_origin(self, station_code: str) -> None:
        """Select origin station from autocomplete dropdown."""
        self.click_xpath(self.XPATH_ORIGIN)
        self.human_delay(500, 800)
        self.page.locator(f"xpath={self.XPATH_ORIGIN}").clear()
        self.page.locator(f"xpath={self.XPATH_ORIGIN}").fill(station_code)
        self.human_delay(1500, 2500)

        xpath = self.XPATH_STATION_OPTION.replace("{station}", station_code)
        try:
            self.page.locator(f"xpath={xpath}").wait_for(state="visible", timeout=5000)
            self.page.locator(f"xpath={xpath}").click()
        except Exception:
            first = self.page.locator(f"xpath={self.XPATH_FIRST_OPTION}")
            if first.is_visible():
                first.click()
        self.human_delay(500, 800)

    def select_destination(self, station_code: str) -> None:
        """Select destination station from autocomplete dropdown."""
        self.click_xpath(self.XPATH_DESTINATION)
        self.human_delay(500, 800)
        self.page.locator(f"xpath={self.XPATH_DESTINATION}").clear()
        self.page.locator(f"xpath={self.XPATH_DESTINATION}").fill(station_code)
        self.human_delay(1500, 2500)

        xpath = self.XPATH_STATION_OPTION.replace("{station}", station_code)
        try:
            self.page.locator(f"xpath={xpath}").wait_for(state="visible", timeout=5000)
            self.page.locator(f"xpath={xpath}").click()
        except Exception:
            first = self.page.locator(f"xpath={self.XPATH_FIRST_OPTION}")
            if first.is_visible():
                first.click()
        self.human_delay(500, 800)

    def set_departure_date(self, day: str, months_ahead: int = 1) -> None:
        """Set departure date via jQuery datepicker."""
        self.click_xpath(self.XPATH_DATE_INPUT)
        self.human_delay(800, 1200)
        for _ in range(months_ahead):
            self.click_xpath(self.XPATH_DATE_NEXT_MONTH)
            self.human_delay(500, 800)
        day_xpath = self.XPATH_DATE_DAY.replace("{day}", day)
        self.page.locator(f"xpath={day_xpath}").click()
        self.human_delay(500, 800)

    def set_adult_count(self, count: int) -> None:
        """Set adult passenger count (default 1)."""
        current = int(self.get_input_value_xpath(self.XPATH_ADULT_COUNT) or "1")
        if count > current:
            for _ in range(count - current):
                self.click_xpath(self.XPATH_ADULT_PLUS)
                self.page.wait_for_timeout(300)
        elif count < current:
            for _ in range(current - count):
                self.click_xpath(self.XPATH_ADULT_MINUS)
                self.page.wait_for_timeout(300)

    def set_baby_count(self, count: int) -> None:
        """Set baby passenger count (default 0)."""
        current = int(self.get_input_value_xpath(self.XPATH_BABY_COUNT) or "0")
        if count > current:
            for _ in range(count - current):
                self.click_xpath(self.XPATH_BABY_PLUS)
                self.page.wait_for_timeout(300)

    def click_search(self) -> None:
        """Click search button."""
        self.page.locator(f"xpath={self.XPATH_SEARCH_BTN}").click(force=True)
        self.human_delay(2000, 4000)

    def search_train(self, origin: str, destination: str, day: str,
                     adults: int = 1, babies: int = 0, months_ahead: int = 1) -> None:
        """Complete search flow."""
        self.select_origin(origin)
        self.select_destination(destination)
        self.set_departure_date(day, months_ahead=months_ahead)
        self.set_adult_count(adults)
        if babies > 0:
            self.set_baby_count(babies)
        self.click_search()

    def swap_stations(self) -> None:
        """Click swap button."""
        self.click_xpath(self.XPATH_SWAP_BTN)
        self.page.wait_for_timeout(500)

    # Verifications

    def is_search_form_visible(self) -> bool:
        return self.is_visible_xpath(self.XPATH_ORIGIN) and self.is_visible_xpath(self.XPATH_DESTINATION)

    def get_adult_count(self) -> int:
        return int(self.get_input_value_xpath(self.XPATH_ADULT_COUNT) or "1")

    def get_baby_count(self) -> int:
        return int(self.get_input_value_xpath(self.XPATH_BABY_COUNT) or "0")

    def is_baby_tooltip_visible(self) -> bool:
        return self.is_visible_xpath(self.XPATH_BABY_TOOLTIP)

    def get_baby_tooltip_text(self) -> str:
        return self.get_text_xpath(self.XPATH_BABY_TOOLTIP)

    def get_origin_value(self) -> str:
        return self.get_input_value_xpath(self.XPATH_ORIGIN)

    def get_destination_value(self) -> str:
        return self.get_input_value_xpath(self.XPATH_DESTINATION)
