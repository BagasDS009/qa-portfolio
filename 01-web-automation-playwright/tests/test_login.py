"""
TC-001: Valid Login
TC-002: Invalid Login
Test cases for KAI Booking login functionality.
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from tests.test_data import INVALID_CREDENTIALS


class TestLogin:
    """Test suite for login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize page objects."""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)

    @pytest.mark.smoke
    def test_valid_login(self, page, credentials):
        """
        TC-001: Valid Login
        Verify user can login with valid credentials.
        """
        self.login_page.login(
            username=credentials["valid_user"],
            password=credentials["valid_password"],
        )

        assert self.login_page.is_logged_in(), "Login failed: user profile not visible"
        assert self.home_page.is_search_form_displayed(), (
            "Home page search form not displayed after login"
        )

    @pytest.mark.smoke
    def test_invalid_login_wrong_password(self, page, credentials):
        """
        TC-002: Invalid Login - Wrong Password
        Verify error message displayed for wrong password.
        """
        data = INVALID_CREDENTIALS["wrong_password"]
        self.login_page.login(
            username=credentials["valid_user"],
            password=data["password"],
        )

        assert self.login_page.is_error_displayed(), (
            "Error message not shown for invalid credentials"
        )
        assert self.login_page.is_login_page(), (
            "User should remain on login page after failed login"
        )

    def test_invalid_login_wrong_email(self, page):
        """
        TC-002b: Invalid Login - Wrong Email
        Verify error message displayed for unregistered email.
        """
        data = INVALID_CREDENTIALS["wrong_email"]
        self.login_page.login(
            username=data["username"],
            password=data["password"],
        )

        assert self.login_page.is_error_displayed(), (
            "Error message not shown for unregistered email"
        )

    def test_login_empty_fields(self, page):
        """
        TC-002c: Invalid Login - Empty Fields
        Verify validation when submitting empty credentials.
        """
        self.login_page.navigate_to_login()
        self.login_page.click_login()

        assert self.login_page.is_login_page(), (
            "User should remain on login page when fields are empty"
        )
