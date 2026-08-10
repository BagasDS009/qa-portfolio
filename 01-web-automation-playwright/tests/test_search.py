"""
TC-003: Search Train
Test cases for train search functionality on KAI Booking.
"""

import allure
import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from tests.test_data import VALID_SEARCH, VALID_SEARCH_ALT, VALID_SEARCH_NOT_FOUND, get_departure_date


@allure.epic("KAI Booking")
@allure.feature("Search Train")
class TestSearchTrain:
    """Test suite for train search functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Navigate to home page (no login needed)."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.home_page.navigate_to_home()

    @allure.story("Valid Search")
    @allure.title("TC-003: Search train with valid route (PSE → BD)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_train_valid_route(self, page):
        """Verify user can search trains between valid stations."""
        with allure.step("Fill search form: PSE → BD"):
            self.home_page.search_train(
                origin=VALID_SEARCH["origin"],
                destination=VALID_SEARCH["destination"],
                tgl=VALID_SEARCH["tgl"],
                adults=VALID_SEARCH["adults"],
            )

        with allure.step("Wait for search results"):
            self.train_list_page.wait_for_results()

        with allure.step("Verify train list is displayed"):
            assert self.train_list_page.is_train_list_displayed(), (
                "Train search results not displayed"
            )

        with allure.step("Verify trains are available"):
            assert self.train_list_page.get_available_trains_count() > 0, (
                "No trains found for PSE → BD route"
            )

    @allure.story("Valid Search")
    @allure.title("TC-003b: Search train alternative route (GMR → YK)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_train_alternative_route(self, page):
        """Verify search works for alternative route."""
        with allure.step("Fill search form: GMR → YK"):
            self.home_page.search_train(
                origin=VALID_SEARCH_ALT["origin"],
                destination=VALID_SEARCH_ALT["destination"],
                tgl=VALID_SEARCH_ALT["tgl"],
                adults=VALID_SEARCH_ALT["adults"],
            )

        with allure.step("Wait for search results"):
            self.train_list_page.wait_for_results()

        with allure.step("Verify train list is displayed"):
            assert self.train_list_page.is_train_list_displayed(), (
                "Train search results not displayed for GMR → YK"
            )

    @allure.story("Passenger Count")
    @allure.title("TC-003c: Search train with multiple adult and infant passengers")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_train_multiple_passengers(self, page):
        """Verify search works with more than 1 adult passenger."""
        with allure.step("Fill search form with 2 adults and infant"):
            self.home_page.search_train(
                origin=VALID_SEARCH["origin"],
                destination=VALID_SEARCH["destination"],
                tgl=VALID_SEARCH["tgl"],
                adults=2,
                babies=2,
            )

        with allure.step("Wait for search results"):
            self.train_list_page.wait_for_results()

        with allure.step("Verify train list is displayed"):
            assert self.train_list_page.is_train_list_displayed(), (
                "Train search results not displayed for 2 adults"
            )

    @allure.story("No Results")
    @allure.title("TC-003d: Search with far future date returns no results")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_train_no_results(self, page):
        """Verify appropriate message for unavailable date."""
        with allure.step("Search with date 3 months ahead (beyond booking window)"):
            self.home_page.search_train(
                origin=VALID_SEARCH_NOT_FOUND["origin"],
                destination=VALID_SEARCH_NOT_FOUND["destination"],
                tgl=VALID_SEARCH_NOT_FOUND["tgl"],
                adults=VALID_SEARCH_NOT_FOUND["adults"],
            )

        with allure.step("Wait for results"):
            self.train_list_page.wait_for_results()

        with allure.step("Verify no trains found"):
            is_empty = (
                self.train_list_page.is_no_result()
                or self.train_list_page.get_available_trains_count() == 0
            )
            assert is_empty, "Expected no results for far future date"

    @allure.story("Form Visibility")
    @allure.title("TC-003e: Search form visible on homepage")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_search_form_visible(self, page):
        """Verify search form is displayed on homepage."""
        with allure.step("Check search form elements are visible"):
            assert self.home_page.is_search_form_displayed(), (
                "Search form not visible on home page"
            )

    @allure.story("Business Rule")
    @allure.title("TC-003f: Baby cannot exceed adult passengers")
    @allure.severity(allure.severity_level.NORMAL)
    def test_baby_cannot_exceed_adult(self, page):
        """Verify tooltip shown when baby count exceeds adult count."""
        with allure.step("Set 1 adult passenger (default)"):
            assert self.home_page.get_adult_count() == 1

        with allure.step("Try to add 2 baby passengers"):
            self.home_page.set_baby_count(1)
            # Try clicking plus again (should trigger tooltip)
            self.home_page.click_xpath(self.home_page.XPATH_BABY_PLUS)
            self.home_page.human_delay(500, 800)

        with allure.step("Verify tooltip validation message"):
            assert self.home_page.is_baby_tooltip_visible(), (
                "Tooltip not shown when baby exceeds adult"
            )
            message = self.home_page.get_baby_tooltip_message()
            assert "Tidak bisa melebihi penumpang dewasa" in message, (
                f"Expected tooltip message about baby limit, got: {message}"
            )
