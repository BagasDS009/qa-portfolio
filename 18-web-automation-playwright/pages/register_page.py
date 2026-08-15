"""Register Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Page Object for user registration page."""

    # ============================================================
    # Selectors
    # ============================================================
    INPUT_FIRST_NAME = "[data-test='first-name']"
    INPUT_LAST_NAME = "[data-test='last-name']"
    INPUT_DOB = "[data-test='dob']"
    INPUT_ADDRESS = "[data-test='address']"
    INPUT_CITY = "[data-test='city']"
    INPUT_STATE = "[data-test='state']"
    SELECT_COUNTRY = "[data-test='country']"
    INPUT_POSTCODE = "[data-test='postcode']"
    INPUT_PHONE = "[data-test='phone']"
    INPUT_EMAIL = "[data-test='email']"
    INPUT_PASSWORD = "[data-test='password']"
    BTN_REGISTER = "[data-test='register-submit']"
    ERROR_MESSAGE = ".help-block"

    # ============================================================
    # Actions
    # ============================================================

    def navigate_to_register(self) -> None:
        """Navigate to registration page."""
        self.navigate("auth/register")

    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        dob: str,
        address: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        phone: str,
        email: str,
        password: str,
    ) -> None:
        """Fill all registration fields."""
        self.page.locator(self.INPUT_FIRST_NAME).fill(first_name)
        self.page.locator(self.INPUT_LAST_NAME).fill(last_name)
        self.page.locator(self.INPUT_DOB).fill(dob)
        self.page.locator(self.INPUT_ADDRESS).fill(address)
        self.page.locator(self.INPUT_CITY).fill(city)
        self.page.locator(self.INPUT_STATE).fill(state)
        self.page.locator(self.SELECT_COUNTRY).select_option(value=country)
        self.page.locator(self.INPUT_POSTCODE).fill(postcode)
        self.page.locator(self.INPUT_PHONE).fill(phone)
        self.page.locator(self.INPUT_EMAIL).fill(email)
        self.page.locator(self.INPUT_PASSWORD).fill(password)

    def click_register(self) -> None:
        """Click register button."""
        self.page.locator(self.BTN_REGISTER).click()

    def register(
        self,
        first_name: str,
        last_name: str,
        dob: str,
        address: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        phone: str,
        email: str,
        password: str,
    ) -> None:
        """Perform complete registration flow."""
        self.navigate_to_register()
        self.fill_registration_form(
            first_name, last_name, dob, address, city, state,
            country, postcode, phone, email, password,
        )
        self.click_register()

    # ============================================================
    # Verifications
    # ============================================================

    def is_registration_successful(self) -> bool:
        """Check if registration was successful (redirected to login)."""
        try:
            self.page.wait_for_url("**/auth/login", timeout=10000)
            return True
        except Exception:
            return False

    def get_validation_errors(self) -> list[str]:
        """Get all validation error messages."""
        errors = self.page.locator(self.ERROR_MESSAGE).all_text_contents()
        return [e.strip() for e in errors if e.strip()]
