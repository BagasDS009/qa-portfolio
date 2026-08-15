"""Checkout Page Object for Practice Software Testing (Toolshop)."""

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for multi-step checkout flow."""

    # ============================================================
    # Step 2: Sign In (when already logged in, just proceed)
    # ============================================================
    BTN_PROCEED_SIGN_IN = "[data-test='proceed-2']"

    # ============================================================
    # Step 3: Billing Address
    # ============================================================
    INPUT_STREET = "[data-test='street']"
    INPUT_HOUSE_NUMBER = "[data-test='house_number']"
    INPUT_CITY = "[data-test='city']"
    INPUT_STATE = "[data-test='state']"
    SELECT_COUNTRY = "[data-test='country']"
    INPUT_POSTCODE = "[data-test='postal_code']"
    BTN_PROCEED_ADDRESS = "[data-test='proceed-3']"

    # ============================================================
    # Step 4: Payment
    # ============================================================
    SELECT_PAYMENT_METHOD = "[data-test='payment-method']"
    INPUT_BANK_NAME = "[data-test='bank_name']"
    INPUT_ACCOUNT_NAME = "[data-test='account_name']"
    INPUT_ACCOUNT_NUMBER = "[data-test='account_number']"
    BTN_CONFIRM = "[data-test='finish']"

    # ============================================================
    # Step 5: Confirmation
    # ============================================================
    CONFIRMATION_MESSAGE = "[data-test='payment-success-message']"

    # ============================================================
    # Actions — Step 2: Proceed (already logged in)
    # ============================================================

    def proceed_past_sign_in(self) -> None:
        """Click proceed on the sign-in step (when already logged in)."""
        self.page.locator(self.BTN_PROCEED_SIGN_IN).click()
        self.page.wait_for_timeout(2000)

    # ============================================================
    # Actions — Step 3: Billing Address
    # ============================================================

    def fill_billing_address(
        self,
        street: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        house_number: str = "1",
    ) -> None:
        """Fill billing address form."""
        self.page.locator(self.INPUT_STREET).fill(street)
        self.page.locator(self.INPUT_HOUSE_NUMBER).fill(house_number)
        self.page.locator(self.INPUT_CITY).fill(city)
        self.page.locator(self.INPUT_STATE).fill(state)
        self.page.locator(self.SELECT_COUNTRY).select_option(value=country)
        self.page.locator(self.INPUT_POSTCODE).fill(postcode)

    def proceed_to_payment(self) -> None:
        """Proceed from billing address to payment step."""
        self.page.locator(self.BTN_PROCEED_ADDRESS).click()
        self.page.wait_for_timeout(2000)

    # ============================================================
    # Actions — Step 4: Payment
    # ============================================================

    def select_payment_method(self, method: str) -> None:
        """Select a payment method from dropdown."""
        self.page.locator(self.SELECT_PAYMENT_METHOD).select_option(label=method)
        self.page.wait_for_timeout(1500)

    def fill_bank_transfer(
        self,
        bank_name: str = "Test Bank",
        account_name: str = "Test Account",
        account_number: str = "1234567890",
    ) -> None:
        """Fill bank transfer payment details."""
        self.page.locator(self.INPUT_BANK_NAME).fill(bank_name)
        self.page.locator(self.INPUT_ACCOUNT_NAME).fill(account_name)
        self.page.locator(self.INPUT_ACCOUNT_NUMBER).fill(account_number)

    def confirm_payment(self) -> None:
        """Click confirm/finish button."""
        self.page.locator(self.BTN_CONFIRM).click()
        self.page.wait_for_timeout(3000)

    # ============================================================
    # Full checkout flow helper
    # ============================================================

    def complete_checkout_logged_in(
        self,
        street: str,
        city: str,
        state: str,
        country: str,
        postcode: str,
        payment_method: str = "Bank Transfer",
    ) -> None:
        """Complete checkout from billing address step (already logged in)."""
        # Step 3: Billing address
        self.fill_billing_address(street, city, state, country, postcode)
        self.proceed_to_payment()

        # Step 4: Payment
        self.select_payment_method(payment_method)
        if payment_method == "Bank Transfer":
            self.fill_bank_transfer()
        self.confirm_payment()

    # ============================================================
    # Verifications
    # ============================================================

    def is_checkout_complete(self) -> bool:
        """Verify order confirmation is displayed."""
        try:
            self.page.locator(self.CONFIRMATION_MESSAGE).wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False

    def get_confirmation_message(self) -> str:
        """Get order confirmation message."""
        return self.page.locator(self.CONFIRMATION_MESSAGE).text_content() or ""

    def is_on_billing_step(self) -> bool:
        """Check if we are on the billing address step."""
        return self.page.locator(self.INPUT_STREET).is_visible()

    def is_on_payment_step(self) -> bool:
        """Check if we are on the payment step."""
        return self.page.locator(self.SELECT_PAYMENT_METHOD).is_visible()
