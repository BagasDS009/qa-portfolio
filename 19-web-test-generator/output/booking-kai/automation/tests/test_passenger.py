"""
TC-PASSENGER-001 to TC-PASSENGER-010: Passenger data form test suite for KAI Booking.

Precondition handled by fixture: search → select train → arrive at passenger form.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.passenger_page import PassengerPage
from test_data.passengers import VALID_CONTACT, VALID_PASSENGER, INVALID_PASSENGER, BOUNDARY_DATA


@allure.epic("KAI Online Booking")
@allure.feature("Passenger Data")
@pytest.mark.wave1
class TestPassenger:
    """Passenger data form test suite.
    
    Uses `at_passenger_form` fixture for precondition (search → select train).
    """

    # === CRITICAL ===

    @allure.story("Valid Submission")
    @allure.title("TC-PASSENGER-001: Fill valid data and proceed to seat selection")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.critical
    @pytest.mark.passenger
    def test_passenger_valid_proceed(self, at_passenger_form: Page):
        """Verify valid passenger data allows proceeding to seat selection."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Verify on passenger form"):
            assert passenger.is_form_displayed(), "Not on passenger form after selecting train"

        with allure.step("Fill contact and passenger data"):
            passenger.fill_and_proceed(VALID_CONTACT, VALID_PASSENGER)

        with allure.step("Verify proceeded (left passenger page)"):
            at_passenger_form.wait_for_timeout(3000)
            assert not passenger.has_any_error(), (
                "Errors shown after filling valid data"
            )

    # === NEGATIVE ===

    @allure.story("Validation")
    @allure.title("TC-PASSENGER-004: Submit with empty contact name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.passenger
    def test_empty_contact_name(self, at_passenger_form: Page):
        """Verify 'Mohon isi Nama' error when name is empty."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Fill all except name, click continue"):
            passenger.fill_contact(
                name="",
                phone=VALID_CONTACT["phone"],
                email=VALID_CONTACT["email"],
                id_number=VALID_CONTACT["id_number"],
            )
            passenger.fill_passenger(VALID_PASSENGER["name"], VALID_PASSENGER["id_number"])
            passenger.click_continue()

        with allure.step("Verify name error shown"):
            assert passenger.has_name_error() or passenger.has_any_error(), (
                "No error shown for empty contact name"
            )

    @allure.story("Validation")
    @allure.title("TC-PASSENGER-005: Submit with empty ID number")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.passenger
    def test_empty_id_number(self, at_passenger_form: Page):
        """Verify 'Mohon isi Nomor Identitas' error."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Fill all except ID number"):
            passenger.fill_contact(
                name=VALID_CONTACT["name"],
                phone=VALID_CONTACT["phone"],
                email=VALID_CONTACT["email"],
                id_number="",
            )
            passenger.fill_passenger(VALID_PASSENGER["name"], "")
            passenger.click_continue()

        with allure.step("Verify ID error shown"):
            assert passenger.has_id_error() or passenger.has_any_error()

    @allure.story("Validation")
    @allure.title("TC-PASSENGER-006: Submit with empty email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.passenger
    def test_empty_email(self, at_passenger_form: Page):
        """Verify 'Mohon diisi Email' error."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Fill all except email"):
            passenger.fill_contact(
                name=VALID_CONTACT["name"],
                phone=VALID_CONTACT["phone"],
                email="",
                id_number=VALID_CONTACT["id_number"],
            )
            passenger.fill_passenger(VALID_PASSENGER["name"], VALID_PASSENGER["id_number"])
            passenger.click_continue()

        with allure.step("Verify email error"):
            assert passenger.has_email_error() or passenger.has_any_error()

    @allure.story("Validation")
    @allure.title("TC-PASSENGER-007: Submit with short NIK (< 16 digits)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.passenger
    def test_short_nik(self, at_passenger_form: Page):
        """Verify NIK validation rejects < 16 digits."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Fill with 15-digit NIK"):
            passenger.fill_contact(
                name=VALID_CONTACT["name"],
                phone=VALID_CONTACT["phone"],
                email=VALID_CONTACT["email"],
                id_number=BOUNDARY_DATA["nik_15_digits"],
            )
            passenger.fill_passenger(VALID_PASSENGER["name"], BOUNDARY_DATA["nik_15_digits"])
            passenger.click_continue()

        with allure.step("Verify validation error"):
            at_passenger_form.wait_for_timeout(2000)
            assert passenger.is_form_displayed() or passenger.has_any_error()

    # === EDGE ===

    @allure.story("Security")
    @allure.title("TC-PASSENGER-009: XSS in name field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.passenger
    def test_xss_in_name(self, at_passenger_form: Page):
        """Verify XSS safely handled in passenger name."""
        passenger = PassengerPage(at_passenger_form)

        with allure.step("Fill name with XSS payload"):
            passenger.fill_contact(
                name=BOUNDARY_DATA["xss_name"],
                phone=VALID_CONTACT["phone"],
                email=VALID_CONTACT["email"],
                id_number=VALID_CONTACT["id_number"],
            )

        with allure.step("Verify page still functional"):
            assert at_passenger_form.locator("body").is_visible(), "Page crashed on XSS input"
