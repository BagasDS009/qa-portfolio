"""
TC-CHECKOUT-001 to TC-CHECKOUT-009: Checkout flow test suite.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from test_data.users import VALID_CUSTOMER
from test_data.addresses import VALID_ADDRESS, VALID_BANK_TRANSFER


@allure.epic("Practice Software Testing")
@allure.feature("Checkout")
@pytest.mark.wave1
class TestCheckout:
    """Multi-step checkout flow test suite."""

    @pytest.fixture
    def checkout_ready(self, page: Page) -> Page:
        """Fixture: logged in with item in cart, at checkout."""
        # Login
        login = LoginPage(page)
        login.login(VALID_CUSTOMER["email"], VALID_CUSTOMER["password"])
        page.wait_for_load_state("networkidle")

        # Add product to cart
        home = HomePage(page)
        home.navigate_to_home()
        home.click_product(0)
        ProductDetailPage(page).add_to_cart()

        # Go to cart and proceed
        cart = CartPage(page)
        cart.navigate_to_cart()
        cart.proceed_to_checkout()
        return page

    # === CRITICAL ===

    @allure.story("Complete Checkout")
    @allure.title("TC-CHECKOUT-001: Complete checkout with bank transfer")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.checkout
    def test_checkout_bank_transfer(self, checkout_ready: Page):
        """Verify full checkout flow with bank transfer payment."""
        checkout = CheckoutPage(checkout_ready)

        with allure.step("Complete checkout"):
            checkout.complete_checkout(
                street=VALID_ADDRESS["street"],
                house_number=VALID_ADDRESS["house_number"],
                city=VALID_ADDRESS["city"],
                state=VALID_ADDRESS["state"],
                country=VALID_ADDRESS["country"],
                postcode=VALID_ADDRESS["postcode"],
                payment_method="Bank Transfer",
            )

        with allure.step("Verify payment success message"):
            assert checkout.is_checkout_complete(), (
                "Checkout did not complete — success message not shown"
            )
            msg = checkout.get_confirmation_message()
            assert "success" in msg.lower(), f"Unexpected confirmation: '{msg}'"

    # === POSITIVE ===

    @allure.story("Complete Checkout")
    @allure.title("TC-CHECKOUT-002: Checkout with Cash on Delivery")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_cash_on_delivery(self, checkout_ready: Page):
        """Verify checkout with cash on delivery (no extra fields)."""
        checkout = CheckoutPage(checkout_ready)

        with allure.step("Complete checkout with Cash on Delivery"):
            checkout.complete_checkout(
                street=VALID_ADDRESS["street"],
                house_number=VALID_ADDRESS["house_number"],
                city=VALID_ADDRESS["city"],
                state=VALID_ADDRESS["state"],
                country=VALID_ADDRESS["country"],
                postcode=VALID_ADDRESS["postcode"],
                payment_method="Cash on Delivery",
            )

        with allure.step("Verify success"):
            assert checkout.is_checkout_complete(), "Cash on Delivery checkout failed"

    @allure.story("Complete Checkout")
    @allure.title("TC-CHECKOUT-003: Checkout with different country")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_different_country(self, checkout_ready: Page):
        """Verify checkout works with different billing country."""
        checkout = CheckoutPage(checkout_ready)

        with allure.step("Complete checkout with US address"):
            checkout.complete_checkout(
                street="456 Main St",
                house_number="1A",
                city="New York",
                state="NY",
                country="US",
                postcode="10001",
                payment_method="Bank Transfer",
            )

        with allure.step("Verify success"):
            assert checkout.is_checkout_complete(), "Checkout with US address failed"

    # === NEGATIVE ===

    @allure.story("Validation")
    @allure.title("TC-CHECKOUT-004: Empty billing address fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_empty_billing(self, checkout_ready: Page):
        """Verify cannot proceed with empty billing address."""
        checkout = CheckoutPage(checkout_ready)

        with allure.step("Proceed past sign-in"):
            checkout.proceed_sign_in()

        with allure.step("Verify proceed button is disabled when address is empty"):
            # The site disables the proceed button when required fields are empty
            # This IS the validation — button stays disabled until all fields filled
            proceed_btn = checkout_ready.locator("[data-test='proceed-3']")
            is_disabled = proceed_btn.is_disabled()
            assert is_disabled, (
                "Proceed button should be disabled when billing address fields are empty"
            )

    @allure.story("Validation")
    @allure.title("TC-CHECKOUT-005: Empty bank transfer fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_empty_payment(self, checkout_ready: Page):
        """Verify cannot confirm with empty payment details."""
        checkout = CheckoutPage(checkout_ready)

        with allure.step("Fill billing and proceed"):
            checkout.proceed_sign_in()
            checkout.fill_billing_address(
                VALID_ADDRESS["street"], VALID_ADDRESS["house_number"],
                VALID_ADDRESS["city"], VALID_ADDRESS["state"],
                VALID_ADDRESS["country"], VALID_ADDRESS["postcode"],
            )
            checkout.proceed_to_payment()

        with allure.step("Select Bank Transfer but leave fields empty"):
            checkout.select_payment_method("Bank Transfer")

        with allure.step("Verify confirm button is disabled when payment fields empty"):
            # Site disables the confirm button until payment fields are filled
            confirm_btn = checkout_ready.locator("[data-test='finish']")
            assert confirm_btn.is_disabled(), (
                "Confirm button should be disabled when bank transfer fields are empty"
            )

    @allure.story("Authentication")
    @allure.title("TC-CHECKOUT-006: Checkout blocked without login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_without_login(self, page: Page):
        """Verify checkout requires authentication at sign-in step."""
        # Add product without logging in
        home = HomePage(page)
        home.navigate_to_home()
        home.click_product(0)
        ProductDetailPage(page).add_to_cart()

        cart = CartPage(page)
        cart.navigate_to_cart()

        with allure.step("Proceed to checkout (not logged in)"):
            cart.proceed_to_checkout()

        with allure.step("Verify login required (cannot proceed past Step 2)"):
            checkout = CheckoutPage(page)
            # Should show login form or block at Step 2
            page.wait_for_timeout(2000)
            assert not checkout.is_on_billing_step(), (
                "Should not reach billing step without login"
            )
