"""Product Detail Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """Page Object for /product/{id}."""

    # Selectors
    PRODUCT_NAME = "[data-test='product-name']"
    UNIT_PRICE = "[data-test='unit-price']"
    DESCRIPTION = "[data-test='product-description']"
    INPUT_QUANTITY = "[data-test='quantity']"
    BTN_ADD_TO_CART = "[data-test='add-to-cart']"
    BTN_INCREASE_QTY = "[data-test='increase-quantity']"
    BTN_DECREASE_QTY = "[data-test='decrease-quantity']"
    BTN_ADD_FAVORITES = "[data-test='add-to-favorites']"
    TOAST = "[role='alert']"
    RELATED_PRODUCTS = "[data-test='related-product']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def add_to_cart(self) -> None:
        """Click Add to Cart and wait for toast confirmation."""
        self.page.locator(self.BTN_ADD_TO_CART).click()
        try:
            self.page.locator(self.TOAST).first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass

    def set_quantity(self, qty: int) -> None:
        """Set quantity directly."""
        self.page.locator(self.INPUT_QUANTITY).fill(str(qty))

    def increase_quantity(self, times: int = 1) -> None:
        """Click + button N times."""
        for _ in range(times):
            self.page.locator(self.BTN_INCREASE_QTY).click()

    def decrease_quantity(self, times: int = 1) -> None:
        """Click - button N times."""
        for _ in range(times):
            self.page.locator(self.BTN_DECREASE_QTY).click()

    # Verifications

    def get_product_name(self) -> str:
        """Get product title."""
        return self.page.locator(self.PRODUCT_NAME).text_content() or ""

    def get_price(self) -> str:
        """Get unit price text."""
        return self.page.locator(self.UNIT_PRICE).text_content() or ""

    def get_quantity(self) -> int:
        """Get current quantity value."""
        return int(self.page.locator(self.INPUT_QUANTITY).input_value() or "1")

    def get_toast_message(self) -> str:
        """Get toast notification text."""
        try:
            self.page.locator(self.TOAST).first.wait_for(state="visible", timeout=5000)
            return self.page.locator(self.TOAST).first.text_content() or ""
        except Exception:
            return ""

    def is_loaded(self) -> bool:
        """Check if product detail page is displayed."""
        return self.page.locator(self.PRODUCT_NAME).is_visible()
