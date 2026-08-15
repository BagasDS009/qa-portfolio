"""Cart Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for shopping cart page."""

    # ============================================================
    # Selectors (based on actual site v5 structure)
    # ============================================================
    PRODUCT_TITLE = "[data-test='product-title']"
    PRODUCT_QUANTITY = "[data-test='product-quantity']"
    BTN_REMOVE = "a.btn-danger"
    BTN_PROCEED_CHECKOUT = "[data-test='proceed-1']"
    CART_TOTAL = "[data-test='cart-total']"

    # ============================================================
    # Actions
    # ============================================================

    def navigate_to_cart(self) -> None:
        """Navigate directly to cart/checkout page."""
        self.navigate("checkout")
        self.page.wait_for_timeout(3000)

    def remove_item(self, index: int = 0) -> None:
        """Remove item from cart by index."""
        self.page.locator(self.BTN_REMOVE).nth(index).click()
        self.page.wait_for_timeout(3000)

    def set_quantity(self, quantity: int, index: int = 0) -> None:
        """Set item quantity directly."""
        qty_input = self.page.locator(self.PRODUCT_QUANTITY).nth(index)
        qty_input.fill(str(quantity))
        qty_input.press("Tab")
        self.page.wait_for_timeout(1500)

    def increase_quantity(self, index: int = 0) -> None:
        """Increase item quantity by 1."""
        qty_input = self.page.locator(self.PRODUCT_QUANTITY).nth(index)
        current = int(qty_input.input_value() or "1")
        qty_input.fill(str(current + 1))
        qty_input.press("Tab")
        self.page.wait_for_timeout(1500)

    def decrease_quantity(self, index: int = 0) -> None:
        """Decrease item quantity by 1."""
        qty_input = self.page.locator(self.PRODUCT_QUANTITY).nth(index)
        current = int(qty_input.input_value() or "1")
        if current > 1:
            qty_input.fill(str(current - 1))
            qty_input.press("Tab")
            self.page.wait_for_timeout(1500)

    def proceed_to_checkout(self) -> None:
        """Click proceed to checkout (step 1 -> step 2: sign in)."""
        self.page.locator(self.BTN_PROCEED_CHECKOUT).click()
        self.page.wait_for_timeout(2000)

    # ============================================================
    # Verifications
    # ============================================================

    def get_cart_items_count(self) -> int:
        """Get number of items in cart."""
        return self.page.locator(self.PRODUCT_TITLE).count()

    def get_item_names(self) -> list[str]:
        """Get all item names in cart."""
        return self.page.locator(self.PRODUCT_TITLE).all_text_contents()

    def get_cart_total(self) -> str:
        """Get cart total amount."""
        return self.page.locator(self.CART_TOTAL).text_content() or ""

    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.get_cart_items_count() == 0

    def get_item_quantity(self, index: int = 0) -> str:
        """Get quantity of item by index."""
        return self.page.locator(self.PRODUCT_QUANTITY).nth(index).input_value()
