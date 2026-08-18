"""Seat Selection Page Object for KAI Booking."""

from pages.base_page import BasePage


class SeatPage(BasePage):
    """Page Object for interactive seat map."""

    XPATH_SEAT_MAP = '//div[contains(@class,"seat-map") or contains(@class,"seat-layout") or contains(@class,"seat-container")]'
    XPATH_AVAILABLE = '//div[contains(@class,"seat") and not(contains(@class,"occupied")) and not(contains(@class,"selected")) and not(contains(@class,"disabled"))]'
    XPATH_SELECTED = '//div[contains(@class,"seat") and (contains(@class,"selected") or contains(@class,"active"))]'
    XPATH_OCCUPIED = '//div[contains(@class,"seat") and (contains(@class,"occupied") or contains(@class,"disabled"))]'
    XPATH_CONFIRM_BTN = '//button[contains(text(),"Konfirmasi") or contains(text(),"Lanjutkan")]'
    XPATH_SKIP_BTN = '//button[contains(text(),"Lewati")]|//a[contains(text(),"Pilih Nanti")]'
    XPATH_SEAT_INFO = '//*[contains(@class,"seat-info") or contains(@class,"selected-seat")]'

    # Actions

    def select_first_available(self) -> None:
        """Click first available (green) seat."""
        self.page.locator(f"xpath={self.XPATH_AVAILABLE}").first.click()
        self.page.wait_for_timeout(500)

    def select_seat_by_index(self, index: int) -> None:
        """Select specific available seat by index."""
        self.page.locator(f"xpath={self.XPATH_AVAILABLE}").nth(index).click()
        self.page.wait_for_timeout(500)

    def confirm_seat(self) -> None:
        """Click confirm button after selecting seat."""
        self.click_xpath(self.XPATH_CONFIRM_BTN)
        self.page.wait_for_load_state("load")
        self.human_delay(1000, 2000)

    def skip_selection(self) -> None:
        """Skip seat selection (auto-assign)."""
        if self.is_visible_xpath(self.XPATH_SKIP_BTN):
            self.click_xpath(self.XPATH_SKIP_BTN)
            self.page.wait_for_load_state("load")

    # Verifications

    def is_seat_map_visible(self) -> bool:
        return self.is_visible_xpath(self.XPATH_SEAT_MAP)

    def get_available_count(self) -> int:
        return self.count_xpath(self.XPATH_AVAILABLE)

    def is_seat_selected(self) -> bool:
        return self.count_xpath(self.XPATH_SELECTED) > 0

    def get_seat_info(self) -> str:
        return self.get_text_xpath(self.XPATH_SEAT_INFO)
