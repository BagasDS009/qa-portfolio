"""Cart Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for /checkout (Step 1: Cart Review)."""

    # Selectors
    PRODUCT_TITLE = "[data-test='product-title']"
    PRODUCT_QUANTITY = "[data-test='product-quantity']"
    BTN_REMOVE = "a.btn-danger"
    BTN_PROCEED = "[data-test='proceed-1']"
    CART_TOTAL = "[data-test='cart-total']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def navigate_to_cart(self) -> None:
        """Navigate to cart page."""
        self.navigate("checkout")
        self.page.wait_for_load_state("networkidle")

    def set_quantity(self, quantity: int, index: int = 0) -> None:
        """Set item quantity at index."""
        qty_input = self.page.locator(self.PRODUCT_QUANTITY).nth(index)
        qty_input.fill(str(quantity))
        qty_input.press("Tab")
        self.page.wait_for_load_state("networkidle")

    def remove_item(self, index: int = 0) -> None:
        """Remove item at index from cart. Waits for DOM update."""
        item_count_before = self.get_item_count()
        self.page.locator(self.BTN_REMOVE).nth(index).click()
        # Wait for item count to change (DOM update after removal)
        if item_count_before > 0:
            self.page.wait_for_timeout(2000)
            self.page.wait_for_load_state("networkidle")

    def proceed_to_checkout(self) -> None:
        """Click proceed to checkout (Step 1 → Step 2)."""
        self.page.locator(self.BTN_PROCEED).click()
        self.page.wait_for_load_state("networkidle")

    # Verifications

    def get_item_count(self) -> int:
        """Count items in cart."""
        return self.page.locator(self.PRODUCT_TITLE).count()

    def get_item_names(self) -> list[str]:
        """Get all item names."""
        return self.page.locator(self.PRODUCT_TITLE).all_text_contents()

    def get_total(self) -> str:
        """Get cart total text."""
        return self.page.locator(self.CART_TOTAL).text_content() or ""

    def is_empty(self) -> bool:
        """Check if cart has no items. Waits for cart update."""
        # Wait for potential async cart update
        self.page.wait_for_timeout(2000)
        return self.get_item_count() == 0

    def get_item_quantity(self, index: int = 0) -> int:
        """Get quantity of item at index."""
        return int(self.page.locator(self.PRODUCT_QUANTITY).nth(index).input_value() or "0")
