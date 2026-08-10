"""Login Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for KAI Login page using XPath selectors."""

    # ============================================================
    # XPath Locators
    # ============================================================
    XPATH_USERNAME = '//input[@type="username"]'
    XPATH_PASSWORD = '//input[@type="password"]'
    XPATH_LOGIN_BUTTON = '//span[@class="btn-text"]'
    XPATH_ERROR_MESSAGE = '//div[contains(@class,"iziToast") and contains(@class,"iziToast-color-red")]'
    XPATH_PROFILE_ICON = '//span[@class="input-group-addon"]'
    XPATH_REGISTER_LINK = '//a[normalize-space()="Registrasi"]'
    XPATH_FORGOT_PASSWORD = '//a[normalize-space()="Lupa password"]'
    XPATH_CLOSE_MODAL = '//button[contains(@class,"close") or @aria-label="Close"]'



    def navigate_to_login(self):
        """Navigate to login page."""
        self.navigate()
        self.wait_for_load()

    def enter_username(self, username: str):
        """Enter username/email."""
        self.fill_xpath(self.XPATH_USERNAME, username)

    def enter_password(self, password: str):
        """Enter password."""
        self.fill_xpath(self.XPATH_PASSWORD, password)

    def click_login(self):
        """Click login button."""
        self.click_xpath(self.XPATH_LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Perform complete login flow."""
        self.navigate_to_login()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.page.wait_for_load_state("networkidle")

    def is_logged_in(self) -> bool:
        """Verify user is logged in by checking profile icon visibility."""
        try:
            self.page.locator(f"xpath={self.XPATH_PROFILE_ICON}").wait_for(
                state="visible", timeout=5000
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get login error message text."""
        try:
            self.page.locator(f"xpath={self.XPATH_ERROR_MESSAGE}").wait_for(
                state="visible", timeout=5000
            )
            return self.get_text_xpath(self.XPATH_ERROR_MESSAGE)
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_visible_xpath(self.XPATH_ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        """Verify we are on the login page."""
        return self.is_visible_xpath(self.XPATH_LOGIN_BUTTON)

    def click_register(self):
        """Click register link."""
        self.click_xpath(self.XPATH_REGISTER_LINK)

    def click_forgot_password(self):
        """Click forgot password link."""
        self.click_xpath(self.XPATH_FORGOT_PASSWORD)
