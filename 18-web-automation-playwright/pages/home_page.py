"""Home Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the home/products page with search, filters, and product grid."""

    # ============================================================
    # Selectors
    # ============================================================
    INPUT_SEARCH = "[data-test='search-query']"
    BTN_SEARCH = "[data-test='search-submit']"
    BTN_RESET_SEARCH = "[data-test='search-reset']"

    # Product grid
    PRODUCT_CARD = "a.card"
    PRODUCT_NAME = "[data-test='product-name']"
    PRODUCT_PRICE = "[data-test='product-price']"

    # Filters & Sort
    SORT_SELECT = "[data-test='sort']"
    PAGINATION_NEXT = "[data-test='pagination-next']"
    PAGINATION_PREV = "[data-test='pagination-prev']"

    # Navigation
    NAV_HOME = "[data-test='nav-home']"
    NAV_CATEGORIES = "[data-test='nav-categories']"
    NAV_CONTACT = "[data-test='nav-contact']"
    NAV_SIGN_IN = "[data-test='nav-sign-in']"
    NAV_CART = "[data-test='nav-cart']"

    # ============================================================
    # Actions
    # ============================================================

    def navigate_to_home(self) -> None:
        """Navigate to home page and wait for products to load."""
        self.navigate()
        self.page.locator(self.PRODUCT_CARD).first.wait_for(state="visible", timeout=15000)

    def search_product(self, query: str) -> None:
        """Search for a product by keyword."""
        self.page.locator(self.INPUT_SEARCH).fill(query)
        self.page.locator(self.BTN_SEARCH).click()
        self.page.wait_for_timeout(2000)

    def reset_search(self) -> None:
        """Reset search/filters."""
        self.page.locator(self.BTN_RESET_SEARCH).click()
        self.page.locator(self.PRODUCT_CARD).first.wait_for(state="visible", timeout=10000)

    def sort_products(self, sort_label: str) -> None:
        """Sort products by option label (e.g., 'Name (A - Z)')."""
        self.page.locator(self.SORT_SELECT).select_option(label=sort_label)
        self.page.wait_for_timeout(2000)

    def filter_by_category(self, category_id: str) -> None:
        """Filter products by clicking category checkbox."""
        self.page.locator(f"[data-test='category-{category_id}']").check()
        self.page.wait_for_timeout(2000)

    def click_product(self, index: int = 0) -> None:
        """Click on a product card by index (0-based)."""
        self.page.locator(self.PRODUCT_CARD).nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def click_product_by_name(self, name: str) -> None:
        """Click on a specific product by name."""
        self.page.locator(self.PRODUCT_NAME).filter(has_text=name).first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_next_page(self) -> None:
        """Click next page in pagination."""
        self.page.locator(self.PAGINATION_NEXT).click()
        self.page.wait_for_timeout(2000)

    def go_to_sign_in(self) -> None:
        """Navigate to sign-in page via nav."""
        self.page.locator(self.NAV_SIGN_IN).click()

    def go_to_cart(self) -> None:
        """Navigate to cart via nav."""
        self.page.locator(self.NAV_CART).click()

    def go_to_contact(self) -> None:
        """Navigate to contact page via nav."""
        self.page.locator(self.NAV_CONTACT).click()

    # ============================================================
    # Verifications
    # ============================================================

    def get_product_count(self) -> int:
        """Get number of products displayed on current page."""
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_product_names(self) -> list[str]:
        """Get all product names on current page."""
        self.page.locator(self.PRODUCT_NAME).first.wait_for(state="visible", timeout=10000)
        return self.page.locator(self.PRODUCT_NAME).all_text_contents()

    def get_product_prices(self) -> list[str]:
        """Get all product prices on current page."""
        return self.page.locator(self.PRODUCT_PRICE).all_text_contents()

    def get_cart_quantity(self) -> str:
        """Get cart item count from nav badge."""
        try:
            badge = self.page.locator(f"{self.NAV_CART} span")
            if badge.is_visible():
                return badge.text_content() or "0"
            return "0"
        except Exception:
            return "0"

    def is_product_displayed(self, name: str) -> bool:
        """Check if a specific product is displayed."""
        return self.page.locator(self.PRODUCT_NAME).filter(has_text=name).count() > 0

    def has_no_results(self) -> bool:
        """Check if no products are shown (empty results)."""
        self.page.wait_for_timeout(2000)
        return self.get_product_count() == 0
