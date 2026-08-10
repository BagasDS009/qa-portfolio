"""Passenger Data Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class PassengerPage(BasePage):
    """Page Object for passenger information form using XPath."""

    # ============================================================
    # XPath Locators - Contact Person
    # ============================================================
    XPATH_CONTACT_NAME = "//input[contains(@name,'contact_name') or contains(@placeholder,'Nama Pemesan') or @id='contactName']"
    XPATH_CONTACT_PHONE = "//input[contains(@name,'contact_phone') or contains(@placeholder,'Telepon') or @id='contactPhone']"
    XPATH_CONTACT_EMAIL = "//input[contains(@name,'contact_email') or contains(@placeholder,'Email') or @id='contactEmail']"

    # XPath Locators - Passenger Info
    XPATH_PASSENGER_NAME = "//input[contains(@name,'passenger_name') or contains(@placeholder,'Nama Penumpang') or contains(@name,'passengername')]"
    XPATH_PASSENGER_ID_TYPE = "//select[contains(@name,'id_type') or contains(@name,'idType')]"
    XPATH_PASSENGER_ID_NUMBER = "//input[contains(@name,'id_number') or contains(@placeholder,'Nomor Identitas') or contains(@name,'idNumber')]"
    XPATH_PASSENGER_PHONE = "//input[contains(@name,'passenger_phone') or contains(@placeholder,'No. Telepon Penumpang')]"

    # XPath Locators - Actions
    XPATH_CONTINUE_BUTTON = "//button[contains(text(),'Lanjutkan') or contains(text(),'Continue') or contains(text(),'Selanjutnya')]"
    XPATH_BACK_BUTTON = "//button[contains(text(),'Kembali') or contains(text(),'Back')]"
    XPATH_VALIDATION_ERROR = "//*[contains(@class,'error') or contains(@class,'invalid-feedback') or contains(@class,'text-danger')]"
    XPATH_REQUIRED_ERROR = "//*[contains(text(),'wajib') or contains(text(),'harus diisi') or contains(text(),'required')]"

    def fill_contact_person(self, name: str, phone: str, email: str):
        """Fill contact person information."""
        self.fill_xpath(self.XPATH_CONTACT_NAME, name)
        self.fill_xpath(self.XPATH_CONTACT_PHONE, phone)
        self.fill_xpath(self.XPATH_CONTACT_EMAIL, email)

    def fill_passenger_info(
        self,
        name: str,
        id_type: str = "KTP",
        id_number: str = "",
        phone: str = "",
        index: int = 0,
    ):
        """Fill passenger information by index (for multi-passenger)."""
        # Fill passenger name
        passenger_names = self.page.locator(f"xpath={self.XPATH_PASSENGER_NAME}")
        passenger_names.nth(index).fill(name)

        # Fill ID number
        if id_number:
            id_numbers = self.page.locator(f"xpath={self.XPATH_PASSENGER_ID_NUMBER}")
            id_numbers.nth(index).fill(id_number)

        # Fill phone if available
        if phone:
            phones = self.page.locator(f"xpath={self.XPATH_PASSENGER_PHONE}")
            if phones.count() > index:
                phones.nth(index).fill(phone)

    def click_continue(self):
        """Click continue/next button."""
        self.click_xpath(self.XPATH_CONTINUE_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def click_back(self):
        """Click back button."""
        self.click_xpath(self.XPATH_BACK_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def is_validation_error_displayed(self) -> bool:
        """Check if any validation error is shown."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_ERROR) or self.is_visible_xpath(
            self.XPATH_REQUIRED_ERROR
        )

    def get_validation_errors(self) -> list[str]:
        """Get all validation error messages."""
        errors = self.page.locator(f"xpath={self.XPATH_VALIDATION_ERROR}").all_text_contents()
        return [e.strip() for e in errors if e.strip()]

    def is_passenger_form_displayed(self) -> bool:
        """Check if passenger form is displayed."""
        return self.is_visible_xpath(self.XPATH_CONTACT_NAME) or self.is_visible_xpath(
            self.XPATH_PASSENGER_NAME
        )

    def submit_empty_form(self):
        """Submit form without filling any fields (for validation testing)."""
        self.click_continue()
