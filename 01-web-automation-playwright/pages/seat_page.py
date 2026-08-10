"""Seat Selection Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class SeatPage(BasePage):
    """Page Object for seat selection page using XPath."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_SEAT_MAP = "//div[contains(@class,'seat-map') or contains(@class,'seat-layout') or contains(@class,'seat-container')]"
    XPATH_AVAILABLE_SEAT = "//div[contains(@class,'seat') and not(contains(@class,'occupied')) and not(contains(@class,'selected')) and not(contains(@class,'disabled'))]"
    XPATH_SELECTED_SEAT = "//div[contains(@class,'seat') and (contains(@class,'selected') or contains(@class,'active') or contains(@class,'chosen'))]"
    XPATH_OCCUPIED_SEAT = "//div[contains(@class,'seat') and (contains(@class,'occupied') or contains(@class,'disabled') or contains(@class,'taken'))]"
    XPATH_CONFIRM_BUTTON = "//button[contains(text(),'Konfirmasi') or contains(text(),'Confirm') or contains(text(),'Lanjutkan')]"
    XPATH_SKIP_BUTTON = "//button[contains(text(),'Lewati') or contains(text(),'Skip')]|//a[contains(text(),'Pilih Nanti')]"
    XPATH_COACH_SELECTOR = "//select[contains(@name,'coach') or contains(@name,'gerbong')]|//div[contains(@class,'coach-selector')]"
    XPATH_SEAT_INFO = "//*[contains(@class,'seat-info') or contains(@class,'seat-summary') or contains(@class,'selected-seat')]"

    def is_seat_map_displayed(self) -> bool:
        """Check if seat map/layout is visible."""
        return self.is_visible_xpath(self.XPATH_SEAT_MAP)

    def get_available_seats_count(self) -> int:
        """Get number of available (unoccupied) seats."""
        return self.count_xpath(self.XPATH_AVAILABLE_SEAT)

    def select_first_available_seat(self):
        """Select the first available seat on the map."""
        self.page.locator(f"xpath={self.XPATH_AVAILABLE_SEAT}").first.click()
        self.page.wait_for_timeout(500)

    def select_seat_by_index(self, index: int):
        """Select seat by index from available seats."""
        self.page.locator(f"xpath={self.XPATH_AVAILABLE_SEAT}").nth(index).click()
        self.page.wait_for_timeout(500)

    def is_seat_selected(self) -> bool:
        """Check if a seat has been selected."""
        return self.count_xpath(self.XPATH_SELECTED_SEAT) > 0

    def get_selected_seat_info(self) -> str:
        """Get selected seat information text."""
        return self.get_text_xpath(self.XPATH_SEAT_INFO)

    def confirm_seat(self):
        """Confirm seat selection and proceed."""
        self.click_xpath(self.XPATH_CONFIRM_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def skip_seat_selection(self):
        """Skip seat selection (auto-assign by system)."""
        if self.is_visible_xpath(self.XPATH_SKIP_BUTTON):
            self.click_xpath(self.XPATH_SKIP_BUTTON)
            self.page.wait_for_load_state("networkidle")

    def select_coach(self, coach_number: str):
        """Select specific coach/gerbong."""
        self.page.locator(f"xpath={self.XPATH_COACH_SELECTOR}").select_option(coach_number)
        self.page.wait_for_timeout(1000)
