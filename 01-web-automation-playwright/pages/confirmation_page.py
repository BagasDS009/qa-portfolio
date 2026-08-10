"""Order Confirmation Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class ConfirmationPage(BasePage):
    """Page Object for order/booking confirmation page using XPath."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_SUCCESS_MSG = "//*[contains(@class,'success') or contains(text(),'Berhasil') or contains(text(),'Sukses')]"
    XPATH_BOOKING_CODE = "//*[contains(@class,'booking-code') or contains(@class,'kode-booking') or contains(@class,'pnr')]"
    XPATH_TRAIN_INFO = "//div[contains(@class,'train-info') or contains(@class,'detail-kereta')]"
    XPATH_DEPARTURE_INFO = "//*[contains(@class,'departure') or contains(@class,'keberangkatan')]"
    XPATH_PASSENGER_INFO = "//*[contains(@class,'passenger') or contains(@class,'penumpang')]"
    XPATH_DOWNLOAD_BTN = "//button[contains(text(),'Unduh') or contains(text(),'Download')]|//a[contains(text(),'E-Ticket')]"
    XPATH_BACK_HOME = "//a[contains(text(),'Beranda') or contains(text(),'Home')]|//button[contains(text(),'Kembali')]"
    XPATH_PAYMENT_STATUS = "//*[contains(@class,'payment-status') or contains(@class,'status-bayar')]"

    def is_booking_confirmed(self) -> bool:
        """Check if booking is confirmed successfully."""
        return self.is_visible_xpath(
            self.XPATH_SUCCESS_MSG
        ) or self.is_visible_xpath(self.XPATH_BOOKING_CODE)

    def get_booking_code(self) -> str:
        """Get booking confirmation code."""
        return self.get_text_xpath(self.XPATH_BOOKING_CODE).strip()

    def get_train_info(self) -> str:
        """Get booked train information."""
        return self.get_text_xpath(self.XPATH_TRAIN_INFO)

    def get_departure_info(self) -> str:
        """Get departure details."""
        return self.get_text_xpath(self.XPATH_DEPARTURE_INFO)

    def get_passenger_info(self) -> str:
        """Get passenger information."""
        return self.get_text_xpath(self.XPATH_PASSENGER_INFO)

    def get_payment_status(self) -> str:
        """Get payment status text."""
        return self.get_text_xpath(self.XPATH_PAYMENT_STATUS)

    def click_download_ticket(self):
        """Click download e-ticket button."""
        self.click_xpath(self.XPATH_DOWNLOAD_BTN)

    def go_back_to_home(self):
        """Navigate back to home page."""
        self.click_xpath(self.XPATH_BACK_HOME)
        self.page.wait_for_load_state("networkidle")

    def is_payment_pending(self) -> bool:
        """Check if payment status is pending."""
        status = self.get_payment_status().lower()
        return "pending" in status or "menunggu" in status
