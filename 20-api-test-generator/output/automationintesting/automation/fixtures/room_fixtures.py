"""Room fixtures — provides RoomClient and test data factory."""

import pytest
from faker import Faker

from api.room_client import RoomClient

fake = Faker()


def make_room_data(**overrides) -> dict:
    """Generate valid room data with optional overrides."""
    data = {
        "roomName": str(fake.random_int(min=100, max=999)),
        "type": fake.random_element(["Single", "Double", "Suite", "Family"]),
        "accessible": fake.boolean(),
        "roomPrice": fake.random_int(min=50, max=500),
        "description": fake.sentence(nb_words=10),
        "features": fake.random_elements(
            ["TV", "WiFi", "Safe", "Mini Bar", "Views", "Radio"],
            unique=True,
            length=fake.random_int(min=1, max=4),
        ),
        "image": f"/images/room{fake.random_int(min=1, max=5)}.jpg",
    }
    data.update(overrides)
    return data


@pytest.fixture()
def room_client(admin_token: str) -> RoomClient:
    """Authenticated RoomClient."""
    client = RoomClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def room_client_unauth() -> RoomClient:
    """Unauthenticated RoomClient."""
    client = RoomClient()
    yield client
    client.close()


@pytest.fixture()
def created_room(room_client: RoomClient) -> dict:
    """Create a room and yield its data. Cleanup after test.

    API returns 200 {"success":true} — so we GET /room list before/after
    to identify the newly created room by diff.
    """
    # Get rooms before
    before_resp = room_client.get_rooms()
    before_ids = {r["roomid"] for r in before_resp.json().get("rooms", [])}

    # Create room
    data = make_room_data()
    response = room_client.create_room(data)
    assert response.status_code == 200, f"Room creation failed: {response.text}"

    # Get rooms after to find the new one
    after_resp = room_client.get_rooms()
    after_rooms = after_resp.json().get("rooms", [])
    new_rooms = [r for r in after_rooms if r["roomid"] not in before_ids]
    assert len(new_rooms) > 0, "Room was not created (not found in list)"

    room = new_rooms[0]
    yield room

    # Teardown — delete the room
    room_client.delete_room(room["roomid"])
