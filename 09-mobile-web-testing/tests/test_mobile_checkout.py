"""
Mobile Checkout Flow Tests - Verify complete purchase flow on mobile devices.
"""

import allure
import pytest


@allure.epic("Mobile Web Testing")
@allure.feature("Mobile Checkout")
class TestMobileCheckout:
    """Test checkout flow on mobile devices."""

    def _login(self, page):
        """Helper: Login on mobile."""
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").tap()
        page.wait_for_load_state("domcontentloaded")

    @allure.title("Complete checkout flow on mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    def test_full_checkout_flow(self, mobile_page):
        """Verify user can complete purchase on mobile device."""
        page, device_name = mobile_page

        with allure.step(f"Login on {device_name}"):
            self._login(page)

        with allure.step("Add product to cart"):
            page.locator("[data-test='add-to-cart-sauce-labs-backpack']").tap()
            page.wait_for_timeout(500)

        with allure.step("Go to cart"):
            page.locator(".shopping_cart_link").tap()
            page.wait_for_load_state("domcontentloaded")
            assert "/cart" in page.url

        with allure.step("Proceed to checkout"):
            page.locator("[data-test='checkout']").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step("Fill checkout information"):
            page.locator("[data-test='firstName']").fill("Bagas")
            page.locator("[data-test='lastName']").fill("Saputra")
            page.locator("[data-test='postalCode']").fill("12345")
            page.locator("[data-test='continue']").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step("Finish checkout"):
            page.locator("[data-test='finish']").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Verify order complete on {device_name}"):
            assert page.locator(".complete-header").is_visible()
            assert "Thank you" in page.locator(".complete-header").text_content()

    @allure.title("Cart persists after page refresh on mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_cart_persists_after_refresh(self, mobile_page):
        """Verify cart items persist after mobile page refresh."""
        page, device_name = mobile_page

        with allure.step("Login and add item"):
            self._login(page)
            page.locator("[data-test='add-to-cart-sauce-labs-backpack']").tap()
            page.wait_for_timeout(500)

        with allure.step("Refresh page"):
            page.reload()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Verify cart still has item on {device_name}"):
            badge = page.locator(".shopping_cart_badge")
            assert badge.is_visible()
            assert badge.text_content() == "1"

    @allure.title("Remove item from cart on mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_remove_from_cart(self, mobile_page):
        """Verify user can remove item from cart on mobile."""
        page, device_name = mobile_page

        with allure.step("Login and add item"):
            self._login(page)
            page.locator("[data-test='add-to-cart-sauce-labs-backpack']").tap()
            page.wait_for_timeout(500)

        with allure.step("Go to cart"):
            page.locator(".shopping_cart_link").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Remove item on {device_name}"):
            page.locator("[data-test='remove-sauce-labs-backpack']").tap()
            page.wait_for_timeout(500)

        with allure.step("Verify cart is empty"):
            assert not page.locator(".shopping_cart_badge").is_visible()

    @allure.title("Checkout validation on mobile - empty fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_checkout_validation(self, mobile_page):
        """Verify checkout form validation works on mobile."""
        page, device_name = mobile_page

        with allure.step("Login and add item"):
            self._login(page)
            page.locator("[data-test='add-to-cart-sauce-labs-backpack']").tap()

        with allure.step("Navigate to checkout"):
            page.locator(".shopping_cart_link").tap()
            page.wait_for_load_state("domcontentloaded")
            page.locator("[data-test='checkout']").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step("Submit empty form"):
            page.locator("[data-test='continue']").tap()

        with allure.step(f"Verify error message on {device_name}"):
            error = page.locator("[data-test='error']")
            assert error.is_visible()
            assert "First Name is required" in error.text_content()
