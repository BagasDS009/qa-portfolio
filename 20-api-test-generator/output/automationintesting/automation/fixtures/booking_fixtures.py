"""Booking fixtures — provides BookingClient and test data factory."""

from datetime import date, timedelta

import pytest
from faker import Faker

from api.booking_client import BookingClient

fake = Faker()


def make_booking_data(room_id: int, **overrides) -> dict:
    """Generate valid booking data for a given room ID."""
    checkin = date.today() + timedelta(days=fake.random_int(min=30, max=60))
    checkout = checkin + timedelta(days=fake.random_int(min=1, max=5))

    data = {
        "roomid": room_id,
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
    }
    data.update(overrides)
    return data


@pytest.fixture()
def booking_client(admin_token: str) -> BookingClient:
    """Authenticated BookingClient."""
    client = BookingClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def booking_client_unauth() -> BookingClient:
    """Unauthenticated BookingClient."""
    client = BookingClient()
    yield client
    client.close()


@pytest.fixture()
def created_booking(booking_client: BookingClient, created_room: dict) -> dict:
    """Create a booking on a fresh room and yield. Cleanup after test."""
    data = make_booking_data(room_id=created_room["roomid"])
    response = booking_client.create_booking(data)
    assert response.status_code == 201, f"Booking creation failed: {response.text}"
    booking = response.json()
    yield booking
    # Teardown
    booking_client.delete_booking(booking["bookingid"])
