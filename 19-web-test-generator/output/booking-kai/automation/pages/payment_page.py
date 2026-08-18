"""Payment Page Object for KAI Booking.

WARNING: NEVER automate actual payment submission. Test UI validation only.
"""

from pages.base_page import BasePage


class PaymentPage(BasePage):
    """Page Object for payment page — UI validation ONLY (no real payment)."""

    XPATH_BOOKING_CODE = '//*[contains(@class,"booking-code") or contains(@class,"kode-booking") or contains(@class,"pnr")]'
    XPATH_TOTAL_PRICE = '//*[contains(@class,"total") and contains(@class,"price")]|//*[contains(@class,"total-bayar")]'
    XPATH_PAYMENT_METHODS = '//div[contains(@class,"payment-method") or contains(@class,"payment-list")]'
    XPATH_PAYMENT_OPTION = '//div[contains(@class,"payment-item") or contains(@class,"pay-method")]'
    XPATH_COUNTDOWN = '//*[contains(@class,"countdown") or contains(@class,"timer")]'
    XPATH_BANK_TRANSFER = '//*[contains(text(),"Transfer") or contains(text(),"Bank")]'
    XPATH_EWALLET = '//*[contains(text(),"E-Wallet") or contains(text(),"QRIS")]'

    # Verifications ONLY — no payment actions

    def is_payment_page_visible(self) -> bool:
        """Check if payment page is displayed."""
        return (self.is_visible_xpath(self.XPATH_PAYMENT_METHODS) or
                self.is_visible_xpath(self.XPATH_BOOKING_CODE))

    def get_booking_code(self) -> str:
        """Get booking/reservation code."""
        return self.get_text_xpath(self.XPATH_BOOKING_CODE).strip()

    def get_total_price(self) -> str:
        """Get total payment amount (e.g., 'Rp 350.000')."""
        return self.get_text_xpath(self.XPATH_TOTAL_PRICE).strip()

    def get_payment_methods_count(self) -> int:
        """Count available payment methods."""
        return self.count_xpath(self.XPATH_PAYMENT_OPTION)

    def has_bank_transfer(self) -> bool:
        """Check if bank transfer option exists."""
        return self.is_visible_xpath(self.XPATH_BANK_TRANSFER)

    def has_ewallet(self) -> bool:
        """Check if e-wallet/QRIS option exists."""
        return self.is_visible_xpath(self.XPATH_EWALLET)

    def is_countdown_visible(self) -> bool:
        """Check if payment countdown timer is displayed."""
        return self.is_visible_xpath(self.XPATH_COUNTDOWN)
