"""Login Page Object for KAI Booking."""

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for KAI login — may appear as modal or page."""

    XPATH_USERNAME = '//input[@name="username"]'
    XPATH_PASSWORD = '//input[@type="password"]'
    XPATH_LOGIN_BTN = '//button[@id="btnLogin"]'
    XPATH_CAPTCHA = '//input[@name="captcha"]'
    XPATH_ERROR_TOAST = '//div[contains(@class,"iziToast") and contains(@class,"iziToast-color-red")]|//div[contains(@class,"alert-danger")]'
    XPATH_PROFILE_ICON = '//span[@class="input-group-addon"]'
    XPATH_REGISTER_LINK = '//a[normalize-space()="Registrasi"]'

    # Actions

    def navigate_to_login(self) -> None:
        """Navigate to login page (separate page at /auth/login)."""
        self.navigate("auth/login")
        self.page.locator(f"xpath={self.XPATH_USERNAME}").wait_for(state="visible", timeout=15000)

    def login(self, username: str, password: str, captcha: str = "") -> None:
        """Complete login flow.
        
        Note: Site has CAPTCHA field. In automation:
        - If captcha param provided → fill it
        - If empty → try submitting without (may fail with captcha error)
        - For real testing: may need to bypass or mock CAPTCHA
        """
        self.navigate_to_login()
        self.fill_xpath(self.XPATH_USERNAME, username)
        self.fill_xpath(self.XPATH_PASSWORD, password)
        if captcha:
            self.fill_xpath(self.XPATH_CAPTCHA, captcha)
        self.click_xpath(self.XPATH_LOGIN_BTN)
        self.page.wait_for_load_state("load")
        self.human_delay(2000, 3000)

    def click_login_button(self) -> None:
        """Click login without filling fields."""
        self.click_xpath(self.XPATH_LOGIN_BTN)

    # Verifications

    def is_logged_in(self) -> bool:
        """Check if profile icon is visible (logged in state)."""
        try:
            self.page.locator(f"xpath={self.XPATH_PROFILE_ICON}").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def is_error_displayed(self) -> bool:
        """Check if red error toast (iziToast) is visible."""
        try:
            self.page.locator(f"xpath={self.XPATH_ERROR_TOAST}").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get error toast text."""
        return self.get_text_xpath(self.XPATH_ERROR_TOAST)

    def is_login_form_visible(self) -> bool:
        """Check if login form is shown."""
        return self.is_visible_xpath(self.XPATH_USERNAME)
