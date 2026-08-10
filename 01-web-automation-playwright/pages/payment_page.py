"""Payment Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class PaymentPage(BasePage):
    """Page Object for payment/checkout page using XPath."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_PAYMENT_METHODS = "//div[contains(@class,'payment-method') or contains(@class,'payment-list')]"
    XPATH_PAYMENT_OPTION = "//div[contains(@class,'payment-item') or contains(@class,'pay-method')]"
    XPATH_BOOKING_CODE = "//*[contains(@class,'booking-code') or contains(@class,'kode-booking') or contains(@class,'pnr')]"
    XPATH_TOTAL_PRICE = "//*[contains(@class,'total') and contains(@class,'price')]|//*[contains(@class,'total-bayar')]"
    XPATH_PAY_BUTTON = "//button[contains(text(),'Bayar') or contains(text(),'Pay') or contains(text(),'Konfirmasi')]"
    XPATH_COUNTDOWN = "//*[contains(@class,'countdown') or contains(@class,'timer')]"
    XPATH_BANK_TRANSFER = "//*[contains(text(),'Transfer') or contains(text(),'Bank')]"
    XPATH_EWALLET = "//*[contains(text(),'E-Wallet') or contains(text(),'QRIS')]"
    XPATH_ORDER_SUMMARY = "//div[contains(@class,'summary') or contains(@class,'ringkasan')]"

    def is_payment_page_displayed(self) -> bool:
        """Check if payment page is displayed."""
        return self.is_visible_xpath(
            self.XPATH_PAYMENT_METHODS
        ) or self.is_visible_xpath(self.XPATH_BOOKING_CODE)

    def get_booking_code(self) -> str:
        """Get booking/reservation code."""
        return self.get_text_xpath(self.XPATH_BOOKING_CODE).strip()

    def get_total_price(self) -> str:
        """Get total payment amount."""
        return self.get_text_xpath(self.XPATH_TOTAL_PRICE).strip()

    def select_payment_method(self, method: str = "bank_transfer"):
        """Select payment method by type."""
        if method == "bank_transfer":
            self.click_xpath(self.XPATH_BANK_TRANSFER)
        elif method == "ewallet":
            self.click_xpath(self.XPATH_EWALLET)
        else:
            self.page.locator(f"xpath={self.XPATH_PAYMENT_OPTION}").first.click()
        self.page.wait_for_timeout(1000)

    def click_pay(self):
        """Click pay/confirm payment button."""
        self.click_xpath(self.XPATH_PAY_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_order_summary(self) -> str:
        """Get order summary text."""
        return self.get_text_xpath(self.XPATH_ORDER_SUMMARY)

    def is_countdown_displayed(self) -> bool:
        """Check if payment countdown timer is visible."""
        return self.is_visible_xpath(self.XPATH_COUNTDOWN)

    def get_available_payment_methods(self) -> int:
        """Get count of available payment methods."""
        return self.count_xpath(self.XPATH_PAYMENT_OPTION)
