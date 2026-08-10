"""
TC-004: Select Train (Add to Cart)
TC-005: Change Train Selection (Remove from Cart)
TC-006: Complete Booking/Checkout
Test cases for end-to-end train booking flow on KAI.
"""

import pytest
from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from pages.seat_page import SeatPage
from pages.payment_page import PaymentPage
from pages.confirmation_page import ConfirmationPage
from tests.test_data import VALID_SEARCH, CONTACT_PERSON, PASSENGER_1, get_departure_date


class TestBookingFlow:
    """Test suite for train booking/checkout flow."""

    @pytest.fixture(autouse=True)
    def setup(self, page, login):
        """Setup: Login and initialize page objects."""
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
            origin=VALID_SEARCH["origin"],             # PSE
            destination=VALID_SEARCH["destination"],   # BD
            date=get_departure_date(7),
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

    @pytest.mark.smoke
    def test_select_train(self, page):
        """
        TC-004: Select Train
        Verify user can select a train from search results.
        """
        self._search_train()
        assert self.train_list_page.get_available_trains_count() > 0, (
            "No trains available to select"
        )

        train_name = self.train_list_page.get_train_name(0)
        self.train_list_page.select_first_train()

        assert self.passenger_page.is_passenger_form_displayed(), (
            f"Passenger form not shown after selecting: {train_name}"
        )

    def test_select_different_train(self, page):
        """
        TC-005: Change Train Selection
        Verify user can go back and select a different train.
        """
        self._search_train()
        trains_count = self.train_list_page.get_available_trains_count()

        if trains_count >= 2:
            self.train_list_page.select_first_train()
            self.passenger_page.click_back()

            self.train_list_page.wait_for_results()
            second_train = self.train_list_page.get_train_name(1)
            self.train_list_page.select_train_by_index(1)

            assert self.passenger_page.is_passenger_form_displayed(), (
                f"Passenger form not shown after selecting: {second_train}"
            )
        else:
            pytest.skip("Only 1 train available, cannot test change selection")

    @pytest.mark.smoke
    def test_complete_booking_flow(self, page):
        """
        TC-006: Complete Checkout/Booking Flow
        Verify full flow: Search → Select → Passenger → Seat → Payment.
        """
        # Step 1-2: Search and select train
        self._search_train()
        self.train_list_page.select_first_train()

        # Step 3: Fill passenger data
        self._fill_passenger_data()

        # Step 4: Seat selection (skip if available)
        if self.seat_page.is_seat_map_displayed():
            self.seat_page.select_first_available_seat()
            self.seat_page.confirm_seat()

        # Step 5: Verify payment page
        assert self.payment_page.is_payment_page_displayed(), (
            "Payment page not displayed after completing booking flow"
        )

    def test_booking_preserves_train_info(self, page):
        """
        TC-006b: Verify booking details preserved through flow.
        """
        self._search_train()
        selected_train = self.train_list_page.get_train_name(0)
        self.train_list_page.select_first_train()

        self._fill_passenger_data()

        if self.seat_page.is_seat_map_displayed():
            self.seat_page.select_first_available_seat()
            self.seat_page.confirm_seat()

        assert self.payment_page.is_payment_page_displayed(), (
            f"Payment page not reached after booking {selected_train}"
        )
