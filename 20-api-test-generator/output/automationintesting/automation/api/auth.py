"""Auth client — login, validate, logout, token management."""

import allure

from api.base_client import BaseClient
from config.settings import Config


class AuthClient(BaseClient):
    """Handles authentication against /auth endpoints."""

    def login(self, username: str = "", password: str = "") -> str:
        """Login and return token. Uses admin creds from config if not provided."""
        username = username or Config.ADMIN_USERNAME
        password = password or Config.ADMIN_PASSWORD

        with allure.step(f"POST /auth/login (user={username})"):
            response = self.post("/auth/login", json={
                "username": username,
                "password": password,
            })

        if response.status_code == 200:
            token = response.json().get("token", "")
            self.set_token(token)
            return token
        return ""

    def validate(self) -> dict:
        """Validate current token."""
        with allure.step("POST /auth/validate"):
            response = self.post("/auth/validate")
        return response.json() if response.status_code == 200 else {}

    def logout(self) -> int:
        """Logout and clear token."""
        with allure.step("POST /auth/logout"):
            response = self.post("/auth/logout")
        self.clear_token()
        return response.status_code
