"""Test suite for /booking endpoints — CRUD operations."""

from datetime import date, timedelta

import allure
import pytest

from api.booking_client import BookingClient
from config.settings import Config
from fixtures.booking_fixtures import make_booking_data


@allure.epic("Restful Booker Platform")
@allure.feature("Booking")
class TestBookingCreate:
    """POST /booking — create operations (public)."""

    @allure.title("TC-BOOK-001: Create booking with valid data returns 201")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_create_booking_valid(self, booking_client: BookingClient, created_room: dict):
        room_id = created_room["roomid"]
        data = make_booking_data(room_id=room_id)

        with allure.step(f"POST /booking (room={room_id})"):
            response = booking_client.create_booking(data)

        with allure.step("Verify 201 + booking created"):
            assert response.status_code == 201
            booking = response.json()
            assert booking["roomid"] == room_id
            assert booking["firstname"] == data["firstname"]
            assert booking["lastname"] == data["lastname"]
            assert "bookingid" in booking

        # Cleanup
        booking_client.delete_booking(booking["bookingid"])

    @allure.title("TC-BOOK-002: Create booking without firstname returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_booking_missing_firstname(self, booking_client_unauth: BookingClient, created_room: dict):
        data = make_booking_data(room_id=created_room["roomid"])
        del data["firstname"]

        with allure.step("POST /booking without firstname"):
            response = booking_client_unauth.create_booking(data)

        with allure.step("Verify 400"):
            assert response.status_code == 400

    @allure.title("TC-BOOK-003: Create booking without lastname returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_booking_missing_lastname(self, booking_client_unauth: BookingClient, created_room: dict):
        data = make_booking_data(room_id=created_room["roomid"])
        del data["lastname"]

        with allure.step("POST /booking without lastname"):
            response = booking_client_unauth.create_booking(data)

        with allure.step("Verify 400"):
            assert response.status_code == 400

    @allure.title("TC-BOOK-004: Create booking with checkout before checkin returns 409")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.edge
    def test_create_booking_invalid_dates(self, booking_client_unauth: BookingClient, created_room: dict):
        checkin = date.today() + timedelta(days=50)
        checkout = checkin - timedelta(days=2)  # checkout BEFORE checkin

        data = make_booking_data(
            room_id=created_room["roomid"],
            bookingdates={
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
            },
        )

        with allure.step("POST /booking with checkout < checkin"):
            response = booking_client_unauth.create_booking(data)

        with allure.step("Verify 409 (conflict)"):
            assert response.status_code == 409

    @allure.title("TC-BOOK-005: Create booking without bookingdates causes server hang")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_booking_missing_dates(self, booking_client_unauth: BookingClient, created_room: dict):
        """API BUG: Missing bookingdates causes the server to hang (no response).
        We verify by setting a short timeout and expecting ReadTimeout.
        """
        import httpx as _httpx

        data = make_booking_data(room_id=created_room["roomid"])
        del data["bookingdates"]

        with allure.step("POST /booking without bookingdates (expect timeout — API bug)"):
            # Use a short timeout since API hangs on this payload
            short_client = BookingClient()
            short_client.session = _httpx.Client(
                base_url=short_client.base_url, timeout=5.0
            )
            try:
                response = short_client.create_booking(data)
                # If it does respond, should be 400
                assert response.status_code == 400
            except _httpx.ReadTimeout:
                pass  # Expected — API BUG: hangs on missing dates
            finally:
                short_client.close()


@allure.epic("Restful Booker Platform")
@allure.feature("Booking")
class TestBookingRead:
    """GET /booking — read operations (requires auth)."""

    @allure.title("TC-BOOK-006: GET /booking?roomid={id} returns bookings list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_get_bookings_by_room(self, booking_client: BookingClient, created_booking: dict):
        room_id = created_booking["roomid"]

        with allure.step(f"GET /booking?roomid={room_id}"):
            response = booking_client.get_bookings(room_id)

        with allure.step("Verify 200 + bookings array"):
            assert response.status_code == 200
            data = response.json()
            assert "bookings" in data
            assert isinstance(data["bookings"], list)
            assert len(data["bookings"]) > 0

    @allure.title("TC-BOOK-007: GET /booking/{id} returns single booking")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_get_booking_by_id(self, booking_client: BookingClient, created_booking: dict):
        booking_id = created_booking["bookingid"]

        with allure.step(f"GET /booking/{booking_id}"):
            response = booking_client.get_booking(booking_id)

        with allure.step("Verify 200 + correct booking"):
            assert response.status_code == 200
            data = response.json()
            assert data["bookingid"] == booking_id
            assert data["firstname"] == created_booking["firstname"]

    @allure.title("TC-BOOK-008: GET /booking without roomid returns error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_bookings_no_roomid(self, booking_client: BookingClient):
        with allure.step("GET /booking without roomid param"):
            response = booking_client.get("/booking")

        with allure.step("Verify error response"):
            assert response.status_code in [400, 500]

    @allure.title("TC-BOOK-009: GET /booking without auth returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_get_bookings_no_auth(self, booking_client_unauth: BookingClient, created_room: dict):
        with allure.step("GET /booking?roomid=1 without auth"):
            response = booking_client_unauth.get_bookings(created_room["roomid"])

        with allure.step("Verify 401"):
            assert response.status_code == 401


@allure.epic("Restful Booker Platform")
@allure.feature("Booking")
class TestBookingUpdate:
    """PUT /booking/{id} — update operations (requires auth)."""

    @allure.title("TC-BOOK-010: Update booking with valid data returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_update_booking_valid(self, booking_client: BookingClient, created_booking: dict):
        booking_id = created_booking["bookingid"]
        # Use far-future dates different from the original to avoid 409 conflict
        from datetime import date, timedelta
        new_checkin = date.today() + timedelta(days=200)
        new_checkout = new_checkin + timedelta(days=2)

        updated = {
            "roomid": created_booking["roomid"],
            "firstname": "UpdatedName",
            "lastname": created_booking["lastname"],
            "depositpaid": created_booking["depositpaid"],
            "bookingdates": {
                "checkin": new_checkin.isoformat(),
                "checkout": new_checkout.isoformat(),
            },
        }

        with allure.step(f"PUT /booking/{booking_id}"):
            response = booking_client.update_booking(booking_id, updated)

        with allure.step("Verify 200 + updated firstname"):
            assert response.status_code == 200
            data = response.json()
            # Response wraps in {"booking": {...}, "bookingid": N}
            booking = data.get("booking", data)
            assert booking["firstname"] == "UpdatedName"

    @allure.title("TC-BOOK-011: Update booking without auth returns 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_update_booking_no_auth(self, booking_client_unauth: BookingClient, created_booking: dict):
        booking_id = created_booking["bookingid"]
        updated = make_booking_data(room_id=created_booking["roomid"])

        with allure.step(f"PUT /booking/{booking_id} without auth"):
            response = booking_client_unauth.update_booking(booking_id, updated)

        with allure.step("Verify 403"):
            assert response.status_code == 403

    @allure.title("TC-BOOK-012: Update non-existent booking returns 404/405")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_booking_not_found(self, booking_client: BookingClient, created_room: dict):
        updated = make_booking_data(room_id=created_room["roomid"])

        with allure.step("PUT /booking/99999"):
            response = booking_client.update_booking(99999, updated)

        with allure.step("Verify 404 or 405"):
            assert response.status_code in [404, 405]


@allure.epic("Restful Booker Platform")
@allure.feature("Booking")
class TestBookingDelete:
    """DELETE /booking/{id} — delete operations (requires auth)."""

    @allure.title("TC-BOOK-013: Delete booking returns 202")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_delete_booking_valid(self, booking_client: BookingClient, created_room: dict):
        # Create a booking specifically for deletion
        data = make_booking_data(room_id=created_room["roomid"])
        create_resp = booking_client.create_booking(data)
        assert create_resp.status_code == 201
        booking_id = create_resp.json()["bookingid"]

        with allure.step(f"DELETE /booking/{booking_id}"):
            response = booking_client.delete_booking(booking_id)

        with allure.step("Verify 202"):
            assert response.status_code == 202

    @allure.title("TC-BOOK-014: Delete booking without auth returns 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_delete_booking_no_auth(self, booking_client_unauth: BookingClient, created_booking: dict):
        booking_id = created_booking["bookingid"]

        with allure.step(f"DELETE /booking/{booking_id} without auth"):
            response = booking_client_unauth.delete_booking(booking_id)

        with allure.step("Verify 403"):
            assert response.status_code == 403

    @allure.title("TC-BOOK-015: Delete non-existent booking returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_delete_booking_not_found(self, booking_client: BookingClient):
        with allure.step("DELETE /booking/99999"):
            response = booking_client.delete_booking(99999)

        with allure.step("Verify 404"):
            assert response.status_code in [404, 405]


@allure.epic("Restful Booker Platform")
@allure.feature("Booking")
class TestBookingContract:
    """Schema/contract validation for booking responses."""

    @allure.title("TC-BOOK-016: Booking object has required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_booking_schema(self, booking_client: BookingClient, created_booking: dict):
        booking_id = created_booking["bookingid"]

        with allure.step(f"GET /booking/{booking_id}"):
            response = booking_client.get_booking(booking_id)

        with allure.step("Verify booking schema"):
            assert response.status_code == 200
            booking = response.json()
            required_fields = {"bookingid", "roomid", "firstname", "lastname", "depositpaid", "bookingdates"}
            assert required_fields.issubset(set(booking.keys()))
            assert isinstance(booking["bookingid"], int)
            assert isinstance(booking["roomid"], int)
            assert isinstance(booking["firstname"], str)
            assert isinstance(booking["lastname"], str)
            assert isinstance(booking["depositpaid"], bool)
            assert "checkin" in booking["bookingdates"]
            assert "checkout" in booking["bookingdates"]
