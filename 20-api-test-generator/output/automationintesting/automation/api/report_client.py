"""Report client — typed methods for /report endpoints."""

import httpx
import allure

from api.base_client import BaseClient


class ReportClient(BaseClient):
    """Read operations for Report resource."""

    def get_report(self) -> httpx.Response:
        """GET /report — get booking report (requires auth)."""
        with allure.step("GET /report"):
            return self.get("/report")
