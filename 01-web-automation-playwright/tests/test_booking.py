"""
TC-004: Select Train
TC-005: Change Train Selection
TC-006: Complete Booking
Test cases for end-to-end train booking flow on KAI.
"""

import allure
import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from pages.seat_page import SeatPage
from pages.payment_page import PaymentPage
from pages.confirmation_page import ConfirmationPage
from tests.test_data import VALID_SEARCH, CONTACT_PERSON, PASSENGER_1


@allure.epic("KAI Booking")
@allure.feature("Booking Flow")
class TestBookingFlow:
    """Test suite for train booking/checkout flow."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup: Navigate to home page (no login needed)."""
        self.home_page = HomePage(page)
        self.train_list_page = TrainListPage(page)
        self.passenger_page = PassengerPage(page)
        self.seat_page = SeatPage(page)
        self.payment_page = PaymentPage(page)
        self.confirmation_page = ConfirmationPage(page)

    def _search_train(self):
        """Helper: Search train with valid data."""
        self.home_page.navigate_to_home()
        self.home_page.search_train(
            origin=VALID_SEARCH["origin"],
            destination=VALID_SEARCH["destination"],
            tgl=VALID_SEARCH["tgl"],
            adults=VALID_SEARCH["adults"],
        )
        self.train_list_page.wait_for_results()

    def _fill_passenger_data(self):
        """Helper: Fill passenger form with valid data."""
        self.passenger_page.fill_contact_person(
            name=CONTACT_PERSON["name"],
            phone=CONTACT_PERSON["phone"],
            email=CONTACT_PERSON["email"],
        )
        self.passenger_page.fill_passenger_info(
            name=PASSENGER_1["name"],
            id_number=PASSENGER_1["id_number"],
        )
        self.passenger_page.click_continue()

    @allure.story("Select Train")
    @allure.title("TC-004: Select train from search results")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_select_train(self, page):
        """Verify user can select a train from search results."""
        with allure.step("Search for available trains"):
            self._search_train()

        with allure.step("Verify trains are available"):
            assert self.train_list_page.get_available_trains_count() > 0, (
                "No trains available to select"
            )

        with allure.step("Select first available train"):
            train_name = VALID_SEARCH["train_name"]
            allure.attach(train_name, name="Selected Train", attachment_type=allure.attachment_type.TEXT)
            self.train_list_page.select_train_by_name(train_name)

        with allure.step("Verify passenger form is displayed"):
            assert self.passenger_page.is_passenger_form_displayed(), (
                f"Passenger form not shown after selecting: {train_name}"
            )

    @allure.story("Change Selection")
    @allure.title("TC-005: Change train selection")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_different_train(self, page):
        """Verify user can go back and select a different train."""
        with allure.step("Search for available trains"):
            self._search_train()

        trains_count = self.train_list_page.get_available_trains_count()

        if trains_count >= 2:
            with allure.step("Select first train then go back"):
                self.train_list_page.select_train_by_name(VALID_SEARCH["train_name"])
                self.passenger_page.click_back()

            with allure.step("Select second train"):
                self.train_list_page.wait_for_results()
                second_train = self.train_list_page.get_train_name(1)
                self.train_list_page.select_train_by_index(1)

            with allure.step("Verify passenger form for new selection"):
                assert self.passenger_page.is_passenger_form_displayed(), (
                    f"Passenger form not shown after selecting: {second_train}"
                )
        else:
            pytest.skip("Only 1 train available, cannot test change selection")

    @allure.story("Complete Booking")
    @allure.title("TC-006: Complete end-to-end booking flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_complete_booking_flow(self, page):
        """Verify full flow: Search → Select → Passenger → Seat → Payment."""
        with allure.step("Step 1: Search for trains"):
            self._search_train()

        with allure.step("Step 2: Select train by name"):
            self.train_list_page.select_train_by_name(VALID_SEARCH["train_name"])

        with allure.step("Step 3: Fill passenger data"):
            self._fill_passenger_data()

        with allure.step("Step 4: Handle seat selection"):
            if self.seat_page.is_seat_map_displayed():
                self.seat_page.select_first_available_seat()
                self.seat_page.confirm_seat()

        with allure.step("Step 5: Verify payment page"):
            assert self.payment_page.is_payment_page_displayed(), (
                "Payment page not displayed after completing booking flow"
            )
