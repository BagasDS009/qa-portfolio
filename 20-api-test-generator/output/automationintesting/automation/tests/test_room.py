"""Test suite for /room endpoints — CRUD operations."""

import allure
import pytest

from api.room_client import RoomClient
from config.settings import Config
from fixtures.room_fixtures import make_room_data


@allure.epic("Restful Booker Platform")
@allure.feature("Room")
class TestRoomRead:
    """GET /room — list and get operations (public)."""

    @allure.title("TC-ROOM-001: GET /room returns list of rooms")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_get_rooms_list(self, room_client: RoomClient):
        with allure.step("GET /room"):
            response = room_client.get_rooms()

        with allure.step("Verify 200 + rooms array"):
            assert response.status_code == 200
            data = response.json()
            assert "rooms" in data
            assert isinstance(data["rooms"], list)
            assert len(data["rooms"]) > 0

    @allure.title("TC-ROOM-002: GET /room/{id} returns single room")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_get_room_by_id(self, room_client: RoomClient, created_room: dict):
        room_id = created_room["roomid"]

        with allure.step(f"GET /room/{room_id}"):
            response = room_client.get_room(room_id)

        with allure.step("Verify 200 + correct room"):
            assert response.status_code == 200
            data = response.json()
            assert data["roomid"] == room_id
            assert data["roomName"] == created_room["roomName"]

    @allure.title("TC-ROOM-003: GET /room/{id} with invalid ID returns 500")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_room_invalid_id(self, room_client: RoomClient):
        with allure.step("GET /room/99999"):
            response = room_client.get_room(99999)

        with allure.step("Verify 500 (API returns 500 for non-existent room)"):
            assert response.status_code == 500

    @allure.title("TC-ROOM-004: GET /room response time < 2s")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_rooms_response_time(self, room_client: RoomClient):
        import time

        with allure.step("GET /room and measure time"):
            start = time.time()
            response = room_client.get_rooms()
            elapsed_ms = (time.time() - start) * 1000

        with allure.step(f"Verify response time {elapsed_ms:.0f}ms < {Config.RESPONSE_TIME_BUDGET_MS}ms"):
            assert response.status_code == 200
            assert elapsed_ms < Config.RESPONSE_TIME_BUDGET_MS


