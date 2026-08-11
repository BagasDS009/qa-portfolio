"""
TC-007: Required Field Validation
Test cases for form validation on KAI Booking.
Validation triggers on blur (click field → leave empty → click another field).
"""

import allure
import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from tests.test_data import VALID_SEARCH


@allure.epic("KAI Booking")
@allure.feature("Form Validation")
class TestValidation:
    """Test suite for required field and form validation."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize page objects."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.passenger_page = PassengerPage(page)

    def _navigate_to_passenger_form(self):
        """Helper: Search, select first train, go to passenger form."""
        self.home_page.navigate_to_home()
        self.home_page.search_train(
            origin=VALID_SEARCH["origin"],
            destination=VALID_SEARCH["destination"],
            tgl=VALID_SEARCH["tgl"],
            adults=VALID_SEARCH["adults"],
        )
        self.train_list_page.wait_for_results()
        self.train_list_page.select_first_train()

    # ==================================================================
    # TC-007: Button disabled
    # ==================================================================

    @allure.story("Submit Button")
    @allure.title("TC-007: Submit button disabled when form is empty")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_submit_button_disabled(self, page):
        """Verify submit button is disabled when required fields are empty."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Verify form is displayed"):
            assert self.passenger_page.is_passenger_form_displayed()

        with allure.step("Verify submit button is disabled"):
            assert self.passenger_page.is_submit_button_disabled(), (
                "Submit button should be disabled when form is empty"
            )

    # ==================================================================
    # TC-007b: Contact Name - Mohon isi Nama
    # Flow: Click nama → leave empty → click field lain → error muncul
    # ==================================================================

    @allure.story("Contact Person Validation")
    @allure.title("TC-007b: Validation - Mohon isi Nama")
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_name_required(self, page):
        """Verify 'Mohon isi Nama' error on blur when name is empty."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Click name field → leave empty → click phone field"):
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_NAME)
            self.passenger_page.human_delay(500, 800)
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_PHONE)
            self.passenger_page.human_delay(500, 800)

        with allure.step("Verify 'Mohon isi Nama' error is displayed"):
            assert self.passenger_page.is_validation_error_displayed_name_error(), (
                "Validation error 'Mohon isi Nama' not shown"
            )

    # ==================================================================
    # TC-007c: Contact ID Number - Mohon isi Nomor Identitas
    # Flow: Click no. identitas → leave empty → click field lain → error
    # ==================================================================

    @allure.story("Contact Person Validation")
    @allure.title("TC-007c: Validation - Mohon isi Nomor Identitas")
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_id_number_required(self, page):
        """Verify 'Mohon isi Nomor Identitas' error on blur when ID is empty."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Click ID number field → leave empty → click name field"):
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_ID_NUMBER)
            self.passenger_page.human_delay(500, 800)
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_NAME)
            self.passenger_page.human_delay(500, 800)

        with allure.step("Verify 'Mohon isi Nomor Identitas' error is displayed"):
            assert self.passenger_page.is_validation_error_displayed_no_id(), (
                "Validation error 'Mohon isi Nomor Identitas' not shown"
            )

    # ==================================================================
    # TC-007d: Search without origin
    # ==================================================================

    @allure.story("Search Validation")
    @allure.title("TC-007d: Search without filling origin station")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_without_origin_station(self, page):
        """Verify search cannot proceed without origin station."""
        with allure.step("Navigate to home page"):
            self.home_page.navigate_to_home()

        with allure.step("Click search without filling any field"):
            self.home_page.click_search()

        with allure.step("Verify no results displayed"):
            assert not self.train_list_page.is_train_list_displayed(), (
                "Search should not proceed without required fields"
            )

    # ==================================================================
    # TC-007e: Email - Mohon diisi Email
    # Flow: Click email → leave empty → click field lain → error
    # ==================================================================

    @allure.story("Contact Person Validation")
    @allure.title("TC-007e: Validation - Mohon diisi Email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_email_required(self, page):
        """Verify 'Mohon diisi Email' error on blur when email is empty."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Click email field → leave empty → click name field"):
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_EMAIL)
            self.passenger_page.human_delay(500, 800)
            self.passenger_page.click_xpath(self.passenger_page.XPATH_CONTACT_NAME)
            self.passenger_page.human_delay(500, 800)

        with allure.step("Verify 'Mohon diisi Email' error is displayed"):
            assert self.passenger_page.is_validation_error_displayed_email(), (
                "Validation error 'Mohon diisi Email' not shown"
            )

    # ==================================================================
    # TC-007f: Passenger ID - Nomor Identitas Wajib Diisi
    # Flow: Click no. identitas penumpang → leave empty → click field lain
    # ==================================================================

    @allure.story("Passenger Validation")
    @allure.title("TC-007f: Validation - Nomor Identitas Wajib Diisi (Passenger)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_passenger_id_number_required(self, page):
        """Verify 'Nomor Identitas Wajib Diisi' error on blur."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Click passenger ID field → leave empty → click name field"):
            self.passenger_page.click_xpath(self.passenger_page.XPATH_PASSENGER_ID_NUMBER)
            self.passenger_page.human_delay(500, 800)
            self.passenger_page.click_xpath(self.passenger_page.XPATH_PASSENGER_NAME)
            self.passenger_page.human_delay(500, 800)

        with allure.step("Verify 'Nomor Identitas Wajib Diisi' error is displayed"):
            assert self.passenger_page.is_validation_passenger_no_id_error(), (
                "Validation error 'Nomor Identitas Wajib Diisi' not shown"
            )

    # ==================================================================
    # TC-007g: Passenger Name - Fill out this field
    # Flow: Click nama penumpang → leave empty → click field lain
    # ==================================================================

    @allure.story("Passenger Validation")
    @allure.title("TC-007g: Validation - Passenger name field is required")
    @allure.severity(allure.severity_level.NORMAL)
    def test_passenger_name_required(self, page):
        """Verify passenger name field has required attribute and form cannot submit without it."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Verify passenger name field is required (has required attribute)"):
            locator = page.locator(f"xpath={self.passenger_page.XPATH_PASSENGER_NAME}")
            is_required = locator.get_attribute("required") is not None
            assert is_required, (
                "Passenger name field should have 'required' attribute"
            )
