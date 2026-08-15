"""
TC-006: Contact form
Test cases for contact form submission and validation.
"""

import allure
import pytest

from pages.contact_page import ContactPage
from tests.test_data import VALID_CONTACT, INVALID_CONTACT


@allure.epic("Toolshop E-Commerce")
@allure.feature("Contact Form")
class TestContact:
    """Test suite for contact form functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize contact page."""
        self.contact_page = ContactPage(page)

    @allure.story("Submit Contact Form")
    @allure.title("TC-006a: Submit contact form with valid data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.contact
    def test_submit_valid_contact(self, page):
        """Verify contact form can be submitted with valid data."""
        with allure.step("Navigate to contact page"):
            self.contact_page.navigate_to_contact()

        with allure.step("Fill contact form with valid data"):
            self.contact_page.fill_contact_form(
                first_name=VALID_CONTACT["first_name"],
                last_name=VALID_CONTACT["last_name"],
                email=VALID_CONTACT["email"],
                subject=VALID_CONTACT["subject"],
                message=VALID_CONTACT["message"],
            )

        with allure.step("Submit the form"):
            self.contact_page.submit_form()

        with allure.step("Verify submission success"):
            assert self.contact_page.is_submission_successful(), (
                "Contact form submission failed — no success message shown"
            )

    @allure.story("Contact Validation")
    @allure.title("TC-006b: Submit contact form with empty fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.contact
    def test_submit_empty_contact_form(self, page):
        """Verify validation errors when submitting empty contact form."""
        with allure.step("Navigate to contact page"):
            self.contact_page.navigate_to_contact()

        with allure.step("Submit form without filling any fields"):
            self.contact_page.submit_form()

        with allure.step("Verify validation errors are shown"):
            assert self.contact_page.has_validation_errors(), (
                "No validation errors shown for empty contact form"
            )

    @allure.story("Contact Validation")
    @allure.title("TC-006c: Submit contact form with invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.contact
    def test_submit_invalid_email_contact(self, page):
        """Verify validation error for invalid email format."""
        data = INVALID_CONTACT["invalid_email"]

        with allure.step("Navigate to contact page"):
            self.contact_page.navigate_to_contact()

        with allure.step("Fill form with invalid email"):
            self.contact_page.fill_contact_form(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                subject=data["subject"],
                message=data["message"],
            )

        with allure.step("Submit the form"):
            self.contact_page.submit_form()

        with allure.step("Verify validation error for email"):
            assert self.contact_page.has_validation_errors(), (
                "No validation error shown for invalid email format"
            )
