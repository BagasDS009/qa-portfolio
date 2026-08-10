"""
TC-007: Required Field Validation
Test cases for form validation on KAI Booking.
"""

import allure
import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from tests.test_data import (
    VALID_SEARCH,
    PARTIAL_CONTACT_NO_NAME,
    PASSENGER_NO_ID,
    CONTACT_PERSON,
)


@allure.epic("KAI Booking")
@allure.feature("Form Validation")
class TestValidation:
    """Test suite for required field and form validation."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Navigate to home page (no login needed)."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.passenger_page = PassengerPage(page)

    def _navigate_to_passenger_form(self):
        """Helper: Search and navigate to passenger form."""
        self.home_page.navigate_to_home()
        self.home_page.search_train(
            origin=VALID_SEARCH["origin"],
            destination=VALID_SEARCH["destination"],
            tgl=VALID_SEARCH["tgl"],
            adults=VALID_SEARCH["adults"],
        )
        self.train_list_page.wait_for_results()
        self.train_list_page.select_first_train()

    @allure.story("Required Fields")
    @allure.title("TC-007: Submit empty passenger form")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_passenger_form_required_fields(self, page):
        """Verify validation messages when all fields are empty."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Verify form is displayed"):
            assert self.passenger_page.is_passenger_form_displayed()

        with allure.step("Submit empty form"):
            self.passenger_page.submit_empty_form()

        with allure.step("Verify validation errors are shown"):
            assert self.passenger_page.is_validation_error_displayed(), (
                "No validation errors shown for empty required fields"
            )

    @allure.story("Required Fields")
    @allure.title("TC-007b: Contact name is mandatory")
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_name_required(self, page):
        """Verify contact name field is mandatory."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Fill form without contact name"):
            self.passenger_page.fill_contact_person(
                name=PARTIAL_CONTACT_NO_NAME["name"],
                phone=PARTIAL_CONTACT_NO_NAME["phone"],
                email=PARTIAL_CONTACT_NO_NAME["email"],
            )
            self.passenger_page.click_continue()

        with allure.step("Verify validation error"):
            assert self.passenger_page.is_validation_error_displayed(), (
                "Validation error not shown when contact name is empty"
            )

    @allure.story("Required Fields")
    @allure.title("TC-007c: ID number is mandatory")
    @allure.severity(allure.severity_level.NORMAL)
    def test_id_number_required(self, page):
        """Verify passenger ID number field is mandatory."""
        with allure.step("Navigate to passenger form"):
            self._navigate_to_passenger_form()

        with allure.step("Fill form without ID number"):
            self.passenger_page.fill_contact_person(
                name=CONTACT_PERSON["name"],
                phone=CONTACT_PERSON["phone"],
                email=CONTACT_PERSON["email"],
            )
            self.passenger_page.fill_passenger_info(
                name=PASSENGER_NO_ID["name"],
                id_number=PASSENGER_NO_ID["id_number"],
            )
            self.passenger_page.click_continue()

        with allure.step("Verify validation error"):
            assert self.passenger_page.is_validation_error_displayed(), (
                "Validation error not shown when ID number is empty"
            )

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
