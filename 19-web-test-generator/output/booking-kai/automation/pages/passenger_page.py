"""Passenger Data Page Object for KAI Booking."""

from pages.base_page import BasePage


class PassengerPage(BasePage):
    """Page Object for passenger/contact information form."""

    # Contact Person
    XPATH_CONTACT_NAME = '//input[@id="pemesan_nama"]'
    XPATH_CONTACT_PHONE = '//input[@id="pemesan_nohp"]'
    XPATH_CONTACT_EMAIL = '//input[@id="pemesan_email"]'
    XPATH_CONTACT_ID_NUMBER = '//input[@id="pemesan_notandapengenal"]'
    XPATH_CONTACT_TITLE = '//select[@id="pemesan_title"]'
    XPATH_CONTACT_ID_TYPE = '//select[@id="pemesan_tandapengenal"]'

    # Passenger 1
    XPATH_PASSENGER_NAME = '//input[@id="penumpang_nama1"]'
    XPATH_PASSENGER_ID_NUMBER = '//input[@id="penumpang_notandapengenal1"]'
    XPATH_PASSENGER_TITLE = '//select[@id="penumpang_title1"]'
    XPATH_PASSENGER_ID_TYPE = '//select[@id="penumpang_tandapengenal1"]'

    # Actions
    XPATH_CONTINUE_BTN = '//button[@id="bayar"]'
    XPATH_BACK_BTN = '//button[contains(text(),"Kembali")]'

    # Validation errors (Indonesian)
    XPATH_ERROR_NAME = '//li[normalize-space()="Mohon isi Nama"]'
    XPATH_ERROR_ID = '//li[normalize-space()="Mohon isi Nomor Identitas"]'
    XPATH_ERROR_EMAIL = '//li[normalize-space()="Mohon diisi Email"]'
    XPATH_ERROR_PASSENGER_ID = '//li[normalize-space()="Nomor Identitas Wajib Diisi"]'
    XPATH_ANY_ERROR = '//*[contains(@class,"error") or contains(@class,"text-danger")]'

    # Actions

    def fill_contact(self, name: str, phone: str, email: str, id_number: str) -> None:
        """Fill contact person section."""
        self.fill_xpath(self.XPATH_CONTACT_NAME, name)
        self.fill_xpath(self.XPATH_CONTACT_PHONE, phone)
        self.fill_xpath(self.XPATH_CONTACT_EMAIL, email)
        self.fill_xpath(self.XPATH_CONTACT_ID_NUMBER, id_number)

    def fill_passenger(self, name: str, id_number: str) -> None:
        """Fill passenger 1 data."""
        self.fill_xpath(self.XPATH_PASSENGER_NAME, name)
        self.fill_xpath(self.XPATH_PASSENGER_ID_NUMBER, id_number)

    def click_continue(self) -> None:
        """Click Lanjutkan (continue) button."""
        self.click_xpath(self.XPATH_CONTINUE_BTN)
        self.page.wait_for_load_state("load")
        self.human_delay(1000, 2000)

    def fill_and_proceed(self, contact: dict, passenger: dict) -> None:
        """Fill all fields and proceed to next step."""
        self.fill_contact(
            name=contact["name"],
            phone=contact["phone"],
            email=contact["email"],
            id_number=contact["id_number"],
        )
        self.fill_passenger(
            name=passenger["name"],
            id_number=passenger["id_number"],
        )
        self.click_continue()

    # Verifications

    def is_form_displayed(self) -> bool:
        """Check if passenger form is visible."""
        return self.is_visible_xpath(self.XPATH_CONTACT_NAME)

    def has_name_error(self) -> bool:
        return self.is_visible_xpath(self.XPATH_ERROR_NAME)

    def has_id_error(self) -> bool:
        return self.is_visible_xpath(self.XPATH_ERROR_ID)

    def has_email_error(self) -> bool:
        return self.is_visible_xpath(self.XPATH_ERROR_EMAIL)

    def has_passenger_id_error(self) -> bool:
        return self.is_visible_xpath(self.XPATH_ERROR_PASSENGER_ID)

    def has_any_error(self) -> bool:
        self.page.wait_for_timeout(1000)
        return self.count_xpath(self.XPATH_ANY_ERROR) > 0
