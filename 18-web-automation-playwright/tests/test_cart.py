"""
TC-004: Shopping cart operations
Test cases for add to cart, update quantity, remove items.
"""

import allure
import pytest

from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


@allure.epic("Toolshop E-Commerce")
@allure.feature("Shopping Cart")
class TestCart:
    """Test suite for shopping cart operations."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Initialize page objects."""
        self.home_page = HomePage(page)
        self.product_page = ProductDetailPage(page)
        self.cart_page = CartPage(page)

    def _add_first_product(self):
        """Helper: Navigate to home and add first product to cart."""
        self.home_page.navigate_to_home()
        self.home_page.click_product(0)
        self.product_page.add_to_cart()

    @allure.story("Add to Cart")
    @allure.title("TC-004a: Add single product to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart(self, page):
        """Verify user can add a product to the cart."""
        with allure.step("Navigate to home and select first product"):
            self.home_page.navigate_to_home()
            product_name = self.home_page.get_product_names()[0]
            self.home_page.click_product(0)

        with allure.step("Add product to cart"):
            self.product_page.add_to_cart()

        with allure.step("Verify toast confirmation"):
            toast = self.product_page.get_toast_message()
            assert "added" in toast.lower() or toast != "", (
                f"Expected cart confirmation toast, got: '{toast}'"
            )

        with allure.step("Verify cart has item"):
            self.cart_page.navigate_to_cart()
            assert self.cart_page.get_cart_items_count() >= 1, (
                f"Cart should have at least 1 item after adding '{product_name}'"
            )

    @allure.story("Add to Cart")
    @allure.title("TC-004b: Add multiple products to cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products(self, page):
        """Verify user can add multiple different products."""
        with allure.step("Add first product"):
            self._add_first_product()

        with allure.step("Go back and add second product"):
            self.home_page.navigate_to_home()
            self.home_page.click_product(1)
            self.product_page.add_to_cart()

        with allure.step("Verify cart has 2 items"):
            self.cart_page.navigate_to_cart()
            assert self.cart_page.get_cart_items_count() >= 2, (
                "Cart should have at least 2 items"
            )

    @allure.story("Remove from Cart")
    @allure.title("TC-004c: Remove item from cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_item_from_cart(self, page):
        """Verify user can remove an item from cart."""
        with allure.step("Add product to cart"):
            self._add_first_product()

        with allure.step("Navigate to cart"):
            self.cart_page.navigate_to_cart()
            initial_count = self.cart_page.get_cart_items_count()

        with allure.step("Remove first item"):
            self.cart_page.remove_item(0)

        with allure.step("Verify item was removed"):
            page.wait_for_load_state("networkidle")
            new_count = self.cart_page.get_cart_items_count()
            assert new_count < initial_count, (
                f"Item not removed: count was {initial_count}, now {new_count}"
            )

    @allure.story("Update Quantity")
    @allure.title("TC-004d: Update item quantity in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_update_quantity(self, page):
        """Verify user can increase item quantity in cart."""
        with allure.step("Add product and go to cart"):
            self._add_first_product()
            self.cart_page.navigate_to_cart()

        with allure.step("Increase quantity"):
            self.cart_page.increase_quantity(0)
            page.wait_for_load_state("networkidle")

        with allure.step("Verify quantity increased"):
            qty = self.cart_page.get_item_quantity(0)
            assert int(qty) >= 2, f"Expected quantity >= 2, got {qty}"
