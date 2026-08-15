"""
TC-005: End-to-end checkout flow
Test cases for complete purchase flow (login → add to cart → checkout → address → payment → confirm).
"""

import allure
import pytest

from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from tests.test_data import VALID_CUSTOMER, BILLING_ADDRESS


@allure.epic("Toolshop E-Commerce")
@allure.feature("Checkout Flow")
class TestCheckout:
    """Test suite for end-to-end checkout flow."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize page objects."""
        self.home_page = HomePage(page)
        self.product_page = ProductDetailPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.login_page = LoginPage(page)

    def _login_and_add_to_cart(self, page):
        """Helper: Login first, then add a product to cart."""
        # Login
        self.login_page.login(
            email=VALID_CUSTOMER["email"],
            password=VALID_CUSTOMER["password"],
        )
        page.wait_for_timeout(3000)

        # Add product to cart
        self.home_page.navigate_to_home()
        self.home_page.click_product(0)
        self.product_page.add_to_cart()

    @allure.story("Complete Checkout")
    @allure.title("TC-005a: Complete end-to-end checkout with bank transfer")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_complete_checkout(self, page):
        """Verify user can complete full checkout flow."""
        with allure.step("Step 1: Login and add product to cart"):
            self._login_and_add_to_cart(page)

        with allure.step("Step 2: Navigate to cart and proceed"):
            self.cart_page.navigate_to_cart()
            assert self.cart_page.get_cart_items_count() >= 1, "Cart is empty"
            self.cart_page.proceed_to_checkout()

        with allure.step("Step 3: Proceed past sign-in step (already logged in)"):
            self.checkout_page.proceed_past_sign_in()

        with allure.step("Step 4: Fill billing address"):
            self.checkout_page.fill_billing_address(
                street=BILLING_ADDRESS["street"],
                house_number=BILLING_ADDRESS["house_number"],
                city=BILLING_ADDRESS["city"],
                state=BILLING_ADDRESS["state"],
                country=BILLING_ADDRESS["country"],
                postcode=BILLING_ADDRESS["postcode"],
            )
            self.checkout_page.proceed_to_payment()

        with allure.step("Step 5: Select payment and fill bank details"):
            self.checkout_page.select_payment_method("Bank Transfer")
            self.checkout_page.fill_bank_transfer()
            self.checkout_page.confirm_payment()

        with allure.step("Step 6: Verify order confirmation"):
            assert self.checkout_page.is_checkout_complete(), (
                "Checkout did not complete — confirmation not displayed"
            )

    @allure.story("Checkout Validation")
    @allure.title("TC-005b: Cannot proceed without billing address")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_requires_address(self, page):
        """Verify checkout requires billing address to proceed."""
        with allure.step("Login and add product to cart"):
            self._login_and_add_to_cart(page)

        with allure.step("Go to cart and proceed through steps"):
            self.cart_page.navigate_to_cart()
            self.cart_page.proceed_to_checkout()
            self.checkout_page.proceed_past_sign_in()

        with allure.step("Verify billing form is displayed"):
            assert self.checkout_page.is_on_billing_step(), (
                "Billing address form should be visible at step 3"
            )

        with allure.step("Try to proceed without filling address"):
            # The proceed button should be disabled when address is empty
            proceed_btn = page.locator("[data-test='proceed-3']")
            is_disabled = proceed_btn.is_disabled()
            assert is_disabled, (
                "Proceed button should be disabled when billing address is empty"
            )
