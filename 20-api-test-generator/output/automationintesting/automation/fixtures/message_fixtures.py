"""Message fixtures — provides MessageClient and test data factory."""

import pytest
from faker import Faker

from api.message_client import MessageClient

fake = Faker()


def make_message_data(**overrides) -> dict:
    """Generate valid message data with optional overrides."""
    data = {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.numerify("0##########"),  # 11 digits
        "subject": fake.sentence(nb_words=5),
        "description": fake.paragraph(nb_sentences=3),
    }
    data.update(overrides)
    return data


@pytest.fixture()
def message_client(admin_token: str) -> MessageClient:
    """Authenticated MessageClient."""
    client = MessageClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def message_client_unauth() -> MessageClient:
    """Unauthenticated MessageClient."""
    client = MessageClient()
    yield client
    client.close()


@pytest.fixture()
def created_message(message_client: MessageClient) -> dict:
    """Create a message and yield its data. Cleanup after test.

    API returns 200 {"success":true} — so we GET /message list before/after
    to identify the newly created message by diff.
    """
    # Get messages before
    before_resp = message_client.get_messages()
    before_ids = {m["id"] for m in before_resp.json().get("messages", [])}

    # Create message
    data = make_message_data()
    response = message_client.create_message(data)
    assert response.status_code == 200, f"Message creation failed: {response.text}"

    # Get messages after to find the new one
    after_resp = message_client.get_messages()
    after_msgs = after_resp.json().get("messages", [])
    new_msgs = [m for m in after_msgs if m["id"] not in before_ids]
    assert len(new_msgs) > 0, "Message was not created (not found in list)"

    # GET full message detail by ID
    msg_detail_resp = message_client.get_message(new_msgs[0]["id"])
    assert msg_detail_resp.status_code == 200
    msg = msg_detail_resp.json()

    yield msg

    # Teardown
    message_client.delete_message(msg["messageid"])
