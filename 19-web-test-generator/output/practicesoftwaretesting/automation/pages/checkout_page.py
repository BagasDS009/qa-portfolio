"""Checkout Page Object for Practice Software Testing (Toolshop)."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for multi-step checkout (Steps 2-5)."""

    # Step 2: Sign In
    BTN_PROCEED_SIGN_IN = "[data-test='proceed-2']"

    # Step 3: Billing Address
    INPUT_STREET = "[data-test='street']"
    INPUT_HOUSE_NUMBER = "[data-test='house_number']"
    INPUT_CITY = "[data-test='city']"
    INPUT_STATE = "[data-test='state']"
    SELECT_COUNTRY = "[data-test='country']"
    INPUT_POSTCODE = "[data-test='postal_code']"
    BTN_PROCEED_ADDRESS = "[data-test='proceed-3']"

    # Step 4: Payment
    SELECT_PAYMENT = "[data-test='payment-method']"
    INPUT_BANK_NAME = "[data-test='bank_name']"
    INPUT_ACCOUNT_NAME = "[data-test='account_name']"
    INPUT_ACCOUNT_NUMBER = "[data-test='account_number']"
    BTN_CONFIRM = "[data-test='finish']"

    # Step 5: Confirmation
    SUCCESS_MESSAGE = "[data-test='payment-success-message']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Step 2 Actions

    def proceed_sign_in(self) -> None:
        """Proceed past sign-in step (already logged in)."""
        self.page.locator(self.BTN_PROCEED_SIGN_IN).click()
        self.page.wait_for_load_state("networkidle")

    # Step 3 Actions

    def fill_billing_address(
        self, street: str, house_number: str, city: str,
        state: str, country: str, postcode: str,
    ) -> None:
        """Fill billing address form."""
        self.page.locator(self.INPUT_STREET).fill(street)
        self.page.locator(self.INPUT_HOUSE_NUMBER).fill(house_number)
        self.page.locator(self.INPUT_CITY).fill(city)
        self.page.locator(self.INPUT_STATE).fill(state)
        self.page.locator(self.SELECT_COUNTRY).select_option(value=country)
        self.page.locator(self.INPUT_POSTCODE).fill(postcode)

    def proceed_to_payment(self) -> None:
        """Proceed from billing to payment step."""
        self.page.locator(self.BTN_PROCEED_ADDRESS).click()
        self.page.wait_for_load_state("networkidle")

    # Step 4 Actions

    def select_payment_method(self, label: str) -> None:
        """Select payment method by label."""
        self.page.locator(self.SELECT_PAYMENT).select_option(label=label)
        self.page.wait_for_timeout(500)

    def fill_bank_transfer(
        self, bank_name: str = "Test Bank",
        account_name: str = "Test Account",
        account_number: str = "1234567890",
    ) -> None:
        """Fill bank transfer fields."""
        self.page.locator(self.INPUT_BANK_NAME).fill(bank_name)
        self.page.locator(self.INPUT_ACCOUNT_NAME).fill(account_name)
        self.page.locator(self.INPUT_ACCOUNT_NUMBER).fill(account_number)

    def confirm_payment(self) -> None:
        """Click confirm/finish button."""
        self.page.locator(self.BTN_CONFIRM).click()

    # Full flow helper

    def complete_checkout(
        self, street: str, house_number: str, city: str,
        state: str, country: str, postcode: str,
        payment_method: str = "Bank Transfer",
    ) -> None:
        """Complete full checkout from Step 2 onwards."""
        self.proceed_sign_in()
        self.fill_billing_address(street, house_number, city, state, country, postcode)
        self.proceed_to_payment()
        self.select_payment_method(payment_method)
        if payment_method == "Bank Transfer":
            self.fill_bank_transfer()
        self.confirm_payment()

    # Verifications

    def is_checkout_complete(self) -> bool:
        """Check if success message is shown."""
        try:
            self.page.locator(self.SUCCESS_MESSAGE).wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def get_confirmation_message(self) -> str:
        """Get order confirmation text."""
        return self.page.locator(self.SUCCESS_MESSAGE).text_content() or ""

    def is_on_billing_step(self) -> bool:
        """Check if on billing address step."""
        return self.page.locator(self.INPUT_STREET).is_visible()

    def is_on_payment_step(self) -> bool:
        """Check if on payment step."""
        return self.page.locator(self.SELECT_PAYMENT).is_visible()
