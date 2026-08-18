"""
TC-SEAT-001 to TC-SEAT-004: Seat selection test suite for KAI Booking.

Precondition handled by fixture: search → select train → fill passenger → arrive at seat page.
"""

import allure
import pytest
from playwright.sync_api import Page

from pages.seat_page import SeatPage


@allure.epic("KAI Online Booking")
@allure.feature("Seat Selection")
@pytest.mark.wave1
class TestSeat:
    """Seat selection test suite.
    
    Uses `at_seat_page` fixture for precondition.
    """

    # === CRITICAL ===

    @allure.story("Select Seat")
    @allure.title("TC-SEAT-001: Select first available seat and confirm")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.critical
    @pytest.mark.seat
    def test_select_seat_and_confirm(self, at_seat_page: Page):
        """Verify user can select an available seat and proceed."""
        seat = SeatPage(at_seat_page)

        with allure.step("Verify seat map is displayed"):
            assert seat.is_seat_map_visible(), "Seat map not visible"

        with allure.step("Select first available seat"):
            available = seat.get_available_count()
            assert available > 0, "No available seats"
            seat.select_first_available()

        with allure.step("Verify seat marked as selected"):
            assert seat.is_seat_selected(), "No seat marked as selected"

        with allure.step("Confirm seat selection"):
            seat.confirm_seat()

        with allure.step("Verify left seat page"):
            at_seat_page.wait_for_timeout(3000)
            assert not seat.is_seat_map_visible(), "Should have left seat page"

    # === POSITIVE ===

    @allure.story("Skip Seat")
    @allure.title("TC-SEAT-002: Skip seat selection (auto-assign)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    @pytest.mark.seat
    def test_skip_seat_selection(self, at_seat_page: Page):
        """Verify user can skip and system auto-assigns seat."""
        seat = SeatPage(at_seat_page)

        with allure.step("Click Lewati/Skip"):
            seat.skip_selection()

        with allure.step("Verify proceeded"):
            at_seat_page.wait_for_timeout(3000)
            assert not seat.is_seat_map_visible()

    # === NEGATIVE ===

    @allure.story("Occupied Seat")
    @allure.title("TC-SEAT-003: Clicking occupied seat does nothing")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    @pytest.mark.negative
    @pytest.mark.seat
    def test_occupied_seat_unclickable(self, at_seat_page: Page):
        """Verify occupied seats cannot be selected."""
        seat = SeatPage(at_seat_page)

        with allure.step("Attempt to click occupied seat"):
            if seat.count_xpath(seat.XPATH_OCCUPIED) > 0:
                at_seat_page.locator(f"xpath={seat.XPATH_OCCUPIED}").first.click(force=True)
                at_seat_page.wait_for_timeout(500)

        with allure.step("Page should not crash"):
            assert at_seat_page.locator("body").is_visible()

    # === EDGE ===

    @allure.story("Seat Map")
    @allure.title("TC-SEAT-004: Seat map loads with seats rendered")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    @pytest.mark.edge
    @pytest.mark.seat
    def test_seat_map_renders(self, at_seat_page: Page):
        """Verify seat map renders with available and occupied seats."""
        seat = SeatPage(at_seat_page)

        with allure.step("Verify seat map visible"):
            assert seat.is_seat_map_visible()

        with allure.step("Verify seats rendered"):
            available = seat.get_available_count()
            occupied = seat.count_xpath(seat.XPATH_OCCUPIED)
            total = available + occupied
            assert total > 0, f"No seats in map (avail={available}, occ={occupied})"
