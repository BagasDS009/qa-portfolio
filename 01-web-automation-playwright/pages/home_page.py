"""Home/Search Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for KAI Home/Search page using XPath selectors."""

    # ============================================================
    # XPath Locators - Search Form
    # ============================================================
    XPATH_ORIGIN_INPUT = '//input[@placeholder="Stasiun Asal..." and @id="origination-flexdatalist"]'
    XPATH_DESTINATION_INPUT = '//input[@placeholder="Stasiun Tujuan..." and @id="destination-flexdatalist"]'
    XPATH_DEPARTURE_DATE = '//input[@data-error="Mohon diisi tanggal" and @name="tanggal"]'

    # Adult passenger (plus/minus buttons + input)
    XPATH_ADULT_MINUS = '//button[@data-type="minus" and @data-field="dewasa"]'
    XPATH_ADULT_PLUS = '//button[@data-type="plus" and @data-field="dewasa"]'
    XPATH_ADULT_COUNT = '//input[@id="dewasa"]'

    # Baby passenger (plus/minus buttons + input)
    XPATH_BABY_MINUS = '//button[@data-type="minus" and @data-field="infant"]'
    XPATH_BABY_PLUS = '//button[@data-type="plus" and @data-field="infant"]'
    XPATH_BABY_COUNT = '//input[@id="infant"]'

    # Search & Swap
    XPATH_SEARCH_BUTTON = '//input[@id="submit"]'
    XPATH_SWAP_BUTTON = '//button[contains(@class,"swap") or @aria-label="Swap"]|//*[contains(@class,"swap")]'

    # XPath Locators - Autocomplete Dropdown
    XPATH_STATION_DROPDOWN = '//ul[contains(@class,"autocomplete") or contains(@class,"dropdown")]'
    XPATH_STATION_OPTION = '//span[contains(@class,"station") or parent::li]'
    XPATH_STATION_FIRST_OPTION = '(//span[contains(@class,"station") or parent::li])[1]'

    # XPath Locators - Navigation/Profile
    XPATH_PROFILE_MENU = '//*[contains(@class,"profile") or contains(@class,"user-dropdown") or contains(@class,"account")]'
    XPATH_LOGOUT_BUTTON = '//a[contains(text(),"Logout") or contains(text(),"Keluar")]|//button[contains(text(),"Logout")]'

    # ============================================================
    # Page Actions
    # ============================================================

    def navigate_to_home(self):
        """Navigate to home/booking page."""
        self.navigate()
        self.wait_for_load()

    def select_origin_station(self, station: str):
        """
        Select origin station from autocomplete dropdown.
        Steps: Click input → Type code → Wait dropdown → Click //span[text()='PSE']
        """
        self.click_xpath(self.XPATH_ORIGIN_INPUT)
        self.page.wait_for_timeout(500)

        self.page.locator(f"xpath={self.XPATH_ORIGIN_INPUT}").clear()
        self.fill_xpath(self.XPATH_ORIGIN_INPUT, station)
        self.page.wait_for_timeout(1500)

        # Wait and click matching station from dropdown
        station_xpath = f"//span[text()='{station}']"
        self.page.locator(f"xpath={station_xpath}").wait_for(state="visible", timeout=5000)
        self.click_xpath(station_xpath)
        self.page.wait_for_timeout(500)

    def select_destination_station(self, station: str):
        """
        Select destination station from autocomplete dropdown.
        Steps: Click input → Type code → Wait dropdown → Click //span[text()='BD']
        """
        self.click_xpath(self.XPATH_DESTINATION_INPUT)
        self.page.wait_for_timeout(500)

        self.page.locator(f"xpath={self.XPATH_DESTINATION_INPUT}").clear()
        self.fill_xpath(self.XPATH_DESTINATION_INPUT, station)
        self.page.wait_for_timeout(1500)

        # Wait and click matching station from dropdown
        station_xpath = f"//span[text()='{station}']"
        self.page.locator(f"xpath={station_xpath}").wait_for(state="visible", timeout=5000)
        self.click_xpath(station_xpath)
        self.page.wait_for_timeout(500)

    def set_departure_date(self, date: str):
        """Set departure date."""
        self.fill_xpath(self.XPATH_DEPARTURE_DATE, date)

    def set_adult_count(self, count: int):
        """
        Set adult passenger count using plus/minus buttons.
        Default value is 1, so clicks (count - 1) times on plus.
        """
        # Get current value
        current = int(
            self.page.locator(f"xpath={self.XPATH_ADULT_COUNT}").input_value() or "1"
        )

        if count > current:
            for _ in range(count - current):
                self.click_xpath(self.XPATH_ADULT_PLUS)
                self.page.wait_for_timeout(300)
        elif count < current:
            for _ in range(current - count):
                self.click_xpath(self.XPATH_ADULT_MINUS)
                self.page.wait_for_timeout(300)

    def set_baby_count(self, count: int):
        """
        Set baby passenger count using plus/minus buttons.
        Default value is 0, so clicks count times on plus.
        """
        current = int(
            self.page.locator(f"xpath={self.XPATH_BABY_COUNT}").input_value() or "0"
        )

        if count > current:
            for _ in range(count - current):
                self.click_xpath(self.XPATH_BABY_PLUS)
                self.page.wait_for_timeout(300)
        elif count < current:
            for _ in range(current - count):
                self.click_xpath(self.XPATH_BABY_MINUS)
                self.page.wait_for_timeout(300)

    def click_search(self):
        """Click search/submit button."""
        self.click_xpath(self.XPATH_SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def search_train(self, origin: str, destination: str, date: str, adults: int = 1, babies: int = 0):
        """
        Complete search flow:
        1. Select origin station (dropdown)
        2. Select destination station (dropdown)
        3. Set departure date
        4. Set adult count (plus/minus)
        5. Set baby count (plus/minus)
        6. Click search
        """
        self.select_origin_station(origin)
        self.select_destination_station(destination)
        self.set_departure_date(date)
        self.set_adult_count(adults)
        if babies > 0:
            self.set_baby_count(babies)
        self.click_search()

    def swap_stations(self):
        """Swap origin and destination stations."""
        self.click_xpath(self.XPATH_SWAP_BUTTON)
        self.page.wait_for_timeout(500)

    def is_search_form_displayed(self) -> bool:
        """Verify search form is visible on page."""
        return (
            self.is_visible_xpath(self.XPATH_ORIGIN_INPUT)
            and self.is_visible_xpath(self.XPATH_DESTINATION_INPUT)
        )

    def get_origin_value(self) -> str:
        """Get current origin station input value."""
        return self.page.locator(f"xpath={self.XPATH_ORIGIN_INPUT}").input_value()

    def get_destination_value(self) -> str:
        """Get current destination station input value."""
        return self.page.locator(f"xpath={self.XPATH_DESTINATION_INPUT}").input_value()

    def get_adult_count(self) -> int:
        """Get current adult count value."""
        return int(
            self.page.locator(f"xpath={self.XPATH_ADULT_COUNT}").input_value() or "1"
        )

    def get_baby_count(self) -> int:
        """Get current baby count value."""
        return int(
            self.page.locator(f"xpath={self.XPATH_BABY_COUNT}").input_value() or "0"
        )

    def logout(self):
        """Perform logout from profile menu."""
        self.click_xpath(self.XPATH_PROFILE_MENU)
        self.page.wait_for_timeout(500)
        self.click_xpath(self.XPATH_LOGOUT_BUTTON)
        self.page.wait_for_load_state("networkidle")
