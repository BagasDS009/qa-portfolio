"""Login Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for /auth/login."""

    # Selectors
    INPUT_EMAIL = "[data-test='email']"
    INPUT_PASSWORD = "[data-test='password']"
    BTN_LOGIN = "[data-test='login-submit']"
    LINK_REGISTER = "[data-test='register-link']"
    LINK_FORGOT_PASSWORD = "[data-test='forgot-password-link']"
    ERROR_MESSAGE = "[data-test='login-error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def navigate_to_login(self) -> None:
        """Navigate to login page."""
        self.navigate("auth/login")

    def login(self, email: str, password: str) -> None:
        """Complete login flow: navigate + fill + submit."""
        self.navigate_to_login()
        self.page.locator(self.INPUT_EMAIL).fill(email)
        self.page.locator(self.INPUT_PASSWORD).fill(password)
        self.page.locator(self.BTN_LOGIN).click()

    def click_login_button(self) -> None:
        """Click login button without filling fields."""
        self.page.locator(self.BTN_LOGIN).click()

    def click_register_link(self) -> None:
        """Click link to registration page."""
        self.page.locator(self.LINK_REGISTER).click()

    # Verifications

    def is_logged_in(self) -> bool:
        """Check if user is logged in (redirected away from login)."""
        try:
            self.page.wait_for_url("**/account", timeout=10000)
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get login error text."""
        try:
            self.page.locator(self.ERROR_MESSAGE).wait_for(state="visible", timeout=5000)
            return self.page.locator(self.ERROR_MESSAGE).text_content() or ""
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        """Check if error message is visible."""
        try:
            self.page.locator(self.ERROR_MESSAGE).wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def is_on_login_page(self) -> bool:
        """Verify still on login page."""
        return "/auth/login" in self.get_current_url()
