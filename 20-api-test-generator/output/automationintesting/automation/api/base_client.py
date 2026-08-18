"""Base HTTP client with logging, timing, and Allure attachment."""

import time
import json
from typing import Any

import httpx
import allure

from config.settings import Config


class BaseClient:
    """HTTP wrapper — every request logs timing and attaches response to Allure."""

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = base_url or Config.BASE_URL
        self.token = token
        self.session = httpx.Client(base_url=self.base_url, timeout=float(Config.TIMEOUT))
        if token:
            self.session.cookies.set("token", token)

    def set_token(self, token: str) -> None:
        """Set auth token as cookie (API uses cookie-based auth)."""
        self.token = token
        self.session.cookies.set("token", token)

    def clear_token(self) -> None:
        """Remove auth cookie."""
        self.token = ""
        self.session.cookies.clear()

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        """Execute HTTP request with timing, logging, and Allure attachment."""
        start = time.time()
        response = self.session.request(method, path, **kwargs)
        elapsed_ms = round((time.time() - start) * 1000)

        # Build attachment payload
        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError):
            body = response.text[:5000] if response.text else ""

        attachment = {
            "method": method,
            "url": f"{self.base_url}{path}",
            "status": response.status_code,
            "time_ms": elapsed_ms,
            "response_body": body,
        }

        # Include request body if present
        if "json" in kwargs:
            attachment["request_body"] = kwargs["json"]
        if "data" in kwargs:
            attachment["request_body"] = kwargs["data"]
        if "params" in kwargs:
            attachment["query_params"] = kwargs["params"]

        allure.attach(
            json.dumps(attachment, indent=2, ensure_ascii=False, default=str),
            name=f"{method} {path} → {response.status_code} ({elapsed_ms}ms)",
            attachment_type=allure.attachment_type.JSON,
        )

        return response

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()
