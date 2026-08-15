"""Contact Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Page Object for contact form page."""

    # ============================================================
    # Selectors
    # ============================================================
    INPUT_FIRST_NAME = "[data-test='first-name']"
    INPUT_LAST_NAME = "[data-test='last-name']"
    INPUT_EMAIL = "[data-test='email']"
    SELECT_SUBJECT = "[data-test='subject']"
    INPUT_MESSAGE = "[data-test='message']"
    INPUT_ATTACHMENT = "[data-test='attachment']"
    BTN_SUBMIT = "[data-test='contact-submit']"
    SUCCESS_MESSAGE = ".alert-success"
    ERROR_MESSAGE = ".alert.alert-danger"

    # ============================================================
    # Actions
    # ============================================================

    def navigate_to_contact(self) -> None:
        """Navigate to contact page."""
        self.navigate("contact")

    def fill_contact_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        subject: str,
        message: str,
    ) -> None:
        """Fill all contact form fields."""
        self.page.locator(self.INPUT_FIRST_NAME).fill(first_name)
        self.page.locator(self.INPUT_LAST_NAME).fill(last_name)
        self.page.locator(self.INPUT_EMAIL).fill(email)
        self.page.locator(self.SELECT_SUBJECT).select_option(label=subject)
        self.page.locator(self.INPUT_MESSAGE).fill(message)

    def submit_form(self) -> None:
        """Click submit button."""
        self.page.locator(self.BTN_SUBMIT).click()

    def submit_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        subject: str,
        message: str,
    ) -> None:
        """Fill and submit contact form in one call."""
        self.navigate_to_contact()
        self.fill_contact_form(first_name, last_name, email, subject, message)
        self.submit_form()

    # ============================================================
    # Verifications
    # ============================================================

    def is_submission_successful(self) -> bool:
        """Check if form was submitted successfully."""
        try:
            self.page.locator(self.SUCCESS_MESSAGE).wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False

    def get_success_message(self) -> str:
        """Get success message text."""
        return self.page.locator(self.SUCCESS_MESSAGE).text_content() or ""

    def get_validation_errors(self) -> list[str]:
        """Get all validation error messages."""
        errors = self.page.locator(self.ERROR_MESSAGE).all_text_contents()
        return [e.strip() for e in errors if e.strip()]

    def has_validation_errors(self) -> bool:
        """Check if any validation errors are displayed."""
        self.page.wait_for_timeout(1000)
        return self.page.locator(self.ERROR_MESSAGE).count() > 0
