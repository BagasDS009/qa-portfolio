"""Register Page Object for Practice Software Testing (Toolshop).

Actual form fields (inspected from site Sprint 5):
  first-name, last-name, dob, country, postal_code, house_number,
  street, city, state, phone, email, password
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Page Object for /auth/register."""

    # Selectors (actual data-test attributes from the site)
    INPUT_FIRST_NAME = "[data-test='first-name']"
    INPUT_LAST_NAME = "[data-test='last-name']"
    INPUT_DOB = "[data-test='dob']"
    SELECT_COUNTRY = "[data-test='country']"
    INPUT_POSTCODE = "[data-test='postal_code']"
    INPUT_HOUSE_NUMBER = "[data-test='house_number']"
    INPUT_STREET = "[data-test='street']"
    INPUT_CITY = "[data-test='city']"
    INPUT_STATE = "[data-test='state']"
    INPUT_PHONE = "[data-test='phone']"
    INPUT_EMAIL = "[data-test='email']"
    INPUT_PASSWORD = "[data-test='password']"
    BTN_REGISTER = "[data-test='register-submit']"
    ERROR_MESSAGE = ".help-block, .alert-danger, .alert"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def navigate_to_register(self) -> None:
        """Navigate to registration page and wait for form to load."""
        self.navigate("auth/register")
        self.page.locator(self.INPUT_FIRST_NAME).wait_for(state="visible", timeout=15000)

    def fill_form(
        self,
        first_name: str,
        last_name: str,
        dob: str,
        street: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        phone: str,
        email: str,
        password: str,
        house_number: str = "42",
    ) -> None:
        """Fill all registration fields in the order they appear on the form."""
        self.page.locator(self.INPUT_FIRST_NAME).fill(first_name)
        self.page.locator(self.INPUT_LAST_NAME).fill(last_name)
        self.page.locator(self.INPUT_DOB).fill(dob)
        self.page.locator(self.SELECT_COUNTRY).select_option(value=country)
        self.page.locator(self.INPUT_POSTCODE).fill(postcode)
        self.page.locator(self.INPUT_HOUSE_NUMBER).fill(house_number)
        self.page.locator(self.INPUT_STREET).fill(street)
        self.page.locator(self.INPUT_CITY).fill(city)
        self.page.locator(self.INPUT_STATE).fill(state)
        self.page.locator(self.INPUT_PHONE).fill(phone)
        self.page.locator(self.INPUT_EMAIL).scroll_into_view_if_needed()
        self.page.locator(self.INPUT_EMAIL).fill(email)
        self.page.locator(self.INPUT_PASSWORD).fill(password)

    def submit(self) -> None:
        """Click register button."""
        self.page.locator(self.BTN_REGISTER).click()

    def register(self, **kwargs) -> None:
        """Complete registration: navigate + fill + submit."""
        self.navigate_to_register()
        self.fill_form(**kwargs)
        self.submit()

    # Verifications

    def is_registration_successful(self) -> bool:
        """Check redirect to login after success."""
        try:
            self.page.wait_for_url("**/auth/login", timeout=10000)
            return True
        except Exception:
            return False

    def get_validation_errors(self) -> list[str]:
        """Get all inline validation error messages."""
        errors = self.page.locator(self.ERROR_MESSAGE).all_text_contents()
        return [e.strip() for e in errors if e.strip()]

    def has_errors(self) -> bool:
        """Check if any validation errors are displayed."""
        # Wait for potential API response (duplicate email check takes time)
        self.page.wait_for_timeout(3000)
        return self.page.locator(self.ERROR_MESSAGE).count() > 0
