"""
TC-001: Valid Login
TC-002: Invalid Login
Test cases for KAI Booking login functionality.
"""

import allure
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from tests.test_data import INVALID_CREDENTIALS


@allure.epic("KAI Booking")
@allure.feature("Authentication")
class TestLogin:
    """Test suite for login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize page objects."""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)

    @allure.story("Valid Login")
    @allure.title("TC-001: Login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_login(self, page, credentials):
        """Verify user can login with valid credentials."""
        with allure.step("Navigate to login page and enter credentials"):
            self.login_page.login(
                username=credentials["valid_user"],
                password=credentials["valid_password"],
            )

        with allure.step("Verify user is logged in"):
            assert self.login_page.is_logged_in(), "Login failed: user profile not visible"

        with allure.step("Verify home page search form is displayed"):
            assert self.home_page.is_search_form_displayed(), (
                "Home page search form not displayed after login"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-002: Login with wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_invalid_login_wrong_password(self, page, credentials):
        """Verify error message displayed for wrong password."""
        data = INVALID_CREDENTIALS["wrong_password"]

        with allure.step("Enter valid email with wrong password"):
            self.login_page.login(
                username=credentials["valid_user"],
                password=data["password"],
            )

        with allure.step("Verify error message is displayed"):
            assert self.login_page.is_error_displayed(), (
                "Error message not shown for invalid credentials"
            )

        with allure.step("Verify user stays on login page"):
            assert self.login_page.is_login_page(), (
                "User should remain on login page after failed login"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-002b: Login with unregistered email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login_wrong_email(self, page):
        """Verify error message displayed for unregistered email."""
        data = INVALID_CREDENTIALS["wrong_email"]

        with allure.step("Enter unregistered email"):
            self.login_page.login(
                username=data["username"],
                password=data["password"],
            )

        with allure.step("Verify error message is displayed"):
            assert self.login_page.is_error_displayed(), (
                "Error message not shown for unregistered email"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-002c: Login with empty fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_fields(self, page):
        """Verify validation when submitting empty credentials."""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login()

        with allure.step("Click login without filling fields"):
            self.login_page.click_login()

        with allure.step("Verify user remains on login page"):
            assert self.login_page.is_login_page(), (
                "User should remain on login page when fields are empty"
            )
