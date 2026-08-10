"""
TC-008: Logout
Test cases for logout functionality on KAI Booking.
"""

import allure
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


@allure.epic("KAI Booking")
@allure.feature("Authentication")
class TestLogout:
    """Test suite for logout functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page, login):
        """Setup: Login first (logout tests need authenticated state)."""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)

    @allure.story("Logout")
    @allure.title("TC-008: Successful logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_logout_success(self, page):
        """Verify user can successfully logout."""
        with allure.step("Verify user is on home page"):
            self.home_page.navigate_to_home()
            assert self.home_page.is_search_form_displayed()

        with allure.step("Click logout"):
            self.home_page.logout()

        with allure.step("Verify redirected to login page"):
            assert self.login_page.is_login_page(), (
                "User should be redirected to login page after logout"
            )

    @allure.story("Logout")
    @allure.title("TC-008b: Cannot access protected pages after logout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cannot_access_booking_after_logout(self, page):
        """Verify protected pages redirect to login after logout."""
        with allure.step("Logout"):
            self.home_page.navigate_to_home()
            self.home_page.logout()

        with allure.step("Try to access protected page"):
            self.home_page.navigate_to_home()

        with allure.step("Verify redirect to login"):
            assert self.login_page.is_login_page()

    @allure.story("Logout")
    @allure.title("TC-008c: Re-login after logout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_after_logout(self, page, credentials):
        """Verify user can login again after logging out."""
        with allure.step("Logout"):
            self.home_page.navigate_to_home()
            self.home_page.logout()

        with allure.step("Login again"):
            self.login_page.login(
                username=credentials["valid_user"],
                password=credentials["valid_password"],
            )

        with allure.step("Verify login successful"):
            assert self.login_page.is_logged_in(), (
                "User should be able to login again after logout"
            )
