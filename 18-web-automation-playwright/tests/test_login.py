"""
TC-001: Login with valid credentials
TC-002: Login with invalid credentials
Authentication test cases for Toolshop.
"""

import allure
import pytest

from pages.login_page import LoginPage
from tests.test_data import VALID_CUSTOMER, INVALID_CREDENTIALS


@allure.epic("Toolshop E-Commerce")
@allure.feature("Authentication")
class TestLogin:
    """Test suite for login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize login page."""
        self.login_page = LoginPage(page)

    @allure.story("Invalid Login")
    @allure.title("TC-002a: Login with wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_wrong_password(self, page):
        """Verify error message when using wrong password."""
        creds = INVALID_CREDENTIALS["wrong_password"]

        with allure.step("Attempt login with wrong password"):
            self.login_page.login(
                email=creds["email"],
                password=creds["password"],
            )

        with allure.step("Verify error message is displayed"):
            assert self.login_page.is_error_displayed(), (
                "No error message shown for wrong password"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-002b: Login with unregistered email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_unregistered_email(self, page):
        """Verify error message when using unregistered email."""
        creds = INVALID_CREDENTIALS["unregistered_email"]

        with allure.step("Attempt login with unregistered email"):
            self.login_page.login(
                email=creds["email"],
                password=creds["password"],
            )

        with allure.step("Verify error message is displayed"):
            assert self.login_page.is_error_displayed(), (
                "No error message shown for unregistered email"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-002c: Login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_empty_credentials(self, page):
        """Verify error when submitting empty login form."""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to_login()

        with allure.step("Click login without entering credentials"):
            self.login_page.click_login()

        with allure.step("Verify user stays on login page"):
            assert self.login_page.is_login_page(), (
                "User should remain on login page with empty fields"
            )
