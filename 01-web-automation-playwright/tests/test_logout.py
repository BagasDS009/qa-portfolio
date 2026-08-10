"""
TC-008: Logout
Test cases for logout functionality on KAI Booking.
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


class TestLogout:
    """Test suite for logout functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page, login):
        """Setup: Login and initialize page objects."""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)

    @pytest.mark.smoke
    def test_logout_success(self, page):
        """
        TC-008: Logout
        Verify user can successfully logout.
        """
        self.home_page.navigate_to_home()
        assert self.home_page.is_search_form_displayed(), (
            "User should be on home page (logged in)"
        )

        self.home_page.logout()

        assert self.login_page.is_login_page(), (
            "User should be redirected to login page after logout"
        )
        assert not self.login_page.is_logged_in(), (
            "User profile should not be visible after logout"
        )

    def test_cannot_access_booking_after_logout(self, page):
        """
        TC-008b: Session invalidation after logout
        Verify protected pages redirect to login after logout.
        """
        self.home_page.navigate_to_home()
        self.home_page.logout()

        # Try to access protected page directly
        self.home_page.navigate_to_home()

        assert self.login_page.is_login_page(), (
            "User should be redirected to login after logout"
        )

    def test_login_after_logout(self, page, credentials):
        """
        TC-008c: Re-login after logout
        Verify user can login again after logging out.
        """
        self.home_page.navigate_to_home()
        self.home_page.logout()

        self.login_page.login(
            username=credentials["valid_user"],
            password=credentials["valid_password"],
        )

        assert self.login_page.is_logged_in(), (
            "User should be able to login again after logout"
        )
