"""Message client — typed methods for /message endpoints."""

from typing import Any

import httpx
import allure

from api.base_client import BaseClient


class MessageClient(BaseClient):
    """CRUD operations for Message resource."""

    def get_messages(self) -> httpx.Response:
        """GET /message — list all messages (requires auth)."""
        with allure.step("GET /message"):
            return self.get("/message")

    def get_message(self, message_id: int) -> httpx.Response:
        """GET /message/{id} — get single message (requires auth)."""
        with allure.step(f"GET /message/{message_id}"):
            return self.get(f"/message/{message_id}")

    def create_message(self, message_data: dict[str, Any]) -> httpx.Response:
        """POST /message — create message (public)."""
        with allure.step(f"POST /message (name={message_data.get('name', '?')})"):
            return self.post("/message", json=message_data)

    def delete_message(self, message_id: int) -> httpx.Response:
        """DELETE /message/{id} — delete message (requires auth)."""
        with allure.step(f"DELETE /message/{message_id}"):
            return self.delete(f"/message/{message_id}")
