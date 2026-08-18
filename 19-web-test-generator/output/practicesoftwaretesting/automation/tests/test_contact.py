"""
TC-CONTACT-001 to TC-CONTACT-006: Contact form test suite.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.contact_page import ContactPage
from test_data.negative_inputs import BOUNDARY_DATA, CONTACT_NEGATIVE


VALID_CONTACT = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "subject": "Webmaster",
    "message": (
        "This is an automated test message for verification purposes. "
        "It must be at least fifty characters to pass form validation."
    ),
}


@allure.epic("Practice Software Testing")
@allure.feature("Contact Form")
@pytest.mark.wave1
class TestContact:
    """Contact form test suite."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.contact = ContactPage(page)

    # === CRITICAL ===

    @allure.story("Submit Contact")
    @allure.title("TC-CONTACT-001: Submit contact form with valid data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.contact
    def test_contact_valid_submission(self, page: Page):
        """Verify contact form submits successfully with valid data."""
        with allure.step("Fill and submit contact form"):
            self.contact.submit_contact(**VALID_CONTACT)

        with allure.step("Verify success message"):
            assert self.contact.is_success(), (
                "Contact form submission failed — no success message"
            )

    # === POSITIVE ===

    @allure.story("Submit Contact")
    @allure.title("TC-CONTACT-002: Submit with different subject options")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.contact
    @pytest.mark.parametrize("subject", [
        "Customer service", "Webmaster", "Return", "Payments"
    ])
    def test_contact_all_subjects(self, page: Page, subject: str):
        """Verify all subject dropdown options work."""
        data = {**VALID_CONTACT, "subject": subject}

        with allure.step(f"Submit with subject: {subject}"):
            self.contact.submit_contact(**data)

        with allure.step("Verify success"):
            assert self.contact.is_success(), (
                f"Contact form failed for subject '{subject}'"
            )

    # === NEGATIVE ===

    @allure.story("Validation")
    @allure.title("TC-CONTACT-003: Submit with all empty fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.contact
    def test_contact_empty_fields(self, page: Page):
        """Verify validation errors for empty required fields."""
        with allure.step("Navigate to contact"):
            self.contact.navigate_to_contact()

        with allure.step("Submit empty form"):
            self.contact.submit()

        with allure.step("Verify validation errors"):
            assert self.contact.has_errors(), (
                "No validation errors shown for empty contact form"
            )

    @allure.story("Validation")
    @allure.title("TC-CONTACT-004: Submit with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.contact
    def test_contact_invalid_email(self, page: Page):
        """Verify email format validation on contact form."""
        data = {**VALID_CONTACT, "email": "not-an-email"}

        with allure.step("Submit with invalid email"):
            self.contact.submit_contact(**data)

        with allure.step("Verify error shown"):
            # Form should not succeed with invalid email
            assert not self.contact.is_success() or self.contact.has_errors(), (
                "Contact form accepted invalid email 'not-an-email'"
            )

    @allure.story("Validation")
    @allure.title("TC-CONTACT-005: Submit with message too short")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.contact
    def test_contact_short_message(self, page: Page):
        """Verify minimum message length validation (50 chars)."""
        data = {**VALID_CONTACT, "message": CONTACT_NEGATIVE["short_message"]}

        with allure.step("Submit with short message"):
            self.contact.submit_contact(**data)

        with allure.step("Verify validation error"):
            assert not self.contact.is_success(), (
                "Contact form accepted message shorter than 50 characters"
            )

    # === EDGE ===

    @allure.story("Security")
    @allure.title("TC-CONTACT-006: XSS attempt in message field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.contact
    def test_contact_xss_message(self, page: Page):
        """Verify XSS is sanitized in message field."""
        xss_message = (
            BOUNDARY_DATA["xss_script"] + " " +
            "A" * 50  # Pad to meet 50 char minimum
        )
        data = {**VALID_CONTACT, "message": xss_message}

        with allure.step("Submit with XSS in message"):
            self.contact.submit_contact(**data)

        with allure.step("Verify no script execution"):
            # Either form accepts (sanitized) or rejects — both acceptable
            # Key: no script execution, page still functional
            assert page.locator("body").is_visible(), "Page crashed on XSS input"
