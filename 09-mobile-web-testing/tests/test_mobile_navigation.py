"""
Mobile Navigation Tests - Verify user flows work on mobile devices.
"""

import allure
import pytest


@allure.epic("Mobile Web Testing")
@allure.feature("Mobile Navigation")
class TestMobileNavigation:
    """Test user navigation flows on mobile devices."""

    @allure.title("User can login on mobile device")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    def test_mobile_login(self, mobile_page):
        """Verify login flow works on mobile."""
        page, device_name = mobile_page
        
        with allure.step(f"Login on {device_name}"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("secret_sauce")
            page.locator("#login-button").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step("Verify redirected to inventory page"):
            assert "/inventory" in page.url, f"Login failed on {device_name}"

    @allure.title("Products are scrollable on mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_mobile_scroll(self, mobile_page):
        """Verify user can scroll through products on mobile."""
        page, device_name = mobile_page
        
        with allure.step("Login first"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("secret_sauce")
            page.locator("#login-button").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Scroll down on {device_name}"):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            scroll_y = page.evaluate("window.scrollY")
            assert scroll_y > 0, f"Page did not scroll on {device_name}"

    @allure.title("Add to cart works with touch/tap on mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    def test_mobile_add_to_cart(self, mobile_page):
        """Verify add to cart button responds to tap on mobile."""
        page, device_name = mobile_page
        
        with allure.step("Login"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("secret_sauce")
            page.locator("#login-button").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Tap 'Add to cart' on {device_name}"):
            page.locator("[data-test='add-to-cart-sauce-labs-backpack']").tap()
            page.wait_for_timeout(500)

        with allure.step("Verify cart badge shows 1"):
            badge = page.locator(".shopping_cart_badge")
            assert badge.is_visible(), f"Cart badge not visible on {device_name}"
            assert badge.text_content() == "1", f"Cart badge not '1' on {device_name}"

    @allure.title("Hamburger menu works on mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_mobile_hamburger_menu(self, mobile_page):
        """Verify hamburger/sidebar menu opens on mobile."""
        page, device_name = mobile_page
        
        with allure.step("Login"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("secret_sauce")
            page.locator("#login-button").tap()
            page.wait_for_load_state("domcontentloaded")

        with allure.step(f"Open hamburger menu on {device_name}"):
            page.locator("#react-burger-menu-btn").tap()
            page.wait_for_timeout(500)

        with allure.step("Verify menu items are visible"):
            assert page.locator("#inventory_sidebar_link").is_visible(), "Menu item not visible"
