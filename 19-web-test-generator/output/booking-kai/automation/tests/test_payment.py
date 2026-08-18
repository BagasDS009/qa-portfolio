"""
TC-PAYMENT-001 to TC-PAYMENT-003: Payment page UI validation for KAI Booking.

Precondition handled by fixture: full booking chain → arrive at payment page.
WARNING: NEVER click Pay button — will charge real money.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.payment_page import PaymentPage


@allure.epic("KAI Online Booking")
@allure.feature("Payment")
@pytest.mark.wave1
class TestPayment:
    """Payment page UI validation — NO actual payment.
    
    Uses `at_payment_page` fixture for precondition.
    """

    # === CRITICAL ===

    @allure.story("Payment Page")
    @allure.title("TC-PAYMENT-001: Booking code and total price displayed")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.critical
    @pytest.mark.payment
    def test_payment_page_displays_info(self, at_payment_page: Page):
        """Verify booking code and total amount shown on payment page."""
        payment = PaymentPage(at_payment_page)

        with allure.step("Verify payment page visible"):
            assert payment.is_payment_page_visible(), "Not on payment page"

        with allure.step("Verify booking code displayed"):
            code = payment.get_booking_code()
            assert code != "", "Booking code should not be empty"

        with allure.step("Verify total price displayed"):
            total = payment.get_total_price()
            assert total != "", "Total price should not be empty"

    # === POSITIVE ===

    @allure.story("Payment Methods")
    @allure.title("TC-PAYMENT-002: Multiple payment methods available")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    @pytest.mark.payment
    def test_payment_methods_listed(self, at_payment_page: Page):
        """Verify at least 2 payment methods available."""
        payment = PaymentPage(at_payment_page)

        with allure.step("Check payment methods count"):
            count = payment.get_payment_methods_count()
            assert count >= 2, f"Expected >= 2 methods, got {count}"

    # === EDGE ===

    @allure.story("Payment Timer")
    @allure.title("TC-PAYMENT-003: Countdown timer visible")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.e2e
    @pytest.mark.edge
    @pytest.mark.payment
    def test_countdown_timer(self, at_payment_page: Page):
        """Verify payment deadline countdown displayed."""
        payment = PaymentPage(at_payment_page)

        with allure.step("Verify countdown visible"):
            assert payment.is_countdown_visible(), "Countdown timer should be shown"
