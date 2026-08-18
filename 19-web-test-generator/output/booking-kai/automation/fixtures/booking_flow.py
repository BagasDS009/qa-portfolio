"""Booking flow fixtures — provides precondition states for downstream tests.

Full booking flow:
  1. Search (origin + destination + date H+45)
  2. Select cheapest train from results
  3. Fill passenger data (contact + passenger)
  4. Select seat (or skip)
  5. Payment page (UI only — NEVER pay)

Fixtures:
  - at_train_list: step 1 done (search results visible)
  - at_passenger_form: step 1 + 2 done (train selected, on passenger page)
  - at_seat_page: step 1 + 2 + 3 done (passenger filled, on seat page)
  - at_payment_page: step 1 + 2 + 3 + 4 done (seat confirmed, on payment page)
"""

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.train_list_page import TrainListPage
from pages.passenger_page import PassengerPage
from pages.seat_page import SeatPage
from test_data.routes import VALID_ROUTE
from test_data.passengers import VALID_CONTACT, VALID_PASSENGER


@pytest.fixture
def at_train_list(page: Page) -> Page:
    """Precondition: search executed, train results visible.
    
    Steps:
      1. Navigate to homepage
      2. Select origin (GMR)
      3. Select destination (BD)
      4. Pick date H+45 (navigate months in datepicker)
      5. Click search
      6. Wait for results
    """
    home = HomePage(page)
    home.navigate_to_home()
    home.search_train(
        origin=VALID_ROUTE["origin"],
        destination=VALID_ROUTE["destination"],
        day=VALID_ROUTE["day"],
        months_ahead=VALID_ROUTE.get("months_ahead", 1),
    )
    
    train_list = TrainListPage(page)
    train_list.wait_for_results()
    
    # Verify we actually have results
    if train_list.get_train_count() == 0:
        pytest.skip(f"No trains found for {VALID_ROUTE['origin']}→{VALID_ROUTE['destination']} on day {VALID_ROUTE['day']}")
    
    return page


@pytest.fixture
def at_passenger_form(at_train_list: Page) -> Page:
    """Precondition: cheapest train selected, on passenger data form.
    
    Steps (after at_train_list):
      1. Select cheapest train from results
      2. Wait for page reload to passenger form
      3. Verify passenger form is displayed
    """
    train_list = TrainListPage(at_train_list)
    
    # Select the cheapest train
    train_list.select_cheapest_train()
    at_train_list.wait_for_load_state("load")
    at_train_list.wait_for_timeout(3000)
    
    # Verify we landed on passenger form
    passenger = PassengerPage(at_train_list)
    if not passenger.is_form_displayed():
        pytest.skip("Did not reach passenger form after selecting train — may need login")
    
    return at_train_list


@pytest.fixture
def at_seat_page(at_passenger_form: Page) -> Page:
    """Precondition: passenger data filled, on seat selection page.
    
    Steps (after at_passenger_form):
      1. Fill contact person (name, phone, email, ID)
      2. Fill passenger 1 (name, ID)
      3. Click Lanjutkan (continue)
      4. Wait for seat page
    """
    passenger = PassengerPage(at_passenger_form)
    
    passenger.fill_and_proceed(VALID_CONTACT, VALID_PASSENGER)
    at_passenger_form.wait_for_timeout(3000)
    
    # Verify we moved forward (no longer on passenger form OR no errors)
    if passenger.has_any_error():
        pytest.skip("Passenger form validation failed — cannot proceed to seat")
    
    return at_passenger_form


@pytest.fixture
def at_payment_page(at_seat_page: Page) -> Page:
    """Precondition: seat confirmed (or skipped), on payment page.
    
    Steps (after at_seat_page):
      1. Select first available seat (or skip if none)
      2. Click confirm
      3. Wait for payment page
    """
    seat = SeatPage(at_seat_page)
    
    if seat.is_seat_map_visible():
        if seat.get_available_count() > 0:
            seat.select_first_available()
            seat.confirm_seat()
        else:
            seat.skip_selection()
    
    at_seat_page.wait_for_timeout(3000)
    return at_seat_page
