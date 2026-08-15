"""Login Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the login/sign-in page."""

    # ============================================================
    # Selectors (data-test attributes)
    # ============================================================
    INPUT_EMAIL = "[data-test='email']"
    INPUT_PASSWORD = "[data-test='password']"
    BTN_LOGIN = "[data-test='login-submit']"
    LINK_REGISTER = "[data-test='register-link']"
    LINK_FORGOT_PASSWORD = "[data-test='forgot-password-link']"
    ERROR_MESSAGE = "[data-test='login-error']"

    # ============================================================
    # Actions
    # ============================================================

    def navigate_to_login(self) -> None:
        """Navigate to login page."""
        self.navigate("auth/login")

    def enter_email(self, email: str) -> None:
        """Enter email address."""
        self.page.locator(self.INPUT_EMAIL).fill(email)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.page.locator(self.INPUT_PASSWORD).fill(password)

    def click_login(self) -> None:
        """Click login button."""
        self.page.locator(self.BTN_LOGIN).click()

    def login(self, email: str, password: str) -> None:
        """Perform complete login flow."""
        self.navigate_to_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # ============================================================
    # Verifications
    # ============================================================

    def is_logged_in(self) -> bool:
        """Verify user is logged in (redirected away from login page)."""
        try:
            self.page.wait_for_url("**/account", timeout=10000)
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get login error message text."""
        try:
            self.page.locator(self.ERROR_MESSAGE).wait_for(state="visible", timeout=5000)
            return self.page.locator(self.ERROR_MESSAGE).text_content() or ""
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed (waits up to 5s for it to appear)."""
        try:
            self.page.locator(self.ERROR_MESSAGE).wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def is_login_page(self) -> bool:
        """Verify we are on the login page."""
        return "/auth/login" in self.get_current_url()

    def click_register(self) -> None:
        """Click register link."""
        self.page.locator(self.LINK_REGISTER).click()

    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        self.page.locator(self.LINK_FORGOT_PASSWORD).click()