@allure.epic("Restful Booker Platform")
@allure.feature("Room")
class TestRoomCreate:
    """POST /room — create operations (requires auth)."""

    @allure.title("TC-ROOM-005: Create room with valid data returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_create_room_valid(self, room_client: RoomClient):
        data = make_room_data()

        # Get rooms before
        before = room_client.get_rooms().json().get("rooms", [])
        before_ids = {r["roomid"] for r in before}

        with allure.step(f"POST /room (name={data['roomName']})"):
            response = room_client.create_room(data)

        with allure.step("Verify 200 + room created"):
            assert response.status_code == 200
            resp_data = response.json()
            assert resp_data.get("success") is True

        # Verify room exists in list
        with allure.step("Verify room appears in GET /room"):
            after = room_client.get_rooms().json().get("rooms", [])
            new_rooms = [r for r in after if r["roomid"] not in before_ids]
            assert len(new_rooms) > 0
            assert new_rooms[0]["roomName"] == data["roomName"]

        # Cleanup
        room_client.delete_room(new_rooms[0]["roomid"])

    @allure.title("TC-ROOM-006: Create room without auth returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_create_room_no_auth(self, room_client_unauth: RoomClient):
        data = make_room_data()

        with allure.step("POST /room without auth"):
            response = room_client_unauth.create_room(data)

        with allure.step("Verify 401"):
            assert response.status_code == 401

    @allure.title("TC-ROOM-007: Create room without roomName returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_room_missing_name(self, room_client: RoomClient):
        data = make_room_data()
        del data["roomName"]

        with allure.step("POST /room without roomName"):
            response = room_client.create_room(data)

        with allure.step("Verify 400 (validation error)"):
            assert response.status_code == 400

    @allure.title("TC-ROOM-008: Create room with invalid type returns 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_room_invalid_type(self, room_client: RoomClient):
        data = make_room_data(type="Penthouse")

        with allure.step("POST /room with type='Penthouse'"):
            response = room_client.create_room(data)

        with allure.step("Verify 400"):
            assert response.status_code == 400


@allure.epic("Restful Booker Platform")
@allure.feature("Room")
class TestRoomUpdate:
    """PUT /room/{id} — update operations (requires auth)."""

    @allure.title("TC-ROOM-009: Update room with valid data returns 202")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_update_room_valid(self, room_client: RoomClient, created_room: dict):
        room_id = created_room["roomid"]
        updated_data = make_room_data(roomName="Updated-999")

        with allure.step(f"PUT /room/{room_id}"):
            response = room_client.update_room(room_id, updated_data)

        with allure.step("Verify 202 + accepted"):
            assert response.status_code == 202

    @allure.title("TC-ROOM-010: Update room without auth returns 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_update_room_no_auth(self, room_client_unauth: RoomClient, created_room: dict):
        room_id = created_room["roomid"]
        updated_data = make_room_data()

        with allure.step(f"PUT /room/{room_id} without auth"):
            response = room_client_unauth.update_room(room_id, updated_data)

        with allure.step("Verify 403"):
            assert response.status_code == 403

    @allure.title("TC-ROOM-011: Update non-existent room returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_room_not_found(self, room_client: RoomClient):
        updated_data = make_room_data()

        with allure.step("PUT /room/99999"):
            response = room_client.update_room(99999, updated_data)

        with allure.step("Verify 404"):
            assert response.status_code == 404


@allure.epic("Restful Booker Platform")
@allure.feature("Room")
class TestRoomDelete:
    """DELETE /room/{id} — delete operations (requires auth)."""

    @allure.title("TC-ROOM-012: Delete room returns 202")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_delete_room_valid(self, room_client: RoomClient):
        # Create a room specifically for deletion
        data = make_room_data()
        before = room_client.get_rooms().json().get("rooms", [])
        before_ids = {r["roomid"] for r in before}

        room_client.create_room(data)
        after = room_client.get_rooms().json().get("rooms", [])
        new_rooms = [r for r in after if r["roomid"] not in before_ids]
        assert len(new_rooms) > 0
        room_id = new_rooms[0]["roomid"]

        with allure.step(f"DELETE /room/{room_id}"):
            response = room_client.delete_room(room_id)

        with allure.step("Verify 202"):
            assert response.status_code == 202

        with allure.step("Verify room no longer exists"):
            get_resp = room_client.get_room(room_id)
            assert get_resp.status_code == 500  # API returns 500 for missing rooms

    @allure.title("TC-ROOM-013: Delete room without auth returns 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_delete_room_no_auth(self, room_client_unauth: RoomClient, created_room: dict):
        room_id = created_room["roomid"]

        with allure.step(f"DELETE /room/{room_id} without auth"):
            response = room_client_unauth.delete_room(room_id)

        with allure.step("Verify 403"):
            assert response.status_code == 403

    @allure.title("TC-ROOM-014: Delete non-existent room returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_delete_room_not_found(self, room_client: RoomClient):
        with allure.step("DELETE /room/99999"):
            response = room_client.delete_room(99999)

        with allure.step("Verify 404"):
            assert response.status_code == 404


@allure.epic("Restful Booker Platform")
@allure.feature("Room")
class TestRoomContract:
    """Schema/contract validation for room responses."""

    @allure.title("TC-ROOM-015: Room object has required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_room_schema(self, room_client: RoomClient, created_room: dict):
        room_id = created_room["roomid"]

        with allure.step(f"GET /room/{room_id}"):
            response = room_client.get_room(room_id)

        with allure.step("Verify room schema"):
            assert response.status_code == 200
            room = response.json()
            required_fields = {"roomid", "roomName", "type", "accessible", "roomPrice", "description", "features", "image"}
            assert required_fields.issubset(set(room.keys()))
            assert isinstance(room["roomid"], int)
            assert isinstance(room["roomName"], str)
            assert room["type"] in ["Single", "Double", "Suite", "Family"]
            assert isinstance(room["accessible"], bool)
            assert isinstance(room["roomPrice"], int)
            assert isinstance(room["features"], list)
