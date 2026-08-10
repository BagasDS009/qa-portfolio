"""
TC-007: Required Field Validation
Test cases for form validation on KAI Booking.
"""

import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from tests.test_data import (
    VALID_SEARCH,
    PARTIAL_CONTACT_NO_NAME,
    PASSENGER_NO_ID,
    CONTACT_PERSON,
    get_departure_date,
)


class TestValidation:
    """Test suite for required field and form validation."""

    @pytest.fixture(autouse=True)
    def setup(self, page, login):
        """Setup: Login and initialize page objects."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.passenger_page = PassengerPage(page)

    def _navigate_to_passenger_form(self):
        """Helper: Search train and navigate to passenger form."""
        self.home_page.navigate_to_home()
        self.home_page.search_train(
            origin=VALID_SEARCH["origin"],             # PSE
            destination=VALID_SEARCH["destination"],   # BD
            date=get_departure_date(7),
            adults=VALID_SEARCH["adults"],
        )
        self.train_list_page.wait_for_results()
        self.train_list_page.select_first_train()

    @pytest.mark.smoke
    def test_passenger_form_required_fields(self, page):
        """
        TC-007: Required Field Validation - Empty Passenger Form
        Verify validation messages when all fields are empty.
        """
        self._navigate_to_passenger_form()

        assert self.passenger_page.is_passenger_form_displayed(), (
            "Passenger form not displayed"
        )
        self.passenger_page.submit_empty_form()

        assert self.passenger_page.is_validation_error_displayed(), (
            "No validation errors shown for empty required fields"
        )

    def test_contact_name_required(self, page):
        """
        TC-007b: Contact Name Required
        Verify contact name field is mandatory.
        """
        self._navigate_to_passenger_form()

        self.passenger_page.fill_contact_person(
            name=PARTIAL_CONTACT_NO_NAME["name"],      # Empty
            phone=PARTIAL_CONTACT_NO_NAME["phone"],
            email=PARTIAL_CONTACT_NO_NAME["email"],
        )
        self.passenger_page.click_continue()

        assert self.passenger_page.is_validation_error_displayed(), (
            "Validation error not shown when contact name is empty"
        )

    def test_id_number_required(self, page):
        """
        TC-007c: ID Number Required
        Verify passenger ID number field is mandatory.
        """
        self._navigate_to_passenger_form()

        self.passenger_page.fill_contact_person(
            name=CONTACT_PERSON["name"],
            phone=CONTACT_PERSON["phone"],
            email=CONTACT_PERSON["email"],
        )
        self.passenger_page.fill_passenger_info(
            name=PASSENGER_NO_ID["name"],
            id_number=PASSENGER_NO_ID["id_number"],    # Empty
        )
        self.passenger_page.click_continue()

        assert self.passenger_page.is_validation_error_displayed(), (
            "Validation error not shown when ID number is empty"
        )

    def test_search_without_origin_station(self, page):
        """
        TC-007d: Search Validation - Missing Origin
        Verify search cannot proceed without origin station.
        """
        self.home_page.navigate_to_home()
        self.home_page.click_search()

        assert not self.train_list_page.is_train_list_displayed(), (
            "Search should not proceed without required fields"
        )
