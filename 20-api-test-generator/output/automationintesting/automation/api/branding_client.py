"""Branding client — typed methods for /branding endpoints."""

from typing import Any

import httpx
import allure

from api.base_client import BaseClient


class BrandingClient(BaseClient):
    """Read/Update operations for Branding resource (singleton)."""

    def get_branding(self) -> httpx.Response:
        """GET /branding — get branding info (public)."""
        with allure.step("GET /branding"):
            return self.get("/branding")

    def update_branding(self, branding_data: dict[str, Any]) -> httpx.Response:
        """PUT /branding — update branding (requires auth)."""
        with allure.step("PUT /branding"):
            return self.put("/branding", json=branding_data)
