"""
Mobile Responsive Tests - Verify UI adapts correctly to mobile viewports.
Uses Playwright device emulation (no physical devices needed).
"""

import allure
import pytest


@allure.epic("Mobile Web Testing")
@allure.feature("Responsive Design")
class TestResponsive:
    """Test responsive behavior across mobile devices."""

    @allure.title("Login page renders correctly on mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    def test_login_page_renders_on_mobile(self, mobile_page):
        """Verify login page elements are visible on mobile viewport."""
        page, device_name = mobile_page
        
        with allure.step(f"Verify login form on {device_name}"):
            assert page.locator("#user-name").is_visible(), f"Username field not visible on {device_name}"
            assert page.locator("#password").is_visible(), f"Password field not visible on {device_name}"
            assert page.locator("#login-button").is_visible(), f"Login button not visible on {device_name}"

    @allure.title("Page viewport matches device width")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_viewport_width(self, mobile_page):
        """Verify page respects mobile viewport width."""
        page, device_name = mobile_page
        
        with allure.step(f"Check viewport on {device_name}"):
            viewport_width = page.evaluate("window.innerWidth")
            assert viewport_width <= 450, f"Viewport too wide for mobile on {device_name}: {viewport_width}px"

    @allure.title("Touch events are enabled on mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    def test_touch_enabled(self, mobile_page):
        """Verify touch capabilities are emulated."""
        page, device_name = mobile_page
        
        with allure.step(f"Check touch support on {device_name}"):
            has_touch = page.evaluate("'ontouchstart' in window")
            assert has_touch, f"Touch events not enabled on {device_name}"

    @allure.title("Login page renders correctly on tablet")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.tablet
    def test_login_page_renders_on_tablet(self, tablet_page):
        """Verify login page elements are visible on tablet viewport."""
        page, device_name = tablet_page
        
        with allure.step(f"Verify login form on {device_name}"):
            assert page.locator("#user-name").is_visible()
            assert page.locator("#password").is_visible()
            assert page.locator("#login-button").is_visible()

    @allure.title("Tablet viewport is between mobile and desktop")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.tablet
    def test_tablet_viewport(self, tablet_page):
        """Verify tablet viewport is in expected range."""
        page, device_name = tablet_page
        
        with allure.step(f"Check viewport on {device_name}"):
            viewport_width = page.evaluate("window.innerWidth")
            assert 700 <= viewport_width <= 1100, f"Unexpected tablet viewport: {viewport_width}px"
