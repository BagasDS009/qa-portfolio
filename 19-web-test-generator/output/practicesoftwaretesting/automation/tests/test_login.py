"""
TC-LOGIN-001 to TC-LOGIN-008: Authentication test suite.
Covers: valid login, invalid credentials, empty fields, security inputs.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from test_data.users import VALID_CUSTOMER, VALID_ADMIN, INVALID_CREDENTIALS


@allure.epic("Practice Software Testing")
@allure.feature("Authentication")
@pytest.mark.wave1
class TestLogin:
    """Login functionality test suite."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)

    # === CRITICAL ===

    @allure.story("Valid Login")
    @allure.title("TC-LOGIN-001: Login with valid customer credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.login
    def test_login_valid_credentials(self, page: Page):
        """Verify customer can login with correct email and password."""
        with allure.step("Login with valid credentials"):
            self.login_page.login(VALID_CUSTOMER["email"], VALID_CUSTOMER["password"])

        with allure.step("Verify redirect to account page"):
            assert self.login_page.is_logged_in(), (
                f"Expected redirect to /account after valid login, "
                f"but still on: {page.url}"
            )

    # === POSITIVE ===

    @allure.story("Valid Login")
    @allure.title("TC-LOGIN-002: Login with admin credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_admin(self, page: Page):
        """Verify admin can login successfully."""
        with allure.step("Login as admin"):
            self.login_page.login(VALID_ADMIN["email"], VALID_ADMIN["password"])

        with allure.step("Verify login success (redirect away from login)"):
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            assert "/auth/login" not in page.url, (
                f"Admin login failed — still on login page: {page.url}"
            )

    # === NEGATIVE ===

    @allure.story("Invalid Login")
    @allure.title("TC-LOGIN-003: Login with wrong password shows error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.login
    def test_login_wrong_password(self, page: Page):
        """Verify error message when password is incorrect."""
        creds = INVALID_CREDENTIALS["wrong_password"]

        with allure.step("Attempt login with wrong password"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify error message displayed"):
            assert self.login_page.is_error_displayed(), (
                "No error message shown for wrong password"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-LOGIN-004: Login with unregistered email shows error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.login
    def test_login_unregistered_email(self, page: Page):
        """Verify error for non-existent email."""
        creds = INVALID_CREDENTIALS["unregistered"]

        with allure.step("Login with unregistered email"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify error displayed"):
            assert self.login_page.is_error_displayed(), (
                "No error message shown for unregistered email"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-LOGIN-005: Login with empty email field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.login
    def test_login_empty_email(self, page: Page):
        """Verify validation when email is empty."""
        creds = INVALID_CREDENTIALS["empty_email"]

        with allure.step("Submit login with empty email"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify stays on login page"):
            assert self.login_page.is_on_login_page(), (
                "Should remain on login page with empty email"
            )

    @allure.story("Invalid Login")
    @allure.title("TC-LOGIN-006: Login with empty password field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.login
    def test_login_empty_password(self, page: Page):
        """Verify validation when password is empty."""
        creds = INVALID_CREDENTIALS["empty_password"]

        with allure.step("Submit login with empty password"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify stays on login page"):
            assert self.login_page.is_on_login_page(), (
                "Should remain on login page with empty password"
            )

    # === EDGE CASES ===

    @allure.story("Security")
    @allure.title("TC-LOGIN-007: SQL injection in email field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.login
    def test_login_sql_injection(self, page: Page):
        """Verify SQL injection attempt is safely handled."""
        creds = INVALID_CREDENTIALS["sql_injection"]

        with allure.step("Attempt SQL injection in email"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify no unauthorized access"):
            assert self.login_page.is_on_login_page() or self.login_page.is_error_displayed(), (
                "SQL injection may have bypassed authentication"
            )

    @allure.story("Security")
    @allure.title("TC-LOGIN-008: XSS attempt in email field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.login
    def test_login_xss_attempt(self, page: Page):
        """Verify XSS script is not executed."""
        creds = INVALID_CREDENTIALS["xss_attempt"]

        with allure.step("Enter XSS payload in email field"):
            self.login_page.login(creds["email"], creds["password"])

        with allure.step("Verify script not executed (page still functional)"):
            assert self.login_page.is_on_login_page() or self.login_page.is_error_displayed(), (
                "Page may be compromised by XSS"
            )
