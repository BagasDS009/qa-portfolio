"""Room client — typed methods for /room endpoints."""

from typing import Any

import httpx
import allure

from api.base_client import BaseClient


class RoomClient(BaseClient):
    """CRUD operations for Room resource."""

    def get_rooms(self) -> httpx.Response:
        """GET /room — list all rooms (public)."""
        with allure.step("GET /room"):
            return self.get("/room")

    def get_room(self, room_id: int) -> httpx.Response:
        """GET /room/{id} — get single room (public)."""
        with allure.step(f"GET /room/{room_id}"):
            return self.get(f"/room/{room_id}")

    def create_room(self, room_data: dict[str, Any]) -> httpx.Response:
        """POST /room — create room (requires auth)."""
        with allure.step(f"POST /room (name={room_data.get('roomName', '?')})"):
            return self.post("/room", json=room_data)

    def update_room(self, room_id: int, room_data: dict[str, Any]) -> httpx.Response:
        """PUT /room/{id} — update room (requires auth)."""
        with allure.step(f"PUT /room/{room_id}"):
            return self.put(f"/room/{room_id}", json=room_data)

    def delete_room(self, room_id: int) -> httpx.Response:
        """DELETE /room/{id} — delete room (requires auth)."""
        with allure.step(f"DELETE /room/{room_id}"):
            return self.delete(f"/room/{room_id}")
