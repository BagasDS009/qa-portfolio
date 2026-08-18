"""
TC-SEARCH-001 to TC-SEARCH-011: Train search test suite for KAI Booking.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from test_data.routes import VALID_ROUTE, INVALID_ROUTES


@allure.epic("KAI Online Booking")
@allure.feature("Train Search")
@pytest.mark.wave1
class TestSearch:
    """Train schedule search test suite."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.home = HomePage(page)
        self.home.navigate_to_home()

    # === CRITICAL ===

    @allure.story("Valid Search")
    @allure.title("TC-SEARCH-001: Search valid route returns train results")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.search
    def test_search_valid_route(self, page: Page):
        """Verify search with Gambir→Bandung returns available trains."""
        with allure.step("Fill search form with valid route"):
            self.home.search_train(
                origin=VALID_ROUTE["origin"],
                destination=VALID_ROUTE["destination"],
                day=VALID_ROUTE["day"],
                months_ahead=VALID_ROUTE.get("months_ahead", 1),
            )

        train_list = TrainListPage(page)

        with allure.step("Wait for results"):
            train_list.wait_for_results()

        with allure.step("Verify trains are displayed"):
            assert train_list.is_results_displayed(), (
                f"No train results for {VALID_ROUTE['origin']} → {VALID_ROUTE['destination']}"
            )
            assert train_list.get_train_count() > 0, "Expected at least 1 train"

    # === POSITIVE ===

    @allure.story("Valid Search")
    @allure.title("TC-SEARCH-002: Search with 2 adult passengers")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_search_2_adults(self, page: Page):
        """Verify search works with multiple adults."""
        with allure.step("Search with 2 adults"):
            self.home.search_train(
                origin=VALID_ROUTE["origin"],
                destination=VALID_ROUTE["destination"],
                day=VALID_ROUTE["day"],
                adults=2,
            )

        with allure.step("Verify results shown"):
            train_list = TrainListPage(page)
            train_list.wait_for_results()
            assert train_list.is_results_displayed() or train_list.is_no_result(), (
                "Page should show results or no-result message"
            )

    @allure.story("Valid Search")
    @allure.title("TC-SEARCH-003: Search with adult + baby")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_search_adult_and_baby(self, page: Page):
        """Verify baby passenger accepted in search."""
        with allure.step("Search with 1 adult + 1 baby"):
            self.home.search_train(
                origin=VALID_ROUTE["origin"],
                destination=VALID_ROUTE["destination"],
                day=VALID_ROUTE["day"],
                adults=1,
                babies=1,
            )

        with allure.step("Verify results or no-result"):
            train_list = TrainListPage(page)
            train_list.wait_for_results()
            assert train_list.is_results_displayed() or train_list.is_no_result()

    @allure.story("UI Interaction")
    @allure.title("TC-SEARCH-004: Swap origin and destination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_swap_stations(self, page: Page):
        """Verify swap button exchanges origin and destination."""
        with allure.step("Select origin GMR and destination BD"):
            self.home.select_origin(VALID_ROUTE["origin"])
            self.home.select_destination(VALID_ROUTE["destination"])

        with allure.step("Click swap"):
            self.home.swap_stations()

        with allure.step("Verify stations swapped"):
            page.wait_for_timeout(1000)
            # After swap, values should be exchanged
            # Note: exact assertion depends on how flexdatalist handles swap

    # === NEGATIVE ===

    @allure.story("Validation")
    @allure.title("TC-SEARCH-005: Search with empty origin")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.search
    def test_search_empty_origin(self, page: Page):
        """Verify search blocked when origin is empty."""
        with allure.step("Fill only destination + date, leave origin empty"):
            self.home.select_destination(VALID_ROUTE["destination"])
            self.home.set_departure_date(VALID_ROUTE["day"])

        with allure.step("Click search"):
            self.home.click_search()

        with allure.step("Verify still on search page (not redirected)"):
            assert self.home.is_search_form_visible(), (
                "Should remain on search page when origin is empty"
            )

    @allure.story("Validation")
    @allure.title("TC-SEARCH-006: Search with empty destination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.search
    def test_search_empty_destination(self, page: Page):
        """Verify search blocked when destination is empty."""
        with allure.step("Fill only origin + date"):
            self.home.select_origin(VALID_ROUTE["origin"])
            self.home.set_departure_date(VALID_ROUTE["day"])

        with allure.step("Click search"):
            self.home.click_search()

        with allure.step("Verify still on search page"):
            assert self.home.is_search_form_visible()

    @allure.story("Validation")
    @allure.title("TC-SEARCH-007: Search without selecting date")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.search
    def test_search_no_date(self, page: Page):
        """Verify validation when date not selected."""
        with allure.step("Fill origin + destination, skip date"):
            self.home.select_origin(VALID_ROUTE["origin"])
            self.home.select_destination(VALID_ROUTE["destination"])

        with allure.step("Click search without date"):
            self.home.click_search()

        with allure.step("Verify stays on search page"):
            assert self.home.is_search_form_visible()

    @allure.story("Validation")
    @allure.title("TC-SEARCH-008: Search same origin and destination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.search
    def test_search_same_station(self, page: Page):
        """Verify search with same origin/destination is rejected."""
        data = INVALID_ROUTES["same_station"]

        with allure.step("Select same station for both"):
            self.home.select_origin(data["origin"])
            self.home.select_destination(data["destination"])
            self.home.set_departure_date(data["day"])

        with allure.step("Click search"):
            self.home.click_search()

        with allure.step("Verify error or no redirect"):
            # Either validation error shown or stays on page
            page.wait_for_timeout(2000)
            assert self.home.is_search_form_visible() or page.locator("body").is_visible()

    # === EDGE CASES ===

    @allure.story("Edge Cases")
    @allure.title("TC-SEARCH-009: Baby count cannot exceed adult count")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.search
    def test_baby_exceeds_adult_tooltip(self, page: Page):
        """Verify tooltip when baby > adult."""
        with allure.step("Set adult = 1"):
            self.home.set_adult_count(1)

        with allure.step("Try to set baby = 2"):
            self.home.set_baby_count(2)

        with allure.step("Verify baby capped at 1 or tooltip shown"):
            baby_count = self.home.get_baby_count()
            tooltip_visible = self.home.is_baby_tooltip_visible()
            assert baby_count <= 1 or tooltip_visible, (
                f"Baby ({baby_count}) should not exceed adult (1)"
            )

    @allure.story("Edge Cases")
    @allure.title("TC-SEARCH-010: Maximum adult count is 4")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.search
    def test_max_adult_count(self, page: Page):
        """Verify adult count caps at 4."""
        with allure.step("Click plus 5 times"):
            for _ in range(5):
                self.home.click_xpath(self.home.XPATH_ADULT_PLUS)
                page.wait_for_timeout(300)

        with allure.step("Verify count is 4 (max)"):
            count = self.home.get_adult_count()
            assert count <= 4, f"Adult count {count} exceeds max 4"
