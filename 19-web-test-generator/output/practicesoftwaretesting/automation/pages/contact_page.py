"""Contact Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Page Object for /contact."""

    # Selectors
    INPUT_FIRST_NAME = "[data-test='first-name']"
    INPUT_LAST_NAME = "[data-test='last-name']"
    INPUT_EMAIL = "[data-test='email']"
    SELECT_SUBJECT = "[data-test='subject']"
    INPUT_MESSAGE = "[data-test='message']"
    BTN_SUBMIT = "[data-test='contact-submit']"
    SUCCESS_MESSAGE = ".alert-success"
    ERROR_MESSAGE = ".alert.alert-danger"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def navigate_to_contact(self) -> None:
        """Navigate to contact page."""
        self.navigate("contact")

    def fill_form(self, first_name: str, last_name: str, email: str, subject: str, message: str) -> None:
        """Fill contact form fields."""
        self.page.locator(self.INPUT_FIRST_NAME).fill(first_name)
        self.page.locator(self.INPUT_LAST_NAME).fill(last_name)
        self.page.locator(self.INPUT_EMAIL).fill(email)
        self.page.locator(self.SELECT_SUBJECT).select_option(label=subject)
        self.page.locator(self.INPUT_MESSAGE).fill(message)

    def submit(self) -> None:
        """Click submit button."""
        self.page.locator(self.BTN_SUBMIT).click()

    def submit_contact(self, first_name: str, last_name: str, email: str, subject: str, message: str) -> None:
        """Fill and submit in one call."""
        self.navigate_to_contact()
        self.fill_form(first_name, last_name, email, subject, message)
        self.submit()

    # Verifications

    def is_success(self) -> bool:
        """Check if success message is shown."""
        try:
            self.page.locator(self.SUCCESS_MESSAGE).wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def get_success_message(self) -> str:
        """Get success message text."""
        return self.page.locator(self.SUCCESS_MESSAGE).text_content() or ""

    def has_errors(self) -> bool:
        """Check if validation errors are visible."""
        self.page.wait_for_timeout(1000)
        return self.page.locator(self.ERROR_MESSAGE).count() > 0
