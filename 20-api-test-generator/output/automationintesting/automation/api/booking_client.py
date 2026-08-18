"""Booking client — typed methods for /booking endpoints."""

from typing import Any

import httpx
import allure

from api.base_client import BaseClient


class BookingClient(BaseClient):
    """CRUD operations for Booking resource."""

    def get_bookings(self, room_id: int) -> httpx.Response:
        """GET /booking?roomid={id} — list bookings for a room (requires auth)."""
        with allure.step(f"GET /booking?roomid={room_id}"):
            return self.get("/booking", params={"roomid": room_id})

    def get_booking(self, booking_id: int) -> httpx.Response:
        """GET /booking/{id} — get single booking (requires auth)."""
        with allure.step(f"GET /booking/{booking_id}"):
            return self.get(f"/booking/{booking_id}")

    def create_booking(self, booking_data: dict[str, Any]) -> httpx.Response:
        """POST /booking — create booking (public)."""
        with allure.step(f"POST /booking (room={booking_data.get('roomid', '?')})"):
            return self.post("/booking", json=booking_data)

    def update_booking(self, booking_id: int, booking_data: dict[str, Any]) -> httpx.Response:
        """PUT /booking/{id} — update booking (requires auth)."""
        with allure.step(f"PUT /booking/{booking_id}"):
            return self.put(f"/booking/{booking_id}", json=booking_data)

    def delete_booking(self, booking_id: int) -> httpx.Response:
        """DELETE /booking/{id} — delete booking (requires auth)."""
        with allure.step(f"DELETE /booking/{booking_id}"):
            return self.delete(f"/booking/{booking_id}")
