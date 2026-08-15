"""Product Detail Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """Page Object for product detail page."""

    # ============================================================
    # Selectors
    # ============================================================
    PRODUCT_NAME = "[data-test='product-name']"
    PRODUCT_PRICE = "[data-test='unit-price']"
    PRODUCT_DESCRIPTION = "[data-test='product-description']"
    PRODUCT_IMAGE = "#product-image"

    INPUT_QUANTITY = "[data-test='quantity']"
    BTN_ADD_TO_CART = "[data-test='add-to-cart']"
    BTN_INCREASE_QTY = "[data-test='increase-quantity']"
    BTN_DECREASE_QTY = "[data-test='decrease-quantity']"
    BTN_ADD_TO_FAVORITES = "[data-test='add-to-favorites']"

    TOAST_MESSAGE = "[role='alert']"
    RELATED_PRODUCTS = "[data-test='related-product']"

    # ============================================================
    # Actions
    # ============================================================

    def add_to_cart(self) -> None:
        """Click Add to Cart button and wait for confirmation."""
        self.page.locator(self.BTN_ADD_TO_CART).click()
        # Wait for toast confirmation to appear
        try:
            self.page.locator(self.TOAST_MESSAGE).first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass
        self.page.wait_for_timeout(1000)

    def set_quantity(self, qty: int) -> None:
        """Set product quantity."""
        input_field = self.page.locator(self.INPUT_QUANTITY)
        input_field.fill(str(qty))

    def increase_quantity(self, times: int = 1) -> None:
        """Increase quantity by clicking + button."""
        for _ in range(times):
            self.page.locator(self.BTN_INCREASE_QTY).click()

    def decrease_quantity(self, times: int = 1) -> None:
        """Decrease quantity by clicking - button."""
        for _ in range(times):
            self.page.locator(self.BTN_DECREASE_QTY).click()

    def add_to_favorites(self) -> None:
        """Click Add to Favorites button."""
        self.page.locator(self.BTN_ADD_TO_FAVORITES).click()

    # ============================================================
    # Verifications
    # ============================================================

    def get_product_name(self) -> str:
        """Get product name."""
        return self.page.locator(self.PRODUCT_NAME).text_content() or ""

    def get_product_price(self) -> str:
        """Get product price."""
        return self.page.locator(self.PRODUCT_PRICE).text_content() or ""

    def get_product_description(self) -> str:
        """Get product description."""
        return self.page.locator(self.PRODUCT_DESCRIPTION).text_content() or ""

    def get_quantity(self) -> str:
        """Get current quantity value."""
        return self.page.locator(self.INPUT_QUANTITY).input_value()

    def is_product_page_displayed(self) -> bool:
        """Verify product detail page is loaded."""
        return self.page.locator(self.PRODUCT_NAME).is_visible()

    def get_toast_message(self) -> str:
        """Get toast notification message (e.g., 'Product added to shopping cart')."""
        try:
            self.page.locator(self.TOAST_MESSAGE).wait_for(state="visible", timeout=5000)
            return self.page.locator(self.TOAST_MESSAGE).text_content() or ""
        except Exception:
            return ""

    def get_related_products_count(self) -> int:
        """Get count of related products."""
        return self.page.locator(self.RELATED_PRODUCTS).count()
