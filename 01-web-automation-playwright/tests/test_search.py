"""
TC-003: Search Train
Test cases for train search functionality on KAI Booking.
"""

import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from tests.test_data import VALID_SEARCH, VALID_SEARCH_ALT, INVALID_SEARCH, get_departure_date


class TestSearchTrain:
    """Test suite for train search functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page, login):
        """Setup: Login and initialize page objects."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.home_page.navigate_to_home()

    @pytest.mark.smoke
    def test_search_train_valid_route(self, page):
        """
        TC-003: Search Train - Valid Route (PSE → BD)
        Verify user can search trains between valid stations.
        """
        self.home_page.search_train(
            origin=VALID_SEARCH["origin"],             # PSE
            destination=VALID_SEARCH["destination"],   # BD
            date=get_departure_date(7),
            adults=VALID_SEARCH["adults"],
        )

        self.train_list_page.wait_for_results()
        assert self.train_list_page.is_train_list_displayed(), (
            "Train search results not displayed"
        )
        assert self.train_list_page.get_available_trains_count() > 0, (
            "No trains found for PSE → BD route"
        )

    def test_search_train_alternative_route(self, page):
        """
        TC-003b: Search Train - Alternative Route (GMR → YK)
        """
        self.home_page.search_train(
            origin=VALID_SEARCH_ALT["origin"],             # GMR
            destination=VALID_SEARCH_ALT["destination"],   # YK
            date=get_departure_date(10),
            adults=VALID_SEARCH_ALT["adults"],
        )

        self.train_list_page.wait_for_results()
        assert self.train_list_page.is_train_list_displayed(), (
            "Train search results not displayed for GMR → YK"
        )

    def test_search_train_swap_stations(self, page):
        """
        TC-003c: Search Train - Swap Stations
        Verify swap button exchanges origin and destination.
        """
        self.home_page.select_origin_station(VALID_SEARCH["origin"])       # PSE
        self.home_page.select_destination_station(VALID_SEARCH["destination"])  # BD

        self.home_page.swap_stations()

        current_origin = self.home_page.get_origin_value()
        current_destination = self.home_page.get_destination_value()

        assert VALID_SEARCH["destination"] in current_origin, (
            "Swap did not change origin station"
        )
        assert VALID_SEARCH["origin"] in current_destination, (
            "Swap did not change destination station"
        )

    def test_search_train_no_results(self, page):
        """
        TC-003d: Search Train - No Available Route
        Verify appropriate message for invalid route.
        """
        self.home_page.search_train(
            origin=INVALID_SEARCH["origin"],
            destination=INVALID_SEARCH["destination"],
            date=INVALID_SEARCH["departure_date"],
            adults=INVALID_SEARCH["adults"],
        )

        self.train_list_page.wait_for_results()
        is_empty = (
            self.train_list_page.is_no_result()
            or self.train_list_page.get_available_trains_count() == 0
        )
        assert is_empty, "Expected no results for invalid route"

    def test_search_form_visible_after_login(self, page):
        """
        TC-003e: Search Form Visibility
        Verify search form is displayed after login.
        """
        assert self.home_page.is_search_form_displayed(), (
            "Search form not visible on home page"
        )
