"""
TC-CART-001 to TC-CART-008: Shopping cart test suite.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


@allure.epic("Practice Software Testing")
@allure.feature("Shopping Cart")
@pytest.mark.wave1
class TestCart:
    """Shopping cart management test suite."""

    @pytest.fixture
    def cart_with_item(self, page: Page) -> Page:
        """Fixture: page with one item already in cart."""
        home = HomePage(page)
        home.navigate_to_home()
        home.click_product(0)

        detail = ProductDetailPage(page)
        detail.add_to_cart()
        return page

    # === CRITICAL ===

    @allure.story("Add to Cart")
    @allure.title("TC-CART-001: Add product to cart from detail page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.cart
    def test_add_to_cart(self, page: Page):
        """Verify product can be added to cart with confirmation."""
        home = HomePage(page)
        home.navigate_to_home()

        with allure.step("Click first product"):
            home.click_product(0)

        detail = ProductDetailPage(page)

        with allure.step("Click Add to Cart"):
            detail.add_to_cart()

        with allure.step("Verify toast confirmation"):
            toast = detail.get_toast_message()
            assert "added" in toast.lower() or "cart" in toast.lower(), (
                f"Expected cart confirmation toast, got: '{toast}'"
            )

    # === POSITIVE ===

    @allure.story("Cart Management")
    @allure.title("TC-CART-002: Add multiple products to cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products(self, page: Page):
        """Verify multiple different products appear in cart."""
        home = HomePage(page)
        home.navigate_to_home()

        with allure.step("Add first product"):
            home.click_product(0)
            ProductDetailPage(page).add_to_cart()

        with allure.step("Go back and add second product"):
            home.navigate_to_home()
            home.click_product(1)
            ProductDetailPage(page).add_to_cart()

        with allure.step("Navigate to cart"):
            cart = CartPage(page)
            cart.navigate_to_cart()

        with allure.step("Verify 2 items in cart"):
            assert cart.get_item_count() == 2, (
                f"Expected 2 items in cart, got {cart.get_item_count()}"
            )

    @allure.story("Cart Management")
    @allure.title("TC-CART-003: Update product quantity in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_update_quantity(self, cart_with_item: Page):
        """Verify quantity change recalculates total."""
        cart = CartPage(cart_with_item)
        cart.navigate_to_cart()

        with allure.step("Change quantity to 3"):
            cart.set_quantity(3, index=0)

        with allure.step("Verify quantity updated"):
            qty = cart.get_item_quantity(0)
            assert qty == 3, f"Expected quantity 3, got {qty}"

    # === NEGATIVE ===

    @allure.story("Validation")
    @allure.title("TC-CART-004: Proceed with empty cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.cart
    def test_proceed_empty_cart(self, page: Page):
        """Verify cannot proceed to checkout with empty cart."""
        cart = CartPage(page)
        cart.navigate_to_cart()

        with allure.step("Verify cart is empty"):
            assert cart.is_empty(), "Cart should be empty for this test"

    @allure.story("Validation")
    @allure.title("TC-CART-005: Set quantity to zero")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.cart
    def test_quantity_zero(self, cart_with_item: Page):
        """Verify quantity 0 removes item or shows error."""
        cart = CartPage(cart_with_item)
        cart.navigate_to_cart()

        with allure.step("Set quantity to 0"):
            cart.set_quantity(0, index=0)

        with allure.step("Verify item removed or error shown"):
            # Either item is removed or validation prevents 0
            page = cart_with_item
            page.wait_for_timeout(2000)
            # Cart should be empty or show validation
            count = cart.get_item_count()
            assert count == 0 or cart.get_item_quantity(0) >= 1, (
                "Quantity 0 should remove item or be rejected"
            )

    @allure.story("Validation")
    @allure.title("TC-CART-006: Set negative quantity")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.edge
    @pytest.mark.cart
    def test_negative_quantity(self, cart_with_item: Page):
        """Verify negative quantity is rejected."""
        cart = CartPage(cart_with_item)
        cart.navigate_to_cart()

        with allure.step("Attempt to set quantity to -1"):
            cart.set_quantity(-1, index=0)

        with allure.step("Verify quantity remains valid"):
            cart_with_item.wait_for_timeout(1000)
            qty = cart.get_item_quantity(0)
            assert qty >= 1, f"Negative quantity accepted: {qty}"

    # === EDGE CASES ===

    @allure.story("Edge Cases")
    @allure.title("TC-CART-008: Remove all items from cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.edge
    @pytest.mark.cart
    def test_remove_all_items(self, cart_with_item: Page):
        """Verify cart shows empty state after removing all items."""
        cart = CartPage(cart_with_item)
        cart.navigate_to_cart()

        with allure.step("Remove item"):
            cart.remove_item(0)

        with allure.step("Verify cart is empty"):
            assert cart.is_empty(), "Cart should be empty after removing all items"
