"""Home/Search Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for KAI Home/Search page using XPath selectors."""

    # ============================================================
    # XPath Locators - Search Form
    # ============================================================
    XPATH_ORIGIN_INPUT = '//input[@placeholder="Stasiun Asal..." and @id="origination-flexdatalist"]'
    XPATH_DESTINATION_INPUT = '//input[@placeholder="Stasiun Tujuan..." and @id="destination-flexdatalist"]'
    # Datepicker
    XPATH_DEPARTURE_DATE = '//input[@data-error="Mohon diisi tanggal" and @name="tanggal"]'
    XPATH_DEPARTURE_DATE_BTN_BACK_MONTH = '//a[@class="ui-datepicker-prev ui-corner-all" and @data-event="click" and @title="Prev"]'
    XPATH_DEPARTURE_DATE_BTN_NEXT_MONTH = '//a[@class="ui-datepicker-next ui-corner-all" and @data-event="click" and @title="Next"]'

    # Adult passenger (plus/minus buttons + input)
    XPATH_ADULT_MINUS = '//button[@data-type="minus" and @data-field="dewasa"]'
    XPATH_ADULT_PLUS = '//button[@data-type="plus" and @data-field="dewasa"]'
    XPATH_ADULT_COUNT = '//input[@id="dewasa"]'

    # Baby passenger (plus/minus buttons + input)
    XPATH_BABY_MINUS = '//button[@data-type="minus" and @data-field="infant"]'
    XPATH_BABY_PLUS = '//button[@data-type="plus" and @data-field="infant"]'
    XPATH_BABY_COUNT = '//input[@id="infant"]'

    # Tooltip validation
    XPATH_BABY_TOOLTIP = '//span[@class="tooltiptext"]'
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

    def get_baby_tooltip_message(self) -> str:
        """Get baby passenger tooltip validation message."""
        return self.page.locator(f"xpath={self.XPATH_BABY_TOOLTIP}").inner_text()

    def is_baby_tooltip_visible(self) -> bool:
        """Check if baby tooltip validation is visible."""
        return self.is_visible_xpath(self.XPATH_BABY_TOOLTIP)

    def navigate_to_home(self):
        """Navigate to home/booking page and wait for search form."""
        self.navigate()
        # Wait for search form element instead of networkidle
        try:
            self.page.locator(f"xpath={self.XPATH_ORIGIN_INPUT}").wait_for(
                state="visible", timeout=30000
            )
        except Exception:
            # Page might still be loading, give extra time
            self.human_delay(3000, 5000)

    def select_origin_station(self, station: str):
        """
        Select origin station from autocomplete dropdown.
        Steps: Click input → Type code → Wait dropdown → Click //span[text()='PSE']
        """
        self.click_xpath(self.XPATH_ORIGIN_INPUT)
        self.human_delay(500, 800)

        self.page.locator(f"xpath={self.XPATH_ORIGIN_INPUT}").clear()
        self.page.locator(f"xpath={self.XPATH_ORIGIN_INPUT}").fill(station)
        self.human_delay(1500, 2500)

        # Try to click matching station from dropdown
        station_xpath = f"//span[text()='{station}']"
        try:
            self.page.locator(f"xpath={station_xpath}").wait_for(state="visible", timeout=5000)
            self.page.locator(f"xpath={station_xpath}").click()
        except Exception:
            # Fallback: click first option in dropdown if exact match not found
            first_option = self.page.locator(f"xpath={self.XPATH_STATION_FIRST_OPTION}")
            if first_option.is_visible():
                first_option.click()
        self.human_delay(500, 1000)

    def select_destination_station(self, station: str):
        """
        Select destination station from autocomplete dropdown.
        Steps: Click input → Type code → Wait dropdown → Click //span[text()='BD']
        """
        self.click_xpath(self.XPATH_DESTINATION_INPUT)
        self.human_delay(500, 800)

        self.page.locator(f"xpath={self.XPATH_DESTINATION_INPUT}").clear()
        self.page.locator(f"xpath={self.XPATH_DESTINATION_INPUT}").fill(station)
        self.human_delay(1500, 2500)

        # Try to click matching station from dropdown
        station_xpath = f"//span[text()='{station}']"
        try:
            self.page.locator(f"xpath={station_xpath}").wait_for(state="visible", timeout=5000)
            self.page.locator(f"xpath={station_xpath}").click()
        except Exception:
            # Fallback: click first option in dropdown if exact match not found
            first_option = self.page.locator(f"xpath={self.XPATH_STATION_FIRST_OPTION}")
            if first_option.is_visible():
                first_option.click()
        self.human_delay(500, 1000)

    def set_departure_date(self, tgl: str):
        """
        Set departure date via datepicker.
        Flow: Click input → Next month → Click date number.
        Args:
            tgl: Day number as string (e.g., "17", "25")
        """
        # Step 1: Click date input to open datepicker
        self.click_xpath(self.XPATH_DEPARTURE_DATE)
        self.human_delay(800, 1200)

        # Step 2: Click next month (to pick future date)
        self.click_xpath(self.XPATH_DEPARTURE_DATE_BTN_NEXT_MONTH)
        self.human_delay(500, 800)

        # Step 3: Click the target date number (build xpath directly)
        date_xpath = f'//a[@class="ui-state-default" and normalize-space()="{tgl}"]'
        self.page.locator(f"xpath={date_xpath}").click()
        self.human_delay(500, 1000)

    def navigate_datepicker_next_month(self, times: int = 1):
        """Click next month button in datepicker (for future dates)."""
        for _ in range(times):
            self.click_xpath(self.XPATH_DEPARTURE_DATE_BTN_NEXT_MONTH)
            self.human_delay(500, 800)

    def navigate_datepicker_prev_month(self, times: int = 1):
        """Click previous month button in datepicker."""
        for _ in range(times):
            self.click_xpath(self.XPATH_DEPARTURE_DATE_BTN_BACK_MONTH)
            self.human_delay(500, 800)

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
        """Click search/submit button (force click to bypass any overlay)."""
        self.page.locator(f"xpath={self.XPATH_SEARCH_BUTTON}").click(force=True)
        self.human_delay(2000, 4000)

    def search_train(self, origin: str, destination: str, tgl: str, adults: int = 1, babies: int = 0):
        """
        Complete search flow:
        1. Select origin station (dropdown)
        2. Select destination station (dropdown)
        3. Set departure date (datepicker - day number)
        4. Set adult count (plus/minus)
        5. Set baby count (plus/minus)
        6. Click search
        
        Args:
            origin: Station code (e.g., "PSE")
            destination: Station code (e.g., "BD")
            tgl: Day number string (e.g., "17", "25")
            adults: Number of adult passengers
            babies: Number of baby passengers
        """
        self.select_origin_station(origin)
        self.select_destination_station(destination)
        self.set_departure_date(tgl)
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
