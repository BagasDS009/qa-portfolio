"""
TC-SEARCH-001 to TC-SEARCH-008: Product search and filter test suite.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from test_data.products import SEARCH_QUERIES, SORT_OPTIONS


@allure.epic("Practice Software Testing")
@allure.feature("Product Search & Filter")
@pytest.mark.wave1
class TestSearch:
    """Product search, filter, and sort test suite."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.home = HomePage(page)
        self.home.navigate_to_home()

    # === CRITICAL ===

    @allure.story("Search")
    @allure.title("TC-SEARCH-001: Search by keyword returns matching products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.search
    def test_search_valid_keyword(self, page: Page):
        """Verify search returns products matching keyword."""
        with allure.step("Search for 'pliers'"):
            self.home.search(SEARCH_QUERIES["valid_exact"])

        with allure.step("Verify matching products displayed"):
            assert self.home.has_results(), "No results for 'pliers'"
            names = self.home.get_product_names()
            matching = [n for n in names if "plier" in n.lower()]
            assert len(matching) > 0, (
                f"No product names contain 'plier'. Got: {names}"
            )

    # === POSITIVE ===

    @allure.story("Search")
    @allure.title("TC-SEARCH-002: Partial keyword search")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_search_partial_keyword(self, page: Page):
        """Verify partial keyword returns results (e.g., 'ham' → 'hammer')."""
        with allure.step("Search for 'ham'"):
            self.home.search(SEARCH_QUERIES["valid_partial"])

        with allure.step("Verify results contain matching products"):
            assert self.home.has_results(), "No results for partial keyword 'ham'"

    @allure.story("Filter")
    @allure.title("TC-SEARCH-003: Filter by category reduces results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_filter_by_category(self, page: Page):
        """Verify category filter narrows product list."""
        with allure.step("Get initial product count"):
            initial_count = self.home.get_product_count()

        with allure.step("Apply Hand Tools category filter"):
            self.home.filter_by_category("Hand Tools")

        with allure.step("Verify results filtered (count changed)"):
            filtered_count = self.home.get_product_count()
            assert filtered_count > 0, "Category filter returned no results"
            assert filtered_count <= initial_count, (
                f"Filter should reduce results: {filtered_count} > {initial_count}"
            )

    @allure.story("Sort")
    @allure.title("TC-SEARCH-004: Sort products by price low to high")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.search
    def test_sort_price_ascending(self, page: Page):
        """Verify sort orders products by ascending price."""
        with allure.step("Sort by Price (Low - High)"):
            self.home.sort_by(SORT_OPTIONS["price_asc"])

        with allure.step("Verify prices are in ascending order"):
            prices = self.home.get_product_prices()
            assert len(prices) > 1, "Not enough products to verify sort"
            assert prices == sorted(prices), (
                f"Prices not in ascending order: {prices}"
            )

    # === NEGATIVE ===

    @allure.story("Search")
    @allure.title("TC-SEARCH-005: Search with non-existent keyword shows no results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.search
    def test_search_no_results(self, page: Page):
        """Verify appropriate handling of keyword with no matches."""
        with allure.step("Search for non-existent keyword"):
            self.home.search(SEARCH_QUERIES["no_results"])

        with allure.step("Verify no products shown"):
            assert not self.home.has_results(), (
                "Expected no results for 'xyznonexistent999'"
            )

    @allure.story("Search")
    @allure.title("TC-SEARCH-006: Empty search shows all products")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.search
    def test_search_empty_query(self, page: Page):
        """Verify empty search doesn't filter anything."""
        with allure.step("Submit empty search"):
            self.home.search("")

        with allure.step("Verify products still displayed"):
            assert self.home.has_results(), (
                "Empty search should show all products"
            )

    # === EDGE CASES ===

    @allure.story("Security")
    @allure.title("TC-SEARCH-007: SQL wildcard in search")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.search
    def test_search_sql_wildcard(self, page: Page):
        """Verify SQL wildcard % is handled safely."""
        with allure.step("Search with '%'"):
            self.home.search(SEARCH_QUERIES["sql_wildcard"])

        with allure.step("Verify no server error (page still functional)"):
            # Should either show results or empty — not crash
            assert page.locator("body").is_visible(), "Page crashed on SQL wildcard input"

    @allure.story("Security")
    @allure.title("TC-SEARCH-008: Special characters in search")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.search
    def test_search_special_chars(self, page: Page):
        """Verify special characters don't break the page."""
        with allure.step("Search with special chars '<%>'"):
            self.home.search(SEARCH_QUERIES["special_chars"])

        with allure.step("Verify page still functional"):
            assert page.locator("body").is_visible(), "Page broke on special char input"
