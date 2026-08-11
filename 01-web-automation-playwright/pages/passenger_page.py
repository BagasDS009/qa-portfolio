"""Passenger Data Page Object for KAI Booking - XPath Locators."""

from pages.base_page import BasePage


class PassengerPage(BasePage):
    """Page Object for passenger information form using XPath."""

    # ============================================================
    # XPath Locators - Contact Person
    # ============================================================
    XPATH_CONTACT_NAME_TITLE = "//select[@id='pemesan_title' and @name='pemesan_title']"
    XPATH_CONTACT_PHONE = "//input[@id='pemesan_nohp' and @name='pemesan_nohp']"
    XPATH_CONTACT_EMAIL = "//input[@id='pemesan_email' and @name='pemesan_email']"
    XPATH_CONTACT_NAME = "//input[@id='pemesan_nama' and @name='pemesan_nama']"
    XPATH_CONTACT_ID_TYPE = "//select[@id='pemesan_tandapengenal' and @name='pemesan_tandapengenal']"
    XPATH_CONTACT_ID_NUMBER = "//input[@id='pemesan_notandapengenal']"
    XPATH_CONTACT_ALAMAT = "//input[@id='pemesan_alamat' and @name='pemesan_alamat']"

    # XPath Locators - Passenger Info
    XPATH_PASSENGER_NAME = "//input[@id='penumpang_nama1' and @name='penumpang_nama[]']"
    XPATH_PASSENGER_ID_TYPE = "//select[@id='penumpang_title1' and @name='penumpang_title[]']"
    XPATH_PASSENGER_ID_NUMBER_TYPE = "//select[@id='penumpang_tandapengenal1' and @name='penumpang_tandapengenal[]']"
    XPATH_PASSENGER_ID_NUMBER = "//input[@id='penumpang_notandapengenal1' and @name='penumpang_notandapengenal[]']"

    # XPath Locators - Actions
    XPATH_CONTINUE_BUTTON = "//button[@id='bayar' and @name='submitbutton']"
    XPATH_BACK_BUTTON = "//button[contains(text(),'Kembali') or contains(text(),'Back')]"
    XPATH_VALIDATION_ERROR = "//*[contains(@class,'error') or contains(@class,'invalid-feedback') or contains(@class,'text-danger')]"
    XPATH_VALIDATION_ERROR_MOHON_ISI_NAME = "//li[normalize-space()='Mohon isi Nama']"
    XPATH_VALIDATION_ERROR_MOHON_ISI_NO_ID = "//li[normalize-space()='Mohon isi Nomor Identitas']"
    XPATH_VALIDATION_ERROR_MOHON_ISI_EMAIL = "//li[normalize-space()='Mohon diisi Email']"
    XPATH_VALIDATION_PASSENGER_ERROR_MOHON_ISI_NO_ID = "//li[normalize-space()='Nomor Identitas Wajib Diisi']"
    XPATH_VALIDATION_PASSENGER_ERROR_MOHON_NAME = "//li[normalize-space()='Fill out this field']"
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

    def is_validation_error_displayed_name_error(self) -> bool:
        """Check if any validation error is shown."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_ERROR_MOHON_ISI_NAME) or self.is_visible_xpath(
            self.XPATH_REQUIRED_ERROR
        )
    def is_validation_error_displayed_no_id(self) -> bool:
        """Check if any validation error is shown."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_ERROR_MOHON_ISI_NO_ID) or self.is_visible_xpath(
            self.XPATH_REQUIRED_ERROR
        )
    def is_validation_error_displayed_email(self) -> bool:
        """Check if any validation error is shown."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_ERROR_MOHON_ISI_EMAIL) or self.is_visible_xpath(
            self.XPATH_REQUIRED_ERROR
        )

    def is_validation_passenger_no_id_error(self) -> bool:
        """Check if 'Nomor Identitas Wajib Diisi' error is shown."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_PASSENGER_ERROR_MOHON_ISI_NO_ID)

    def is_validation_passenger_name_error(self) -> bool:
        """Check if 'Fill out this field' error is shown for passenger name."""
        return self.is_visible_xpath(self.XPATH_VALIDATION_PASSENGER_ERROR_MOHON_NAME)

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

    def is_submit_button_disabled(self) -> bool:
        """Check if submit/continue button is disabled when form is empty."""
        locator = self.page.locator(f"xpath={self.XPATH_CONTINUE_BUTTON}")
        return locator.is_disabled()
