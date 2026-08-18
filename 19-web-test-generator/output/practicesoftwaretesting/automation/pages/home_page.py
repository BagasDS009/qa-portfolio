"""Home Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for homepage — product listing, search, filter, sort."""

    # Selectors
    INPUT_SEARCH = "[data-test='search-query']"
    BTN_SEARCH = "[data-test='search-submit']"
    BTN_RESET = "[data-test='search-reset']"
    SELECT_SORT = "[data-test='sort']"
    PRODUCT_CARD = "a.card"
    PRODUCT_NAME = "[data-test='product-name']"
    PRODUCT_PRICE = "[data-test='product-price']"
    PAGINATION_NEXT = "[data-test='pagination-next']"
    NAV_SIGN_IN = "[data-test='nav-sign-in']"
    NAV_CART = "[data-test='nav-cart']"
    NAV_CONTACT = "[data-test='nav-contact']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Actions

    def navigate_to_home(self) -> None:
        """Navigate to homepage and wait for products."""
        self.navigate()
        self.page.locator(self.PRODUCT_CARD).first.wait_for(state="visible", timeout=15000)

    def search(self, query: str) -> None:
        """Search products by keyword."""
        self.page.locator(self.INPUT_SEARCH).fill(query)
        self.page.locator(self.BTN_SEARCH).click()
        self.page.wait_for_load_state("networkidle")

    def reset_search(self) -> None:
        """Reset search and filters."""
        self.page.locator(self.BTN_RESET).click()
        self.page.wait_for_load_state("networkidle")

    def sort_by(self, label: str) -> None:
        """Sort products (e.g., 'Name (A - Z)', 'Price (Low - High)')."""
        self.page.locator(self.SELECT_SORT).select_option(label=label)
        self.page.wait_for_load_state("networkidle")

    def filter_by_category(self, category_name: str) -> None:
        """Check a category filter checkbox by visible label text."""
        # Category IDs are dynamic — find by label text instead
        checkbox = self.page.locator(f"label:has-text('{category_name}') input[type='checkbox']")
        if checkbox.count() == 0:
            # Fallback: find data-test containing 'category-' near the label
            checkbox = self.page.locator(f"label").filter(has_text=category_name).locator("input")
        checkbox.first.check()
        self.page.wait_for_load_state("networkidle")

    def click_product(self, index: int = 0) -> None:
        """Click a product card by index."""
        self.page.locator(self.PRODUCT_CARD).nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def go_to_sign_in(self) -> None:
        """Click sign in nav link."""
        self.page.locator(self.NAV_SIGN_IN).click()

    def go_to_cart(self) -> None:
        """Click cart nav link."""
        self.page.locator(self.NAV_CART).click()

    # Verifications

    def get_product_count(self) -> int:
        """Count visible product cards."""
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_product_names(self) -> list[str]:
        """Get all product name texts on current page."""
        self.page.locator(self.PRODUCT_NAME).first.wait_for(state="visible", timeout=10000)
        return self.page.locator(self.PRODUCT_NAME).all_text_contents()

    def get_product_prices(self) -> list[float]:
        """Get all product prices as floats."""
        texts = self.page.locator(self.PRODUCT_PRICE).all_text_contents()
        return [float(p.replace("$", "").strip()) for p in texts if p.strip()]

    def has_results(self) -> bool:
        """Check if any products are displayed."""
        self.page.wait_for_timeout(2000)
        return self.get_product_count() > 0

    def get_cart_badge_count(self) -> int:
        """Get cart item count from nav badge."""
        try:
            badge = self.page.locator(f"{self.NAV_CART} [data-test='cart-quantity']")
            if badge.is_visible():
                return int(badge.text_content() or "0")
        except Exception:
            pass
        return 0
