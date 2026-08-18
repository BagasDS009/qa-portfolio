"""Test suite for /message endpoints — CRUD operations."""

import allure
import pytest

from api.message_client import MessageClient
from config.settings import Config
from fixtures.message_fixtures import make_message_data


@allure.epic("Restful Booker Platform")
@allure.feature("Message")
class TestMessageCreate:
    """POST /message — create operations (public)."""

    @allure.title("TC-MSG-001: Create message with valid data returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_create_message_valid(self, message_client: MessageClient):
        data = make_message_data()

        with allure.step(f"POST /message (name={data['name']})"):
            response = message_client.create_message(data)

        with allure.step("Verify 200 + success"):
            assert response.status_code == 200
            resp_data = response.json()
            assert resp_data.get("success") is True

    @allure.title("TC-MSG-002: Create message without name returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_message_missing_name(self, message_client_unauth: MessageClient):
        data = make_message_data()
        del data["name"]

        with allure.step("POST /message without name"):
            response = message_client_unauth.create_message(data)

        with allure.step("Verify 400 + validation errors"):
            assert response.status_code == 400
            errors = response.json()
            assert isinstance(errors, list) or "fieldErrors" in str(errors)

    @allure.title("TC-MSG-003: Create message with short phone returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.edge
    def test_create_message_short_phone(self, message_client_unauth: MessageClient):
        data = make_message_data(phone="123")  # Too short (must be 11-21)

        with allure.step("POST /message with phone='123'"):
            response = message_client_unauth.create_message(data)

        with allure.step("Verify 400 + phone validation error"):
            assert response.status_code == 400
            errors = response.json()
            assert isinstance(errors, list)
            assert any("Phone" in e or "phone" in e for e in errors)

    @allure.title("TC-MSG-004: Create message with invalid email returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_message_invalid_email(self, message_client_unauth: MessageClient):
        data = make_message_data(email="not-an-email")

        with allure.step("POST /message with invalid email"):
            response = message_client_unauth.create_message(data)

        with allure.step("Verify 400"):
            assert response.status_code == 400

    @allure.title("TC-MSG-005: Create message without subject returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_message_missing_subject(self, message_client_unauth: MessageClient):
        data = make_message_data()
        del data["subject"]

        with allure.step("POST /message without subject"):
            response = message_client_unauth.create_message(data)

        with allure.step("Verify 400"):
            assert response.status_code == 400


@allure.epic("Restful Booker Platform")
@allure.feature("Message")
class TestMessageRead:
    """GET /message — read operations (public for list, auth for detail)."""

    @allure.title("TC-MSG-006: GET /message returns messages list (public)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_get_messages_list(self, message_client: MessageClient):
        with allure.step("GET /message"):
            response = message_client.get_messages()

        with allure.step("Verify 200 + messages array"):
            assert response.status_code == 200
            data = response.json()
            assert "messages" in data
            assert isinstance(data["messages"], list)

    @allure.title("TC-MSG-007: GET /message/{id} returns single message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_get_message_by_id(self, message_client: MessageClient, created_message: dict):
        msg_id = created_message["messageid"]

        with allure.step(f"GET /message/{msg_id}"):
            response = message_client.get_message(msg_id)

        with allure.step("Verify 200 + correct message"):
            assert response.status_code == 200
            data = response.json()
            assert data["messageid"] == msg_id

    @allure.title("TC-MSG-008: GET /message is accessible without auth (public list)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.wave1
    def test_get_messages_public(self, message_client_unauth: MessageClient):
        with allure.step("GET /message without auth"):
            response = message_client_unauth.get_messages()

        with allure.step("Verify 200 (message list is public)"):
            assert response.status_code == 200
            data = response.json()
            assert "messages" in data


@allure.epic("Restful Booker Platform")
@allure.feature("Message")
class TestMessageDelete:
    """DELETE /message/{id} — delete operations (requires auth)."""

    @allure.title("TC-MSG-009: Delete message returns 202")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_delete_message_valid(self, message_client: MessageClient):
        # Create a message for deletion
        data = make_message_data()
        create_resp = message_client.create_message(data)
        assert create_resp.status_code == 200

        # Find the message in the list
        before = message_client.get_messages().json().get("messages", [])
        # Get the latest message matching our name
        matching = [m for m in before if m.get("name") == data["name"]]
        assert len(matching) > 0, "Created message not found in list"
        msg_id = matching[-1]["id"]

        with allure.step(f"DELETE /message/{msg_id}"):
            response = message_client.delete_message(msg_id)

        with allure.step("Verify 202"):
            assert response.status_code == 202

    @allure.title("TC-MSG-010: Delete message without auth returns 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_delete_message_no_auth(self, message_client_unauth: MessageClient, created_message: dict):
        msg_id = created_message["messageid"]

        with allure.step(f"DELETE /message/{msg_id} without auth"):
            response = message_client_unauth.delete_message(msg_id)

        with allure.step("Verify 403"):
            assert response.status_code == 403


@allure.epic("Restful Booker Platform")
@allure.feature("Message")
class TestMessageContract:
    """Schema/contract validation for message responses."""

    @allure.title("TC-MSG-011: Message object has required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_message_schema(self, message_client: MessageClient, created_message: dict):
        msg_id = created_message["messageid"]

        with allure.step(f"GET /message/{msg_id}"):
            response = message_client.get_message(msg_id)

        with allure.step("Verify message schema"):
            assert response.status_code == 200
            msg = response.json()
            required_fields = {"messageid", "name", "email", "phone", "subject", "description"}
            assert required_fields.issubset(set(msg.keys()))
            assert isinstance(msg["messageid"], int)
            assert isinstance(msg["name"], str)
            assert isinstance(msg["email"], str)

    @allure.title("TC-MSG-012: Validation errors return as array")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_validation_error_format(self, message_client_unauth: MessageClient):
        with allure.step("POST /message with empty body"):
            response = message_client_unauth.create_message({})

        with allure.step("Verify error is array of strings"):
            assert response.status_code == 400
            errors = response.json()
            assert isinstance(errors, list)
            for err in errors:
                assert isinstance(err, str)
