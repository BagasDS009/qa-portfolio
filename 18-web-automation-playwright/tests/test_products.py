"""
TC-003: Product browsing, search, filter, and sort
Test cases for product catalog functionality.
"""

import allure
import pytest

from pages.home_page import HomePage
from tests.test_data import SEARCH_QUERIES, SORT_OPTIONS


@allure.epic("Toolshop E-Commerce")
@allure.feature("Product Catalog")
class TestProducts:
    """Test suite for product browsing, search, filter, and sorting."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Navigate to home page."""
        self.home_page = HomePage(page)
        self.home_page.navigate_to_home()

    @allure.story("Product Grid")
    @allure.title("TC-003a: Products are displayed on home page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.products
    def test_products_displayed(self, page):
        """Verify product grid loads with products on home page."""
        with allure.step("Verify products are loaded"):
            count = self.home_page.get_product_count()
            assert count > 0, f"No products displayed on home page (got {count})"

    @allure.story("Search")
    @allure.title("TC-003b: Search products by valid keyword")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.products
    def test_search_valid_keyword(self, page):
        """Verify search returns relevant results for a valid keyword."""
        query = SEARCH_QUERIES["valid"]

        with allure.step(f"Search for '{query}'"):
            self.home_page.search_product(query)

        with allure.step("Verify search results are displayed"):
            count = self.home_page.get_product_count()
            assert count > 0, f"No results for search query: '{query}'"

    @allure.story("Search")
    @allure.title("TC-003c: Search with no matching results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.products
    def test_search_no_results(self, page):
        """Verify appropriate response when search yields no results."""
        query = SEARCH_QUERIES["no_results"]

        with allure.step(f"Search for non-existent product '{query}'"):
            self.home_page.search_product(query)

        with allure.step("Verify no results displayed"):
            assert self.home_page.has_no_results(), (
                f"Expected no results for '{query}' but products were shown"
            )

    @allure.story("Sort")
    @allure.title("TC-003d: Sort products by name A-Z")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_by_name_asc(self, page):
        """Verify products can be sorted alphabetically A-Z."""
        with allure.step("Sort products by Name (A - Z)"):
            self.home_page.sort_products(SORT_OPTIONS["name_asc"])

        with allure.step("Verify products are sorted"):
            names = self.home_page.get_product_names()
            assert names == sorted(names, key=str.lower), (
                f"Products not sorted A-Z: {names[:5]}"
            )

    @allure.story("Sort")
    @allure.title("TC-003e: Sort products by name Z-A")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_by_name_desc(self, page):
        """Verify products can be sorted alphabetically Z-A."""
        with allure.step("Sort products by Name (Z - A)"):
            self.home_page.sort_products(SORT_OPTIONS["name_desc"])

        with allure.step("Verify products are sorted descending"):
            names = self.home_page.get_product_names()
            assert names == sorted(names, key=str.lower, reverse=True), (
                f"Products not sorted Z-A: {names[:5]}"
            )

    @allure.story("Pagination")
    @allure.title("TC-003f: Navigate to next page of products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.products
    def test_pagination_next_page(self, page):
        """Verify pagination works and shows different products."""
        with allure.step("Get products on first page"):
            first_page_names = self.home_page.get_product_names()

        with allure.step("Navigate to next page"):
            self.home_page.go_to_next_page()

        with allure.step("Verify different products on second page"):
            second_page_names = self.home_page.get_product_names()
            assert second_page_names != first_page_names, (
                "Second page shows same products as first page"
            )
